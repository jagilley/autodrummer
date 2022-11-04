# from tensorflow.keras.models import load_model
# import autokeras as ak
# import numpy as np

# loaded_model = load_model('text_reg', custom_objects=ak.CUSTOM_OBJECTS)

# # predict the bpm for 'rock jazz'
# genre = 'hiphop'

# print(loaded_model.predict(np.array([[genre]]))[0][0])

import joblib

# load model from joblib
reg = joblib.load('text_reg.joblib')

# predict the bpm for 'rock jazz'
genre = 'hiphop'

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# encode the style
style = model.encode(['disco'])

# predict the bpm
print(reg.predict(style))