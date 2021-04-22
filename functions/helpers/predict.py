import tensorflow as tf
from googleapiclient.http import MediaIoBaseDownload
import io
import os
import pandas as pd
import numpy as np
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

class Predict():
    def __init__(self,model_path):
        self.model=tf.keras.models.load_model(model_path)
    def predict(self,df):
        X = df.drop(['AREA','REGION'], axis = 1).astype('float32')
        return self.model.predict(X)