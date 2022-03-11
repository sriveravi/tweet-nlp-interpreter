"""
Extracting features and training a classifier
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from transformers import BartTokenizer, BartModel
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
from tqdm import tqdm

tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')
model = BartModel.from_pretrained('facebook/bart-base')


class_dict_list = [
    {'file': 'cat_tweets.txt', 'data':[]},
    {'file': 'dog_tweets.txt', 'data':[]}]

# loop through files and extract features
for class_idx, class_obj in enumerate(class_dict_list):

    with open(class_obj['file'], 'r') as f:
        text_list = f.readlines()

    for line in tqdm(text_list):

        inputs = tokenizer(line, return_tensors="pt", truncation=True)
        outputs = model(**inputs)
        last_hidden_states = outputs.last_hidden_state        
        line_features = last_hidden_states.detach().numpy().mean(axis=1)
                        
        class_obj['data'].append(line_features)


# make the class labels
features = []
labels = []
names = []
for class_obj in enumerate(class_dict_list):
    features.append(np.vstack(class_obj['data']))
    labels.append(class_idx*np.ones((len(class_obj['data']),1)))
    names.append(class_obj['file'].split('.')[0])


# do some classification
X = np.vstack(features)
# X = scale(X)

y = np.vstack(labels)

reg = LogisticRegression(random_state=42).fit(X, y.ravel())
score = reg.score(X, y)

# get some metrics
print( f"Mean accuracy: {score:.2f}")

y_pred = reg.predict(X)
# y_pred = (y_pred>.5).astype(int)
# acc = accuracy_score(y, y_pred)
# print(f"Accuracy: {acc:.2f}")



X_pca = PCA(n_components=2).fit_transform(X)