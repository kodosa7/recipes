from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.db import connection
from django.db.models import Q
from django.http import HttpResponse
from datetime import datetime
from ipware import get_client_ip
from .forms import UserForm
from .models import Recipe
from .fusioncharts import FusionCharts
from collections import OrderedDict
import requests
import json


# Create your views here.
# homepage view with list of cities and links to them
def home_view(request):
    queryset = Recipe.objects.all()
    context = { 'recipes': queryset }
    return render(request, 'home_view.html', context)

# single recipe view by id
def recipe_id_view(request, id):
    currentRecipe = get_object_or_404(Recipe, id=id)

    form = UserForm()
    context = { 'thisRecipe': currentRecipe,
                'thisForm': form,
                'id': id }

    # store id number to temporary file
    with open("recipes/data/temp_id.json", "w") as out:
        data = str(id)
        out.write(data)

    return render(request, 'recipe.html', context)

# search field view (visible on default home view)
def recipe_search_view(request):
    searchButtonData = request.GET.get('query')
    searchResult = Recipe.objects.filter(Q(mealName__icontains=searchButtonData))
    searchResult_str = str(searchResult)
    context = { 'foundRecipes': searchResult,
                'foundRecipes_str': searchResult_str,
                'searchButtonData': searchButtonData }
    return render(request, 'recipes_found.html', context)

# success view (with charts)
def success_view(request):
    # get id from json file stored in recipe_id_view
    with open("recipes/data/temp_id.json", "r") as file:
        data_list = [id for id in file]
        id = data_list[0]

    # crop the IP address
    ip_tuple = get_client_ip(request)

    ip = str(ip_tuple)
    # check if there's True or False word in the IP string
    if "True" in ip:
        removed_chars = ["'", "(", ")", ",", "True", " "]
    else:
        removed_chars = ["'", "(", ")", ",", "False", " "]

    for char in removed_chars:
        ip = ip.replace(char, "")

    get_db_ip = Recipe.objects.filter(id=id).values('mealIP')
    print(str(get_db_ip.query))
    print(get_db_ip)

    # crop the IP taken from db
    db_ip = str(get_db_ip)
    # check if there's True or False word in the IP string taken from db
    if "True" in db_ip:
        removed_chars = ["'", "(", ")", ",", "True", " ", "<", ">", "[", "]", "{", "}", ":", "QuerySet", "mealIP"]
    else:
        removed_chars = ["'", "(", ")", ",", "False", " ", "<", ">", "[", "]", "{", "}", ":", "QuerySet", "mealIP"]

    for char in removed_chars:
        db_ip = db_ip.replace(char, "")

    print("db_ip", db_ip)

    ipMatch = False

    # compare current IP and db IP
    if ip == db_ip:
        print("ip and db_ip are equal!")
        print("this vote is invalid.")
        print("-" * 20)

        ipMatch = True

    lastIP = ip
    Recipe.objects.filter(id=id).update(mealIP=lastIP) # write current IP to db

    # check of POST request happened and process it
    if request.method == "POST":
        form = UserForm(request.POST)

        # is_valid() needs to have required=True in every form item
        if form.is_valid():
            selected = form.cleaned_data.get("radio_button")
            selectedInt = int(selected)

            # write current meal ID to the database
            Recipe.objects.filter(id=id).update(mealDbRating=selectedInt) # rating

            # create a json file and append collected data to it
            data_dict = {}
            data_dict[id]=selectedInt

            try:
                file = open("recipes/data/data.json")
            except FileNotFoundError:
                file = open("recipes/data/data.json", "a").close()

            # read the old json file, store it to list
            with open("recipes/data/data.json", "r") as file_read:
                data = json.load(file_read)

                # convert id number to string needed in following dict
                str_id = str(id)
                # make a dict with current single record
                single_dict_record = {str_id:selectedInt}

                # add new collected data to the list
                data.append(single_dict_record)

            # write new list with data to json file and beautize it
            with open("recipes/data/data.json", "w") as file_write:
                json.dump(data, file_write, indent=4, separators=(',', ': '))

            # finding duplicate values
            # from dictionary using flip
            flipped_dict = {}

            for item in data:
                for key, value in item.items():
                    if key not in flipped_dict:
                        flipped_dict[key] = [value]
                    else:
                        flipped_dict[key].append(value)

            # for each flipped_dict item calculate the average of values
            for key in flipped_dict:
                if key == str_id:
                    list_of_votes = flipped_dict[str_id]
                    length_of_votes = len(list_of_votes)
                    sum_of_votes = sum(list_of_votes)
                    average_of_votes = sum_of_votes // length_of_votes
                else:
                    pass

            # update database mealAverageRating field
            Recipe.objects.filter(id=id).update(mealAverageRating=average_of_votes)

            # set the string value and send it to the template via context value
            str_average_of_votes = str(average_of_votes)

            # Chart data
            # Chart data is passed to the `dataSource` parameter, as dictionary in the form of key-value pairs.
            dataSource = OrderedDict()

            # The `chartConfig` dict contains key-value pairs data for chart attribute
            chartConfig = OrderedDict()
            chartConfig["caption"] = "Average Recipe Rating Table"
            chartConfig["subCaption"] = "(rated from 1 to 10 points)"
            chartConfig["xAxisName"] = "Recipe"
            chartConfig["yAxisName"] = "Average Rating"
            chartConfig["numberSuffix"] = " points"
            chartConfig["theme"] = "candy"

            # The `chartData` dict contains key-value pairs data
            chartData = OrderedDict()

            # get names
            names_list = []
            for name in Recipe.objects.all():
                str_name = str(name)
                names_list.append(str_name)

            # get ratings
            rating_list = []
            for rating in Recipe.objects.all().values_list('mealAverageRating'):
                str_rating = str(rating)

                removed_chars = ["(", ",", ")"]
                for char in removed_chars:
                    str_rating = str_rating.replace(char, "")

                int_rating = int(str_rating)
                rating_list.append(int_rating)

            # import names + ratings to chart
            chartData = dict(zip(names_list, rating_list))

            dataSource["chart"] = chartConfig
            dataSource["data"] = []

            # Convert the data in the `chartData` array into a format that can be consumed by FusionCharts.
            # The data for the chart should be in an array wherein each element of the array is a JSON object
            # having the `label` and `value` as keys.

            # Iterate through the data in `chartData` and insert in to the `dataSource['data']` list.
            for key, value in chartData.items():
                data = {}
                data["label"] = key
                data["value"] = value
                dataSource["data"].append(data)

            # Create an object for the column 2D chart using the FusionCharts class constructor
            # The chart data is passed to the `dataSource` parameter.
            column2D = FusionCharts("column2d", "ex1" , "90%", "400", "chart-1", "json", dataSource)

            # if IPs are same, rate with "0"
            if ipMatch == False:
                return render(request, 'success.html', {'selected': selected,
                                       'lastIP': lastIP,
                                       'id': id,
                                       'averageVotes': str_average_of_votes,
                                       'chartOutput' : column2D.render(),
                                       'ipMatch': ipMatch,
                                       })
            else:
                str_average_of_votes = "0"
                return render(request, 'success.html', {'selected': selected,
                                       'lastIP': lastIP,
                                       'id': id,
                                       'averageVotes': str_average_of_votes,
                                       'chartOutput' : column2D.render(),
                                       'ipMatch': ipMatch,
                                       })

        else:
            return HttpResponse('Form is not valid')

    else:
        return HttpResponse('Bad HTTP request')
