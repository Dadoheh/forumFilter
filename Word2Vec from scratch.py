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


# ## Read dataset

# In[2]:


df = pd.read_csv('movie_review.csv')


# #### Drop useless columns

# In[3]:


df = df.drop(columns=['fold_id', 'cv_tag', 'html_id', 'sent_id'])
df.head()


# In[4]:


df[df['tag'] == 'neg']


# In[5]:


df_pos = df.iloc[:32937]
df_neg = df.iloc[32937:]


# In[6]:


df_pos['tag'].value_counts()


# In[7]:


df_neg['tag'].value_counts()


# ## Creating new DataFrame with only 1000 pos and 1000 neg tags

# In[8]:


x = random.randint(0, 32000)

new_df_pos = df_pos[x:x+1000]
new_df_neg = df_neg[x:x+1000]
df = pd.concat([new_df_pos, new_df_neg])
df.reset_index(drop=True, inplace=True)
df.head()


# ## Cleaning text

# In[9]:


def clean_text(text): # removing punctuation and lower the text
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for i in text: 
        if i in punc: 
            text = text.replace(i, "")
    text = text.lower()
    return text


# In[10]:


df['text'] = df['text'].apply(clean_text)


# ## Encoding 'tag'

# In[11]:


df['tag'] = df['tag'].apply(lambda x: 1 if x == "pos" else 0)


# In[12]:


df['tag'].value_counts()


# ## Spliting data into train and test set
# 

# In[13]:


from sklearn.model_selection import train_test_split

train, test = train_test_split(df, test_size=0.2)


# In[14]:


with open('./train_dataset_1000.pickle', 'wb') as f:
    cPickle.dump(train, f)
    
with open('./test_dataset_1000.pickle', 'wb') as f:
    cPickle.dump(test, f)


# ## Tokenize text

# In[15]:


all_text = ""
for i in range(len(train['text'])):
    all_text += train['text'].iloc[i]


# In[16]:


# all_text


# In[17]:


def tokenize(text):
    pattern = re.compile(r'[A-Za-z]+[\w^\']*|[\w^\']*[A-Za-z]+[\w^\']*')
    return pattern.findall(text.lower())


# In[18]:


tokens = tokenize(all_text)


# In[19]:


len(tokens)


# ## Mapping, encode, decode functions

# In[20]:


def mapping(tokens):
    word2id = {}
    id2word = {}
    
    for index, word in enumerate(set(tokens)):
        word2id[word] = index
        id2word[index] = word
    
    return word2id, id2word


# In[21]:


word2id, id2word = mapping(tokens)


# In[22]:


print(len(word2id))
print(len(id2word))


# In[23]:


def encode_text(text):
    tokens = tokenize(text)
    encoded_text = []
    for token in tokens:
        if token in word2id:
            encoded_text.append(word2id[token])
    return encoded_text


# In[24]:


def decode_text(encoded_text):
    decoded_text = []
    for index in encoded_text:
        decoded_text.append(id2word[index])
    return " ".join(decoded_text)


# ## Word2Vec class

# In[25]:


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


# In[26]:


len(tokens)


# ## Generating training data

# In[27]:


word2vec = Word2Vec(n=5, eta=0.01, epochs=25, window_size=2)

start_timer_data = time.perf_counter()

training_data = word2vec.generate_training_data(tokens, word2id)

end_timer_data = time.perf_counter()
print(f'Generating training data takes: {end_timer_data - start_timer_data}s')


# ## Training the model

# In[29]:


start_timer_model = time.perf_counter()

history = word2vec.train(training_data, show_progress=True)

plt.plot(range(len(history)), history, color="skyblue")
plt.show()

print('Saving completed model..')
with open('./word2vec1000.pickle', 'wb') as f:
    cPickle.dump(word2vec, f)

end_timer_model = time.perf_counter()
print(f'Training and saving the model takes: {end_timer_model - start_timer_model}s')

