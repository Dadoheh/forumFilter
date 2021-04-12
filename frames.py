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

    """@staticmethod    #metoda byBus
    def analyse_byBus(comment, dictionary):
        lst = analiza_ator.split_comment(comment)
        max = 0
        if len(lst) < 3:
            max = analiza_ator.calc_mean(lst, dictionary)
        for i in range(len(lst) - 2):
            tmp = analiza_ator.calc_mean(lst[i:i + 2], dictionary)
            if tmp > max:
                max = tmp"""
    #@staticmethod
    #def analyse_byBus():

toxicitySeries = pd.read_csv('savedWord.csv')


#small tests
sample = 'i love hamburger'
sample2 = 'i am really proud of you however i want to fuck you'
sample3 = 'i am really proud of you'
sample4 = 'fuck'
#print(toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sample].empty)


print("Vulgarity factor: {}\n".format(Voting.voting(sample)))
print("Vulgarity factor: {}\n".format(Voting.voting(sample2)))
print("Vulgarity factor: {}\n".format(Voting.voting(sample3)))
print("Vulgarity factor: {}\n".format(Voting.voting(sample4)))


"""
TODO
bybus - lokalne średnie
obliczanie treshholdów - trzy treshholdy na sztywno

Średnioterminowo 
obliczanie treshholdów - heurystyka


Długoterminowo:
speech to text - do poszerzenia programu
"""

