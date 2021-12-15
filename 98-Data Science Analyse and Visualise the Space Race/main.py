# import pandas as pd
#
#
# df = pd.read_csv('mission_launches.csv')
# df = df.dropna()
# df.Price = df.Price.astype('string')
# # s = df.Price
# # df.Price = df.Price.replace('\"', '')
# # df.Price = [df.Price[i].replace(',', '') for i in range(len(df.Price))]
# df.Price = df.Price.str.replace(',', '')
# df.Price = df.Price.astype('float64')
# # df.Price = pd.to_numeric(df.Price, errors='ignore')
# # print(df.Price)
# print(df.info())

import pycountry
input_countries = ['American Samoa', 'Canada', 'France']

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_2

codes = [countries.get(country, 'Unknown code') for country in input_countries]

print(codes)