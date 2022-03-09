"""
Extracting features and training a classifier
"""
import numpy as np
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