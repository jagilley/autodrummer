# import autokeras as ak
import pandas as pd
import numpy as np

df = pd.read_csv('e-gmd-q/info-matrix-text.csv')

# filter for only beat == groove
df = df[df['beat_type'] == 'beat']

# deduplicate by note_text
df = df.drop_duplicates(subset=['note_text'])

df['style'] = df['style'].str.replace('/', ' ')

# filter such that style is of type string
df = df[df['style'].apply(lambda x: type(x) == str)]

# remove numeric values from style
df['style'] = df['style'].str.replace('\d+', '', regex=True)

df = df[['style', 'bpm']]

# bpm to numeric
df['bpm'] = pd.to_numeric(df['bpm'], errors='coerce')

# test train split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df['style'], df['bpm'], test_size=0.2, random_state=42)

X_train = X_train.to_numpy()
X_test = X_test.to_numpy()
y_train = y_train.to_numpy()
y_test = y_test.to_numpy()

# reg = ak.TextRegressor(overwrite=True, max_trials=5)
# reg.fit(X_train, y_train, epochs=10)

# print(reg.evaluate(X_test, y_test))

# # predict the bpm for 'rock jazz'
# # print(reg.predict(np.ndarray([['rock jazz']])))

# # save the model
# model = reg.export_model()
# try:
#     model.save("text_reg", save_format="tf")
# except Exception:
#     model.save("text_reg.h5")

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# encode the style
X_train = model.encode(X_train)
X_test = model.encode(X_test)

# train an MLP Regressor
from sklearn.neural_network import MLPRegressor
reg = MLPRegressor(hidden_layer_sizes=(100, 100, 100), max_iter=500)

# train a linear regressor
# from sklearn.linear_model import LinearRegression
# reg = LinearRegression()

reg.fit(X_train, y_train)

# evaluate the model
print(reg.score(X_test, y_test))

# predict the bpm for 'rock jazz'

# encode the style
style = model.encode(['rock jazz'])

# predict the bpm
print(reg.predict(style))

# save the model
import joblib
joblib.dump(reg, 'text_reg.joblib')