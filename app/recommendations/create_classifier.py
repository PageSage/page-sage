import dill
from book_classifier import BookClassifier

test_volumes = []
test_labels = []

with open('emily_books_2_tier.txt', 'r') as test_file:
    for line in test_file:
        items = line.split(',')
        test_volumes.append(items[0])
        test_labels.append(int(items[1].strip()))

base_classifier = BookClassifier(test_volumes, test_labels)

base_classifier.fit()

dill.dump(base_classifier, open('emily_model.pkl', 'wb'))
