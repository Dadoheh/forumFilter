import pandas as pd
#import re


class DataCreating:
    @staticmethod
    def create_data():  # 280 k records processed within 2 hours :D
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
        print("Length of a dictionary {}".format(len(dictionary)))
        toxicitySeries.to_csv('savedWord.csv')
        return toxicitySeries


class Voting:

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
        if byBus is not None and byBus > 0.6:
            print(byBus)
            result = ("Bad sentence with ", byBus, "toxicity ratio",
                    " By local")

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
            counter /= 2    # it's okay only at this moment - we need to improve the counters and thresholds
            if counter > 0.69:
                return counter
        if modulo == 0:
            print('modulo0')
            #return counter
        if modulo == 1:
            print('modulo1')
            counter += Voting.checking_toxicity_from_one_bus(sampleSplit, -1)  # the last word from the list
            if counter > 0.69:
                return counter
        if modulo == 2:
            print('modulo2')
            for k in range(1, 3):
                counter += Voting.checking_toxicity_from_one_bus(sampleSplit, -k)  # two last words from the list
            if counter > 0.69:
                return counter


    @staticmethod
    def checking_toxicity_from_one_bus(sampleSplit, iterator):
        if not toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[iterator]].empty:
            return float(toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[iterator], '0'].item())
        else: return 0


toxicitySeries = pd.read_csv('savedWord.csv')


#small tests

sample2 = 'love you hamburgers much'
sample3 = 'im gonna guess you are the same bigoted non normal that wrote this hate page in the first place. you and your gay friends are all pedophiles'
sample4 = "Regarding her daughter's death, much was made in Great Barrier that Nicole had murdered the child, hence the broken neck and forcibly twisted arm being mentioned. Later much was made about the child being murdered, and Nicole's flippant remarks to Goren about """"accidents"""" seemed to confirm she did murder the child. Given the information in  the episode, I think saying it might have been an accident is reaching"
sample = "In my opinion it's not about being good or not good. If I were to say what I esteem the most in life, I would say - people. People, who gave me a helping hand when I was a mess, when I was alone. And what's interesting, the chance meetings are the ones that influence our lives. The point is that when you profess certain values, even those seemingly universal, you may not find any understanding which, let me say, which helps us to develop. I had luck, let me say, because I found it. And I'd like to thank life. I'd like to thank it - life is singing, life is dancing, life is love. Many people ask me the same question, but how do you do that? where does all your happiness come from? And i replay that it's easy, it's cherishing live, that's what makes me build machines today, and tomorrow... who knows, why not, i would dedicate myself to do some community working and i would be, wham, not least... planting .... i mean... carrots."
#print(Voting.analyse_by_bus(sample2))


print("Sentence: {}\nVulgarity factor: {}\n".format(sample2, Voting.voting(sample2)))
print("Sentence: {}\nVulgarity factor: {}\n".format(sample3, Voting.voting(sample3)))
print("Sentence: {}\nVulgarity factor: {}\n".format(sample4, Voting.voting(sample4)))
print("Sentence: {}\nVulgarity factor: {}\n".format(sample, Voting.voting(sample)))

#this counters version should be changed

#TODO
"""
bybus - lokalne średnie #FINISHED
obliczanie treshholdów - trzy treshholdy na sztywno #FINISHED

Średnioterminowo 
obliczanie treshholdów - heurystyka
zmiana lokalnych busów - np na 4, na 5, na 2

Długoterminowo:
speech to text - zamiana mowy na tekst i sprawdzenie toksyczności (do poszerzenia programu)
translacja na język polski - np google tłumacz plugin
"""

