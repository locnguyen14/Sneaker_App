from flask import Flask
import pickle
import os

# Global constant for classifier, scaler, pca
MODEL_FOLDER = 'webscrapezappos/pkl_file'
CLASSIFIER = pickle.load(open(os.path.join(MODEL_FOLDER, 'model.pkl'), 'rb'))
SCALER = pickle.load(open(os.path.join(MODEL_FOLDER, 'scaler.pkl'), 'rb'))
PCA = pickle.load(open(os.path.join(MODEL_FOLDER, 'pca.pkl'), 'rb'))
ENCODER = pickle.load(open(os.path.join(MODEL_FOLDER, 'encoder.pkl'), 'rb'))

UPLOAD_FOLDER = 'webscrapezappos/static/images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '19031995'

from webscrapezappos import routes 
