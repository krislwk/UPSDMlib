import pandas as pd
from opencage.geocoder import OpenCageGeocode

GEOCODE_API_KEY = "77987660cbc445de9b873604e55f2d3d"

def geocodeColumn(datasetLocation, API_KEY, cityColumnName, HQLocationColumnName): #creates a new excel file with a new column longitude and latitude
    location_arr = []
    df = pd.read_excel(datasetLocation)
    city_list = df[cityColumnName].to_numpy() #Putting cities in a list
    country_list = df[HQLocationColumnName].to_numpy() #Putting locations in a list

    country_list_index = 0
    for x in country_list: #Turning every element in the column to a country name
        country = x.split(", ")[1]
        if len(country) == 2:
            country_list[country_list_index] = "United States"
        else:
            country_list[country_list_index] = country
        country_list_index += 1

    for x in range(len(city_list)): #grabbing longtitude and latitude of every location
        combined = "{0}, {1}".format(city_list[x], country_list[x])
        location_arr.append(combined)
        geocoder = OpenCageGeocode(API_KEY)
        longlatArr = []
        for x in location_arr:
            query = x
            result = geocoder.geocode(query)
            lat = result[0]['geometry']['lat']
            lng = result[0]['geometry']['lng']
            combined = str(lat) + ", " + str(lng)
            longlatArr.append(combined)

        df['long lat'] = longlatArr #the dataset file should now have a new column containing the PE location's long and lat
        df.to_excel("output.xlsx")
