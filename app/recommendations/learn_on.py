import requests
import os
import re
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from copy import deepcopy


class BookClassifier(object):
    def __init__(self, volumes=[], ratings=[]):
        if (len(volumes) == 0) or (len(ratings) == 0):
            raise ValueError('Initial values cannot be zero')
        if (len(volumes) != len(ratings)):
            raise ValueError('Labels and data must have the same length')

        self.volumes = volumes
        self.ratings = ratings
        self.__book_data = []
        self.categories = dict()
        self.maturities = dict()
        self.books = []
        self.X_train, self.y_train = [],[]
        self.__model = None
        self.set_up()


    def set_up(self):
        self.__book_data = self.__pull_books(self.volumes, self.ratings)
        self.__find_categories(self.__book_data)
        #self.maturities = self.__find_maturities(self.book_data)
        self.books = self.__reformat(self.__book_data)
        self.X_train, self.y_train = self.__x_y_train(self.books)


    def __pull_books(self, volumes, labels=[]):
        book_data = []
        search_key = str(os.environ.get('SEARCH_KEY'))
        baseURL = 'https://www.googleapis.com/books/v1/volumes/'
        endURL = '?key=' + search_key

        headers = {'Accept': 'application/json'}

        for index, volume in enumerate(volumes):
            url = baseURL + str(volume) + endURL

            resp = requests.get(url, params=headers)
            if not resp.ok:
                raise ValueError('Response error: ' + str(resp)+ '; could not make call\n' + str(resp.json()))
            book_info = resp.json()
            new_book = {}

            try:
                page_count  =  int(book_info['volumeInfo']['pageCount'])
            except (KeyError):
                page_count = 100

            try:
                categories = self.__category_preprocessor(book_info['volumeInfo']['categories'])
            except (KeyError):
                categories = self.__category_preprocessor(['Fiction'])

            try:
                average_rating = float(book_info['volumeInfo']['averageRating'])
            except (KeyError):
                average_rating = float(3)

            try:
                ratings_count = int(book_info['volumeInfo']['ratingsCount'])
            except (KeyError):
                ratings_count = int(0)

            '''
            try:
                maturity_rating = book_info['volumeInfo']['maturityRating']
            except (KeyError):
                maturity_rating = 'NOT_MATURE'
            '''

            if labels != []:
                book_data.append({
                    'user_rating'       : labels[index],
                    'page_count'        : page_count,
                    'categories'        : categories,
                    'average_rating'    : average_rating,
                    'ratings_count'     : ratings_count
                    #'maturity_rating'   : maturity_rating
                })
            else:
                book_data.append({
                    'page_count'        : page_count,
                    'categories'        : categories,
                    'average_rating'    : average_rating,
                    'ratings_count'     : ratings_count
                    #'maturity_rating'   : maturity_rating
                })

        return book_data


    def __category_preprocessor(self, categories):
        if type(categories) != type(list()):
            return categories
        
        cats = []
        for category in categories:
            cat_split = category.split('/')
            for cat in cat_split:
                cat = cat.strip().lower()
                if cat not in cats:
                    cats.append(cat)

        return cats


    def __find_categories(self, books):
        index = 2
        for book in books:
            for category in book['categories']:
                if category not in self.categories.keys():
                    self.categories[category] = index
                    index += 1


    def __find_maturities(self, books):
        index = 0
        for book in books:
            if book['maturity_rating'] not in self.maturities:
                self.maturities[book['maturity_rating']] = index
                index += 1


    def __reformat(self, books):
        new_books = []
        for book in books:
            new_book = []
            for data in book:
                if 'categories' == data:
                    for category in self.categories:
                        new_book.append(0)
                elif 'maturity_rating' == data:
                    for maturity in self.maturities:
                        new_book.append(0)
                else:
                    new_book.append(book[data])
            new_books.append(new_book)
        for index, book in enumerate(new_books):
            for category in self.categories:
                if category in books[index]['categories']:
                    new_books[index][self.categories[category]] = books[index]['categories'].count(category)
            '''for maturities in self.maturities:
                if maturity in books[index]['maturities']:
                    new_books[index][len(maturities[maturity])
            '''
        return new_books


    def __x_y_train(self, books):
        books = deepcopy(books)
        labels = []
        new_books = []

        for book in books:
            labels.append(np.array(int(book.pop(0))))
            new_books.append(book)

        return (np.asarray(new_books), np.asarray(labels))


    def fit(self):
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(units=20, input_dim=self.X_train.shape[1],
                                     kernel_initializer='glorot_uniform',
                                     bias_initializer='zeros',
                                     activation='selu'))

        model.add(keras.layers.Dense(units=20, input_dim=self.X_train.shape[1],
                                     kernel_initializer='glorot_uniform',
                                     bias_initializer='zeros',
                                     activation='selu'))

        model.add(keras.layers.Dense(units=1, input_dim=self.X_train.shape[1],
                                     kernel_initializer='glorot_uniform',
                                     bias_initializer='zeros',
                                     activation='softmax'))

        sgd_optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-7, momentum=0.9)

        model.compile(optimizer=sgd_optimizer, loss='binary_crossentropy')

        history = model.fit(self.X_train, self.y_train,
                            batch_size=3, epochs=15, verbose=1,
                            validation_split=0.1)

        self.y_train_pred = model.predict_classes(self.X_train, verbose=0)

        self.__model = model

        
    def feature_space(self):
        return str(self.X_train.shape[0]) + ', ' + str(self.X_train.shape[1])
    
    
    def train_acc(self):
        print(self.y_train_pred)
        print(self.y_train)
        return np.sum(self.y_train_pred == self.y_train, axis=0)
    
        
    def __preprocess_book(self, book):
        book = deepcopy(book)
        book_data = [self.__pull_books(book)]
        
        return np.asarray(self.__reformat(book))


    def predict(self, book=[]):
        if book == [] or book:
            raise ValueError('Parameter cannot be an empty book')
        if self.__model == None:
            raise ValueError('Classifier needs training before predictions')
        if type(book) != type(str()):
            raise ValueError('Book must a valid volumeID of type "String"')

        X_sample = __preprocess_book(book)
        
        return self.__model.predict_classes(X_sample, verbose=0)


test_volumes = []
test_labels = []

with open('emily_books_2_tier.txt', 'r') as test_file:
    for line in test_file:
        items = line.split(',')
        test_volumes.append(items[0])
        test_labels.append(items[1].strip())

print('Length of volumes:\t', len(test_volumes))
print('Length of labels:\t', len(test_labels))

test_model = BookClassifier(test_volumes, test_labels)