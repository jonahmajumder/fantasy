import requests
from bs4 import BeautifulSoup
import csv
import os, sys
import numpy as np
import pickle

# nfl data function pool

def get_nfl_data(STAT_TYPE, YEAR):
    # create URL (page must actually exist)
    url = f'https://www.pro-football-reference.com/years/{YEAR}/{STAT_TYPE}.htm'
    # get page data and parse to nice HTML with beautiful soup
    r = requests.get(url)
    page = BeautifulSoup(r.content, 'html.parser')

    # this is convenient to have defined for future comparisons
    TAG_TYPE = type(page.find('head'))

    # main table is always within a div with ID of 'content'
    content_div = page.find('div', {'id': 'content'})
    # there seems to always just be one table head element, so find that
    table_head = content_div.find('thead')

    # look near the found table head for the main table body
    main_table_body = None
    for tag in table_head.parent.children:
         if type(tag) is TAG_TYPE:
            if tag.name == 'tbody':
                main_table_body = tag

    # make sure the above worked
    if (main_table_body == None):
        print('Table body not found!')
        return []

    # parse the table head for the column titles
    # note that sometimes there are multiple header rows, and in those cases we want the last one
    all_rows = table_head.find_all('tr')
    category_row = all_rows[-1] # get the last row

    categories = []
    category_tags = category_row.find_all('th')
    for tag in category_tags:
        categories.append(tag['data-stat']) # the attribute 'data-stat' seems to have the information we want

    # parse the actual table body for the data itself
    # note that there are more header rows interspersed in the table rows that we don't want
    # these unwanted rows can be ignored by making sure the row has no 'class' attribute

    def table_row_without_class(tag):
        return (not tag.has_attr('class')) and (tag.name == 'tr')

    table_rows = main_table_body.find_all(table_row_without_class)

    all_data = []
    for i, row in enumerate(table_rows):
        row_data = []
        data_tags = row.find_all(('th','td')) # get all data HTML tags
        for tag in data_tags:
            child_tags = tag.find_all()
            if child_tags: # this if statement checks if the list is not empty (i.e. there is at least 1 child)
                data = child_tags[0].contents
            else:
                data = tag.contents
            # make sure it's not an empty data point
            if data:
                row_data.append(data[0])
            else:
                row_data.append('') # put in an empty string just to have something there
        all_data.append(row_data)

    data_with_header = np.vstack((categories, all_data))

    return data_with_header

def _data_col(data, col_name):
    col_headers = [data[0, i] for i in range(np.shape(data)[1])]
    try:
        col_idx = col_headers.index(col_name)
    except ValueError:
        print('Column not found in data.')
        return []
    raw_col = data[1:, col_idx]
    try:
        col = raw_col.astype(float)
        return col
    except ValueError:
        return raw_col

def get_data_columns(data, column_names):
    cols = []
    for col_name in column_names:
        cols.append(_data_col(data, col_name))
    outmat = np.hstack(cols)
    return outmat

def data_to_csv(data, csvfilename):
    outfile = open(csvfilename,'w')
    wr = csv.writer(outfile)
    wr.writerows(data)
    outfile.close()
    return

def data_from_csv(csvfilename):
    infile = open(csvfilename,'r')
    rdr = csv.reader(infile)
    data = []
    for row in rdr:
        data.append(row)
    infile.close()
    return np.matrix(data)

def save_data_variable(data, picklefile):
    pickle.dump(data, open(picklefile, 'wb'))
    return

def load_data_variable(picklefile):
    data = pickle.load(open(picklefile, 'rb'))
    return data