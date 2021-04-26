import pandas as pd
import numpy as np
import CalculateToxicity

#main training and checking class
class TrainDB:
    @staticmethod
    def toxicBoardToTraining(toxicBoardToTraining, listOfQueries, quantity):
        appender = train.query(listOfQueries).head(quantity)
        toxicBoardToTraining = toxicBoardToTraining.append(appender)
        toxicBoardToTraining = toxicBoardToTraining.set_index(pd.Index([k for k in range(len(toxicBoardToTraining))]))
        return(toxicBoardToTraining)


    @staticmethod
    def checkingPotentialThres():
        potentialThreshold = list(np.arange(0.20, 0.86, 0.06))
        potentialThreshold
        bestThresholds = {}
        badCom = 0
        for j in range(len(toxicBoardToTraining) - 1):
            sample = toxicBoardToTraining['comment_text'][j]
            print(
                "Sentence: {}\nVulgarity factor: {}".format(sample, framesWithLocals.Voting.voting(sample.lower(),
                                                                                                potentialThreshold[0])))
            if toxicBoardToTraining['toxic'][j] > 0:
                badCom += 1
                print("BAD_FORMAT############{}####\n\n".format(badCom))
            accuracy = badCom / len(toxicBoardToTraining)
            print("ACCURACY############{}####".format(accuracy))

            # TODO #change if statement
            # TODO (if 1 in toxic/severe_toxic... then sentence is bad
            # TODO so if the return bad is also bad [:)] then badCom += 1
            # TODO finally check the accuracy (badCom/len(toxicBoardTr..)

# file reading
toxicitySeries = pd.read_csv('savedWord.csv')
toxicitySeries = toxicitySeries.rename(columns={'Unnamed: 0': 'words', '0': 'values'})
train = pd.read_csv('train.csv')


#rules
listOfQueries = ["(toxic>0 or severe_toxic>0) or (obscene>0 or threat>0) or (insult>0 or identity_hate>0)",
                  "(toxic>0 and severe_toxic>0) or (obscene>0 and threat>0) or (insult>0 and identity_hate>0)",
                 "(toxic>0 and severe_toxic>0 and obscene>0) or (threat>0 and insult>0 and identity_hate>0)",
             "toxic == 0 and severe_toxic == 0 and obscene == 0 and threat ==0 and insult == 0 and identity_hate == 0"]
listOfQuantity = [200, 200, 200, 400]   # may change 2 lists into 1 dict?
toxicBoardToTraining = pd.DataFrame(columns=['id', 'comment_text', 'toxic', 'severe_toxic', 'obscene', 'threat', 'insult'
                                             , 'identity_hate'])

#setting training csv
for i in range(len(listOfQueries)):
    toxicBoardToTraining = TrainDB.toxicBoardToTraining(toxicBoardToTraining, listOfQueries[i], listOfQuantity[i])
#toxicBoardToTraining.to_csv('toxicBoardToTraining.csv')        # to csv
print(toxicBoardToTraining)


TrainDB.checkingPotentialThres()



#TODO
# wybierz binarnie wartość z przedziału 'values > 0.20 and values < 0.80' - finished
# sprawdź zgodność dla małej bazy (tysiąc komentarzy) - finished
# potrzeba oddzielenia bazy tysiąca komentarzy (60% negatywnych, 40% pozytywnych) - finished
# stwórz listę wartości potencjalnych thresholdów range(0.20,0.80,0.6 step)
# oblicz accurancy dla podanej wartości z listy
# każde sprawdzenie zapisz do słownika - wybrany_thershold : accurancy
# wybierz maksymalną wartość

