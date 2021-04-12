import pandas as pd
import re


class DataCreating:
    @staticmethod
    def create_data():  # 280 k records processed within 2 hours :D
        file = open('DictOfNegativeWords.txt', 'w')  # file  to the modification
        frame = pd.read_csv('train.csv', low_memory=True)
        dictionary, dictionary_bad = {}, {}
        toxicitySeries = pd.Series(index=[], dtype=float)

        for i in range(len(frame) - 1, 0, -1):
            comment = frame.iloc[i]['comment_text']
            x = [word.strip(':,;"-_·()[]{}\n?!@|.') for word in comment.split()]
            bad = (frame.iloc[i]['toxic'] + frame.iloc[i]['severe_toxic']
                   + frame.iloc[i]['obscene'] + frame.iloc[i][
                'threat'] + frame.iloc[i]['identity_hate'] + frame.iloc[i]['insult'])
            for j in range(len(x)):
                any = x[j].lower()
                if any != '':
                    if any in dictionary:
                        dictionary[any] += 1
                        if bad > 0:
                            dictionary_bad[any] += 1
                    else:
                        dictionary[any] = 1
                        if bad > 0:
                            dictionary_bad[any] = 1
                        else:
                            dictionary_bad[any] = 0
        for key in dictionary.keys():
            #result = str((key, float(dictionary_bad[key] / dictionary[key])))
            # file.write(result)

            toxicityRatio = float(dictionary_bad[key] / dictionary[key])
            toxicitySeries[key] = toxicityRatio

        file.close()
        print("Length of a dictionary {}".format(len(dictionary)))

        toxicitySeries.to_csv('savedWord.csv')
        return toxicitySeries

    @staticmethod
    def read_data_from_file():  # to the modification
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


class Voting:
    
    @staticmethod
    def voting(sample):
        averageToxicity = 0.72  #  = toxicitySeries.mean()
        counter = 0
        sampleSplit = (sample.split(' '))
        lenSampleSplit = len(sampleSplit)
        print(sampleSplit)
        for i in range(len(sampleSplit)):
            if not (toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[i]].empty):
                counter += float(toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[i], '0'].item())
            else: lenSampleSplit -= 1  # setting unknown word as not important

        toxicityOfWord = counter/lenSampleSplit
        if toxicityOfWord > averageToxicity:
            result = ("Bad sentence with ", toxicityOfWord, "toxicity ratio",
                    " Avg toxicity =", averageToxicity)
        else:
            result = ("Good sentence with ", toxicityOfWord, "toxicity ratio",
                    " Avg toxicity = ", averageToxicity)
        return result



toxicitySeries = pd.read_csv('savedWord.csv')

#small tests

sample = 'and i really like you'
sample2 = 'fuck you motherfucker idiot'
sample3 = 'i am really proud of you'
sample4 = 'fuck'
#print(toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sample].empty)

print("Vulgarity factor: {}\n".format(Voting.voting(sample)))
print("Vulgarity factor: {}\n".format(Voting.voting(sample2)))
print("Vulgarity factor: {}\n".format(Voting.voting(sample3)))
print("Vulgarity factor: {}\n".format(Voting.voting(sample4)))



