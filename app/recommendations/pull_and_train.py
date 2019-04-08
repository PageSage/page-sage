import requests
import os
from sys import argv
import re
import numpy as np
#from sklearn.model_selection import GridSearchCV
#from sklearn.decomposition import LatentDirichletAllocation

# See page 270
# See page 284 for using prediction and prediction probability

test_volumes = [{'id' : 'i_-bdQjbAZ8C',
                'rating' : 5}]
book_names = ['Jonathan Strange']

# Actual labels should be ratings, table info should be what is currently labels


def pull_books(book_list):
    book_data = []
    search_key = str(os.environ.get('SEARCH_KEY'))
    baseURL = 'https://www.googleapis.com/books/v1/volumes/'
    endURL = '?key=' + search_key
    headers = {'Accept': 'application/json'}
    for volume in book_list:
        #print(volume)
        url = baseURL + volume['id'] + endURL
        book_info = requests.get(url, params=headers).json()
        print(book_info)
        print()
        new_book = {}
        new_book['rating'] = volume['rating']

        ## Replacement/Default Values for non-existent information in JSON
        try:
            page_count = int(book_info['volumeInfo']['pageCount'])
        except (KeyError):
            page_count = 100

        try:
            categories = category_preprocessor(book_info['volumeInfo']['categories'])
        except (KeyError):
            categories = category_preprocessor(['Fiction'])

        try:
            average_rating = float(book_info['volumeInfo']['averageRating'])
        except (KeyError):
            average_rating = float(3.5)

        try:
            ratings_count = book_info['volumeInfo']['ratingsCount']
        except (KeyError):
            ratings_count = float(0)

        try:
            maturity_rating = book_info['volumeInfo']['maturityRating']
        except (KeyError):
            maturity_rating = 'NOT_MATURE'

        try:
            description = text_preprocessor(book_info['volumeInfo']['description'])
        except (KeyError):
            cats = ""
            for cat in categories:
                cats += cat + " "
            #description = text_preprocessor(book_info['volumeInfo']['title'] + " " str(categories))
            description = text_preprocessor(cats)

        book_data.append({
            'rating'         : volume['rating'],
            'page_count'     : page_count,
            'categories'     : categories,
            'average_rating' : average_rating,
            'ratings_count'  : ratings_count,
            'maturity_rating': maturity_rating,
            'description'    : description
        })
        
    return book_data

def text_preprocessor(text):
    text = re.sub('<[^>]*>', ' ', text)
    text_split = text.split('\\')
    return ''.join(text_split)


def category_preprocessor(categories):
    if type(categories) != type(list()):
        return categories
    output = []
    for category in categories:
        cat_split = category.split('/')
        output.append(''.join(cat_split))
    return output


def make_processable(books):
    data = []
    for book in books:
        book_data = []
        for item in book:
            book_data.append(book[item])
        print(book_data)
        data.append(book_data)
    return data

def gen_labels(books):
    labels = []
    for book in books:
        for item in book:
            labels.append(item)
            print(item)
        break
    return np.array(labels)

# Structure of Data

'''
test = pull_books(test_volumes)
data = make_processable(test)
labels = gen_labels(test)
print(labels)
print(data)
'''


if __name__ == '__main__':
    arg_length = len(argv)
    file_num = 1
    while file_num < arg_length:
        test_volumes = []
        with open(str(argv[file_num]), 'r') as test_data:
            for line in test_data:
                items = line.split('  ')
                new_volume = {'id': items[0], 'rating': items[1].strip()}
                test_volumes.append(new_volume)
        print("Made it here")
        test = pull_books(test_volumes)
        data = make_processable(test)
        labels = gen_labels(test)
        print(labels)
        print(data)
        file_num += 1
