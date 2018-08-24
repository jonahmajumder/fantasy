# import all the functions for use
from nfl_function_pool import *

# as an example, let's get the rushing data from 2017 and save it as 'rushing.csv'

stat = 'rushing'
year = '2017'

csvfile = 'rushing.csv'

rushing_data = get_nfl_data(stat, year)

data_to_csv(rushing_data, csvfile)
 
