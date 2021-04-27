class Voting:

    @staticmethod
    def voting(sampleSplit, threshold):
        averageToxicity = threshold  # = toxicitySeries.mean()
        counter = 0
        if type(sampleSplit) is not list:
            sampleSplit = (sampleSplit.split(' '))
        lenSampleSplit = len(sampleSplit)
        print("lenOfSampleSplit {}".format(len(sampleSplit)))             # to remove
        wrong = 0
        for i in range(len(sampleSplit)):  # need to find a better way to looking frames (maybe 5-7?)
            if not toxicitySeries.loc[toxicitySeries['words'] == sampleSplit[i]].empty:
                counter += float(toxicitySeries.loc[toxicitySeries['words'] == sampleSplit[i], 'values'].item())
            else:
                lenSampleSplit -= 1  # setting unknown word as not important
                wrong += 1
        toxicityOfWord = counter/lenSampleSplit
        if toxicityOfWord > averageToxicity:
            result = ("Bad sentence with ", toxicityOfWord, "toxicity ratio",
                    " Avg toxicity =", averageToxicity)
            badBool = True
        else:
            result = ("Good sentence with ", toxicityOfWord, "toxicity ratio",
                    " Avg toxicity = ", averageToxicity)
            badBool = False
        byBus = Voting.analyse_by_bus(sampleSplit)
        if byBus is not None and byBus > threshold/3:
            print("toxicyby byBus: {} ".format(byBus))
            result = ("Bad sentence with ", byBus, "toxicity ratio",
                    " By local")
        #print("wrong",wrong)
        return result, badBool


    @staticmethod   # to factorise - DRY
    def analyse_by_bus(sampleSplit):
        counter = 0
        modulo = len(sampleSplit) % 3
        for i in range(0, len(sampleSplit) - modulo, 3):
            tmp = []
            tmp.extend((sampleSplit[i], sampleSplit[i + 1], sampleSplit[i + 2]))
            for j in range(len(tmp)):
                counter += Voting.checking_toxicity_from_one_bus(sampleSplit, j)
        if modulo == 1:
            print('modulo1')  # to remove
            counter += Voting.checking_toxicity_from_one_bus(sampleSplit, -1)  # the last word from the list
            #return counter
        if modulo == 2:
            print('modulo2')  # to remove
            for k in range(1, 3):
                counter += Voting.checking_toxicity_from_one_bus(sampleSplit, -k)  # two last words from the list
        return counter/len(sampleSplit)


    @staticmethod
    def checking_toxicity_from_one_bus(sampleSplit, iterator):
        if not toxicitySeries.loc[toxicitySeries['words'] == sampleSplit[iterator]].empty:
            return float(toxicitySeries.loc[toxicitySeries['words'] == sampleSplit[iterator], 'values'].item())
        else:
            return 0


toxicitySeries = pd.read_csv('savedWord.csv')
toxicitySeries = toxicitySeries.rename(columns={'Unnamed: 0': 'words', '0': 'values'})
#print(toxicitySeries.head(10), "\n")


#small tests (taken from CalculateToxicity.py (framesWithLocals.py/voting.py)
"""
sample = 'i love hamburgers'
sample2 = "In my opinion it's not about being good or not good. If I were to say what I esteem the most in life, I would say - people. People, who gave me a helping hand when I was a mess, when I was alone. And what's interesting, the chance meetings are the ones that influence our lives. The point is that when you profess certain values, even those seemingly universal, you may not find any understanding which, let me say, which helps us to develop. I had luck, let me say, because I found it. And I'd like to thank life. I'd like to thank it - life is singing, life is dancing, life is love. Many people ask me the same question, but how do you do that? where does all your happiness come from? And i replay that it's easy, it's cherishing live, that's what makes me build machines today, and tomorrow... who knows, why not, i would dedicate myself to do some community working and i would be, wham, not least... planting .... i mean... carrots."
sample3 = 'fuck head limey vandal'
sample4 = "Why these fucking made under my username Hardcore my Fan were reverted? tits weren't vandalisms, just closure on some GAs after I voted at New York Dolls FAC. And please don't remove the template from the talk page since I'm retired now"


print("Sentence: {}\nVulgarity factor: {}\n".format(sample, framesWithLocals.Voting.voting(sample.lower(),threshold=0.2)))
print("Sentence: {}\nVulgarity factor: {}\n".format(sample2, framesWithLocals.Voting.voting(sample2.lower())))
print("Sentence: {}\nVulgarity factor: {}\n".format(sample3, framesWithLocals.Voting.voting(sample3.lower())))
print("Sentence: {}\nVulgarity factor: {}\n".format(sample4, framesWithLocals.Voting.voting(sample4.lower())))
"""
