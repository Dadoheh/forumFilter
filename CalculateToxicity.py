import pandas as pd

class Voting:

    @staticmethod
    def voting(sampleSplit):
        averageToxicity = 0.72  # = toxicitySeries.mean()
        counter = 0
        if type(sampleSplit) is not list:
            sampleSplit = (sampleSplit.split(' '))
        lenSampleSplit = len(sampleSplit)
        print(len(sampleSplit))             # to remove
        #print("co to jest", sampleSplit)    # to remove
        wrong = 0
        for i in range(len(sampleSplit)):  # need to find a better way to looking frames (maybe 5-7?)
            if not toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[i]].empty:
                counter += float(toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[i], '0'].item())
            else:
                lenSampleSplit -= 1  # setting unknown word as not important
                #print('sth wrong (1)')
                wrong += 1

        toxicityOfWord = counter/lenSampleSplit

        if toxicityOfWord > averageToxicity:
            result = ("Bad sentence with ", toxicityOfWord, "toxicity ratio",
                    " Avg toxicity =", averageToxicity)
        else:
            result = ("Good sentence with ", toxicityOfWord, "toxicity ratio",
                    " Avg toxicity = ", averageToxicity)
        byBus = Voting.analyse_by_bus(sampleSplit)
        if byBus is not None and byBus > 0.3:
            print(byBus)
            result = ("Bad sentence with ", byBus, "toxicity ratio",
                    " By local")
        #print("wrong",wrong)
        return result


    @staticmethod
    def analyse_by_bus(sampleSplit):   # method will be refactored (by using checking_toxicity_from_one_bus(sampleSplit)
        #sample = sample.split(' ')
        dict_of_buses = {}         # not sure if we need it
        counter = 0
        modulo = len(sampleSplit) % 3

        for i in range(0, len(sampleSplit) - modulo, 3):
            tmp = []
            tmp.extend((sampleSplit[i], sampleSplit[i + 1], sampleSplit[i + 2]))
            for j in range(len(tmp)):
                counter += Voting.checking_toxicity_from_one_bus(sampleSplit, j)
        if modulo == 0:
            print('modulo0')
            #return counter
        if modulo == 1:
            print('modulo1')
            counter += Voting.checking_toxicity_from_one_bus(sampleSplit, -1)  # the last word from the list
            #return counter
        if modulo == 2:
            print('modulo2')
            for k in range(1, 3):
                counter += Voting.checking_toxicity_from_one_bus(sampleSplit, -k)  # two last words from the list
        return counter/len(sampleSplit)


    @staticmethod
    def checking_toxicity_from_one_bus(sampleSplit, iterator):
        if not toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[iterator]].empty:
            return float(toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[iterator], '0'].item())
        else:
            return 0
            #print('sth wrong (1)')


toxicitySeries = pd.read_csv('Dictionary.csv')
