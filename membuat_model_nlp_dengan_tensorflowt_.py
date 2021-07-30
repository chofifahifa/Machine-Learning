# -*- coding: utf-8 -*-
"""Membuat Model NLP dengan TensorFlowt .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13CFgpAhsb6gCW5SC19bqLsulo_fEi39a

# Chofifah Fitrotul Hasanah
chofifahfitrotulhasanah@gmail.com
"""

import pandas as pd
from google.colab import files
uploaded = files.upload()

df = pd.read_csv('/content/train.csv')
df

category = pd.get_dummies(df.sentiment)
df_baru = pd.concat([df, category], axis=1)
df_baru = df_baru.drop(columns='sentiment')
df_baru

from collections import Counter

def wordCount(text):
  count = Counter()
  for i in text.values :
    for word in i.split():
      count[word] += 1
  return count

text = df.text
counter = wordCount(text)

num_word = len(counter)
print(num_word)

sentiment = df_baru['text'].values
label = df_baru[['neg', 'pos']].values

from sklearn.model_selection import train_test_split
sentiment_latih, sentiment_test, label_latih, label_test = train_test_split(sentiment, label, test_size=0.2) #80% untuk training dan 20% untuk testing

# mengubah setiap kata pada dataset ke dalam bilangan numerik dengan fungsi Tokenizer
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer = Tokenizer(num_words=280617, oov_token='x')
tokenizer.fit_on_texts(sentiment_latih)

sekuens_latih = tokenizer.texts_to_sequences(sentiment_latih)
sekuens_test = tokenizer.texts_to_sequences(sentiment_test)

padded_latih = pad_sequences(sekuens_latih)
padded_test = pad_sequences(sekuens_test)

padded_latih.shape

from tensorflow.keras import layers
from tensorflow.keras import Sequential

model = Sequential([
    tf.keras.layers.Embedding(input_dim=280617, output_dim=16),
    tf.keras.layers.LSTM(64),
     tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')])
model.summary()

model.compile(
    optimizer='rmsprop',
    loss='binary_crossentropy', #terdapat 2 kelas
    metrics=['accuracy'])

from keras.callbacks import ModelCheckpoint
checkpoint = ModelCheckpoint(
    filepath='my_best_model.hdf5', 
    monitor='val_accuracy',
    verbose=1, 
    save_best_only=True,
    save_weights_only=False,
    mode='auto')

history = model.fit(padded_latih, label_latih, epochs=10, validation_data=(padded_test, label_test), callbacks=[checkpoint])

from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import numpy
#Plot akurasi dan loss data

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()