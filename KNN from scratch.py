#!/usr/bin/env python
# coding: utf-8

# ## Importing

# In[1]:


import numpy as np
import pandas as pd
import re
import random
import matplotlib.pyplot as plt
import _pickle as cPickle
import time
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'svg'")
plt.style.use("seaborn")


# ## Word2Vec class

# In[2]:


class Word2Vec: # skip-gram model
    def __init__(self, n, eta, epochs, window_size):
        self.n = n # dimension of word embeddings (dimension of word's vector)
        self.eta = eta # learning rate
        self.epochs = epochs # number of epochs
        self.window = window_size # size of window context
    
    def generate_training_data(self, tokens, word2id):
        VOCAB_SIZE = len(word2id)
        tokens_len = len(tokens)
        training_data = []
        window = self.window
        self.v_count = VOCAB_SIZE
        print('Started generating data...')
        for i in range(tokens_len):
            
            X = self.one_hot_encode(word2id[tokens[i]], VOCAB_SIZE)
            
            if i % 1000 == 0:
                print(f'i: {i} in progres..')

            # left site of the word
            if i - window < 0:
                start = 0
            else:
                start = i - window

            # right site of the word

            if i + window + 1 > tokens_len:
                end = tokens_len
            else:
                end = i + window + 1

            idx = range(start, end)
            y = []
            for j in idx:
#                 if i % 1000 == 0:
#                     print(f'j: {j}')
                if i == j:
                    continue

                
                y.append(self.one_hot_encode(word2id[tokens[j]], VOCAB_SIZE))
            training_data.append([X, y])

        print("END. Now wait for converting list to numpy array..")
        return np.array(training_data, dtype=object)
    
    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)
    
    def one_hot_encode(self, id, vocab_size):
        vector = np.zeros(vocab_size)
        vector[id] = 1
        return list(vector)
    
    def forward(self, x):
        hidden = np.dot(self.w1.T, x)
        output = np.dot(self.w2.T, hidden)
        y_c = self.softmax(output)
        return y_c, hidden, output
    
    def backpropagation(self, e, h, x):
        dl_dw2 = np.outer(h, e)  
        dl_dw1 = np.outer(x, np.dot(self.w2, e.T))

        # UPDATE WEIGHTS
        self.w1 = self.w1 - (self.eta * dl_dw1)
        self.w2 = self.w2 - (self.eta * dl_dw2)
    
    def train(self, training_data, show_progress=True):
        print("\n Started training data..")
        self.w1 = np.random.uniform(-1, 1, (self.v_count, self.n))     # embedding matrix
        self.w2 = np.random.uniform(-1, 1, (self.n, self.v_count))     # context matrix
        history = []
        for i in range(self.epochs):
        
            self.loss = 0

            for target, context in training_data:

                    # FORWARD PASS
                    y_pred, hidden, output = self.forward(target)

                    # CALCULATE ERROR
                    EI = []
                    for word in context:
                        EI.append(np.subtract(y_pred, word))
                    EI = np.sum(EI, axis=0)
 
                    # BACKPROPAGATION
                    self.backpropagation(EI, hidden, target)

                    # CALCULATE LOSS
                    self.loss += -np.sum([output[word.index(1)] for word in context]) + len(context) * np.log(np.sum(np.exp(output)))
                
            history.append(self.loss)
            
            with open('./word2vec1000.pickle', 'wb') as f:
                cPickle.dump(word2vec, f)
            
            if show_progress:
                print(f'Epoch: {i}/{self.epochs}, Loss: {self.loss}')
        
        return history
        
    def get_vector(self, word, word2id):
        if word in word2id:
            w_index = word2id[word]
            v_w = self.w1[w_index]
            return v_w
        else:   
            return np.zeros(self.n)


# ## Loading data

# In[3]:


with open(r"./train_dataset_1000.pickle", "rb") as f:
    train = cPickle.load(f)

with open(r"./test_dataset_1000.pickle", "rb") as f:
    test = cPickle.load(f)


# In[4]:


all_text = ""
for i in range(len(train['text'])):
    all_text += train['text'].iloc[i]


# In[5]:


def tokenize(text):
    pattern = re.compile(r'[A-Za-z]+[\w^\']*|[\w^\']*[A-Za-z]+[\w^\']*')
    return pattern.findall(text.lower())


# In[6]:


tokens = tokenize(all_text)


# In[7]:


def mapping(tokens):
    word2id = {}
    id2word = {}
    
    for index, word in enumerate(set(tokens)):
        word2id[word] = index
        id2word[index] = word
    
    return word2id, id2word

word2id, id2word = mapping(tokens)


# ## Loading model

# In[8]:


with open(r"./word2vec1000.pickle", "rb") as f:
    model = cPickle.load(f)


# In[9]:


model.get_vector('is', word2id)


# ## Vectorizing text

# In[10]:


def vectorize_sentence(sentence):
    vectorized_sentence = []
    for word in sentence.split():
        vectorized_sentence.append(model.get_vector(word, word2id))
    return vectorized_sentence


# In[11]:


train['vector'] = train['text'].apply(vectorize_sentence)
test['vector'] = test['text'].apply(vectorize_sentence)


# ## Make all vectors the same length

# In[12]:


def make_same_length(vector):
    MAX_LENGTH = 80
    VECTOR_DIMENSION = 5
    while len(vector) < 80:
        vector.append(np.zeros(VECTOR_DIMENSION))
    return vector


# In[13]:


train['vector'] = train['vector'].apply(make_same_length)
test['vector'] = test['vector'].apply(make_same_length)


# In[14]:


train.head()


# ## KNN Classfication

# In[15]:


class KNN:
    @staticmethod
    def minkowskiMetric(v1, v2, m):
        distance = 0
        for i in range(len(v1)):
            distance += abs(v1[i] - v2[i])**m
        distance = distance ** (1/m)
        return np.sum(distance)
    
    @staticmethod
    def clustering(testSample, X, k, classes):
        distances = []
        m = 2
        # obliczenie odlegosci
        for i in range(len(X)):
            distances.append((KNN.minkowskiMetric(testSample, X['vector'].iloc[i], m), i)) # do listy distances dodaje (distance, index)
            
        # posortowanie odleglosci
        distances = sorted(distances) #sortuje distance wraz z indexem
        
        # glosowanie
        for i in range(0, k):
            classes[X['tag'].iloc[distances[i][1]]] += 1
            
        #zwrocenie wyniku
        return max(classes, key=classes.get)


# In[16]:


for k in range(2, 8):
    corrected = 0
    for i in range(len(test)):
        classes = {0: 0, 1: 0}
        result = KNN.clustering(test['vector'].iloc[i], train, k, classes)
        if result == test['tag'].iloc[i]:
            corrected += 1

    accuracy = corrected / len(test) * 100
    print(f'K = {k} - Accuracy is {accuracy}%')

