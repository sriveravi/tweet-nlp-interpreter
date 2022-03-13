# from https://shap.readthedocs.io/en/latest/example_notebooks/text_examples/sentiment_analysis/Using%20custom%20functions%20and%20tokenizers.html

import matplotlib
from numpy import vstack
import shap
from classify import get_features
from classify import reg as classifier
import numpy as np
from classify import class_names
# this defines an explicit python function that takes a list of strings and outputs scores for each class
def f(x):
    features = []
    for line in x:
        features.append(get_features(line))
    features = np.vstack(features)
    return classifier.predict(features)


# build an explainer by explicitly creating a masker
method = "default masker"
if method == "default masker":
    masker = shap.maskers.Text(r"\W") # this will create a basic whitespace tokenizer
    explainer = shap.Explainer(f, masker) #, output_names=class_names[1:])
else:
    raise NotImplementedError("TODO: Implement more masker methods")

x = [
    'RT @dog_rates: This is Charlie. He has literal heart-eyes. 14/10 would be an honor to pet ', 
    'today we took a new route. during our walk. this is very exciting. i did not realize i had unlocked. this part of the map', 
    'i know. you have. some problems. right now. but. my problem. is that. you. are. not. petting me. and isn’t that. so… ',
    ]
shap_values = explainer(x)

shap.plots.text(shap_values)¬