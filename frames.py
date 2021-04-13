import pandas as pd
#import re


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
        file.close()    # to deletion
        print("Length of a dictionary {}".format(len(dictionary)))
        toxicitySeries.to_csv('savedWord.csv')
        return toxicitySeries


class Voting:

    toxicitySeries = pd.read_csv('savedWord.csv')

    @staticmethod
    def voting(sampleSplit):
        averageToxicity = 0.72  # = toxicitySeries.mean()
        counter = 0
        if type(sampleSplit) is not list:
            sampleSplit = (sampleSplit.split(' '))
        lenSampleSplit = len(sampleSplit)
        #print("co to jest", sampleSplit)    # to remove
        for i in range(len(sampleSplit)):
            if not toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[i]].empty:
                counter += float(toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[i], '0'].item())
            else: lenSampleSplit -= 1  # setting unknown word as not important

        toxicityOfWord = counter/lenSampleSplit

        if toxicityOfWord > averageToxicity:
            result = ("Bad sentence with ", toxicityOfWord, "toxicity ratio",
                    " Avg toxicity =", averageToxicity)
        else:
            result = ("Good sentence with ", toxicityOfWord, "toxicity ratio",
                    " Avg toxicity = ", averageToxicity)
        byBus = Voting.analyse_by_bus(sampleSplit)
        if byBus is not None:
            result = ("Bad sentence with ", byBus, "toxicity ratio",
                    " By local")
        return result



    @staticmethod
    def analyse_by_bus(sampleSplit):   # method will be refactored (by using checking_toxicity_from_one_bus(sampleSplit)
        #sample = sample.split(' ')
        dict_of_buses = {}         # not sure if we need it
        counter, modulo = 0, 0

        if len(sampleSplit) % 3 == 1: modulo = 1
        elif len(sampleSplit) % 3 == 2: modulo = 2

        for i in range(0, len(sampleSplit) - modulo, 3):
            tmp = []
            tmp.extend((sampleSplit[i], sampleSplit[i+1], sampleSplit[i+2]))
            for j in range(len(tmp)):
                if not toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == tmp[j]].empty:
                    counter += float(toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == tmp[j], '0'].item())
            #print(tmp) # to remove
            if counter > 0.69:   # static threshold to be replaced with heuristic
                return counter
            else:
                counter = 0
        if modulo == 1:
            print('modulo1')
            if not toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[-1]].empty:
                counter += float(toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[-1], '0'].item())
            if counter > 0.69:  # static threshold to be replaced with heuristic
                return counter
        if modulo == 2:
            print('modulo2')
            for k in range(1, 3):
                if not toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[-k]].empty:
                    counter += float(toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[-k], '0'].item())
            if counter > 0.69:  # static threshold to be replaced with heuristic
                return counter

    """@staticmethod    # to improve
    def checking_toxicity_from_one_bus(sampleSplit):
        if not toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit].empty:
            return float(toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit, '0'].item())
        else: return 0"""


toxicitySeries = pd.read_csv('savedWord.csv')



#small tests
sample = 'i love hamburger'
sample2 = 'i am really proud of you however i want to love you you honey'
sample3 = 'i am really proud of you'
sample4 = 'fuck'

#print(Voting.analyse_by_bus(sample2))

print("Vulgarity factor: {}\n".format(Voting.voting(sample2)))
print("Vulgarity factor: {}\n".format(Voting.voting(sample2)))
print("Vulgarity factor: {}\n".format(Voting.voting(sample3)))
print("Vulgarity factor: {}\n".format(Voting.voting(sample4)))


"""
TODO
bybus - lokalne średnie #FINISHED
obliczanie treshholdów - trzy treshholdy na sztywno #FINISHED

Średnioterminowo 
obliczanie treshholdów - heurystyka
zmiana lokalnych busów - np na 4, na 5, na 2

Długoterminowo:
speech to text - zamiana mowy na tekst i sprawdzenie toksyczności (do poszerzenia programu)

"""

