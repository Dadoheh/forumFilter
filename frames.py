import pandas as pd

file = open('DictOfNegativeWords.txt', 'w')
frame = pd.read_csv('train.csv')

dictionary = {}
dictionary_bad = {}
for i in range(len(frame)-1, 0, -1):
    comment = frame.iloc[i]['comment_text']
    x = [word.strip(':,;"-_·()[]{}\n?!@|.') for word in comment.split()]
    bad=frame.iloc[i]['toxic']+frame.iloc[i]['severe_toxic']+frame.iloc[i]['obscene']+frame.iloc[i]['threat']+frame.iloc[i]['identity_hate']+frame.iloc[i]['insult']
    for j in range(len(x)):
        if x[j] != '':
            slowo=x[j].lower()
            if slowo in dictionary:
                dictionary[slowo] = dictionary[slowo]+1
                if bad>0:
                    dictionary_bad[slowo] = dictionary_bad[slowo] + 1
            else:
                dictionary[slowo] = 1
                if bad > 0:
                    dictionary_bad[slowo] = 1
                else:
                    dictionary_bad[slowo] = 0

for key in dictionary.keys():
    result = str((key, float(dictionary_bad[key]/dictionary[key])))
    file.write(result)
    print(result)
file.close()

"""
TODO-
    analizowanie poziomu toksyczności
        wczytanie listy słów z pliku txt
        myślimy jak zanalizować dane

Kolejne spotkanie:
Niedziela 11.04.21
"""

# | SLOWO | #appearance | #bad |
#              +1         +1

# list.append(slowo)
# x=list[k]

"""dataFrame = pd.DataFrame(index=dictionary_bad.values(), columns=[dictionary])
print(dataFrame)"""