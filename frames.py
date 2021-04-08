import pandas as pd

# import numpy as np

frame = pd.read_csv('train.csv')

dictionary = {}
dictionary_bad = {}
for i in range(10, -1, -1):
    comment = frame.iloc[i]['comment_text']
    x = [word.strip(':,;"-_·()[]{}\n?!') for word in comment.split()]

    # print(len((x)))
    # print(x)
    bad = frame.iloc[i]['toxic'] + frame.iloc[i]['severe_toxic'] + frame.iloc[i]['obscene'] + frame.iloc[i]['threat'] + \
          frame.iloc[i]['identity_hate']

    for j in range(len(x)):
        if x[j] != '':
            if x[j] in dictionary:
                dictionary[x[j]] = dictionary[x[j]] + 1
                dictionary_bad[x[j]] = dictionary_bad[x[j]] + 1
            else:
                dictionary[x[j]] = 1
                dictionary_bad[x[j]] = 1

for key in dictionary.keys():
    print(key, float(dictionary[key] / dictionary_bad[key]))

"""dataFrame = pd.DataFrame(index=dictionary_bad.values(), columns=[dictionary])
print(dataFrame)"""

# | SLOWO | #appearance | #bad |
#              +1         +1


# list.append(slowo)
# x=list[k]

"""
a_list = ["a", "", "c"]

without_empty_strings = []
for string in a_list:
    if (string != ""):
        without_empty_strings.append(string)

        print(without_empty_strings)
OUTPUT
['a', 'c']
"""


dataFrame = pd.DataFrame(index=dictionary_bad.values(), columns=[dictionary])
print(dataFrame)