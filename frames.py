import pandas as pd
import re


def create_data():
    file = open('DictOfNegativeWords.txt', 'w')
    frame = pd.read_csv('train.csv')
    dictionary, dictionary_bad = {}, {}

    for i in range(len(frame) - 1, 0, -1):
        comment = frame.iloc[i]['comment_text']
        x = [word.strip(':,;"-_·()[]{}\n?!@|.') for word in comment.split()]
        bad = frame.iloc[i]['toxic'] + frame.iloc[i]['severe_toxic'] + frame.iloc[i]['obscene'] + frame.iloc[i][
            'threat'] + frame.iloc[i]['identity_hate'] + frame.iloc[i]['insult']
        for j in range(len(x)):
            slowo = x[j].lower()
            if slowo != '':
                if slowo in dictionary:
                    dictionary[slowo] += 1
                    if bad > 0:
                        dictionary_bad[slowo] += 1
                else:
                    dictionary[slowo] = 1
                    if bad > 0:
                        dictionary_bad[slowo] = 1
                    else:
                        dictionary_bad[slowo] = 0
    for key in dictionary.keys():
        result = str((key, float(dictionary_bad[key] / dictionary[key])))
        file.write(result)
        #print(result)
    file.close()
    print("Długość zapisywanego słownika {}".format(len(dictionary)))


def read_data_from_file():
    file = open('DictOfNegativeWords.txt', 'r')
    outputNegative = file.read().split(')(')
    print(type(outputNegative))
    outputDict = {}

    for i in range(len(outputNegative)):
        temp = outputNegative[i]
        key = re.search(r"'(.*?)'", temp)
        variable = float(temp.split(', ')[1][:-1])
        if key and variable:
            key = key.group()
            outputDict[str(key[1:-1])] = variable

    return len(outputDict), outputDict


print(read_data_from_file())
#create_dataa()

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
