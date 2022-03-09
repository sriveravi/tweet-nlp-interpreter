"""
Extracting features and training a classifier
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from transformers import BartTokenizer, BartModel

tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')
model = BartModel.from_pretrained('facebook/bart-base')

file_list = ['cat_tweets.txt', 'dog_tweets.txt']
data_list = [[]]*len(file_list)


# loop through files and extract features
for class_idx, the_file in enumerate(file_list):

    with open(the_file, 'r') as f:
        text_list = f.readlines()

    for line in text_list:

        inputs = tokenizer(line, return_tensors="pt", truncation=True)
        outputs = model(**inputs)

        last_hidden_states = outputs.last_hidden_state
        data_list[class_idx].append(last_hidden_states.detach().numpy().mean(axis=1))


# make the class labels
features = []
labels = []
names = []
for class_idx, the_file in enumerate(file_list):
    features.append(np.vstack(data_list[class_idx]))
    labels.append(class_idx*np.ones((len(data_list[class_idx]),1)))
    names.append(the_file.split('.')[0])


# do some classification
X = np.vstack(features)
y = np.vstack(labels)

reg = LinearRegression().fit(X, y)
score = reg.score(X, y, )

# get some metrics
print( f"R^2 score (1.0 is perfect, const is 0.): {score:.2e}")

y_pred = reg.predict(X)
y_pred = (y_pred>.5).astype(int)
acc = accuracy_score(y, y_pred)
print(f"Accuracy: {acc:.2f}")