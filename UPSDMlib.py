import pandas as pd
from opencage.geocoder import OpenCageGeocode

GEOCODE_API_KEY = "77987660cbc445de9b873604e55f2d3d"

#creates a new excel file containing the inputted dataset but with a new column longitude and latitude
def geocodeColumn(datasetLocation, API_KEY, cityColumnName, HQLocationColumnName):
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
        df.to_excel("LongLatoutput.xlsx")

#uses label encoding to encode a column; method assumes that all possible unique values are present in the column
#creates a new excel file with the inputted dataset but with the column replaced with the label encoded version
def labelEncode(datasetLocation, columnName):
    df = pd.read_excel(datasetLocation)
    list = df[columnName].to_numpy()
    uniqueValues = numpy.unique(list)
    labelColumn = []
    for originalValue in list:
        for index in range(len(uniqueValues)):
            if originalValue == uniqueValues[index]:
                labelColumn.append(index + 1)
    df[columnName] = labelColumn
    df.to_excel("labelEncodeOutput.xlsx")
