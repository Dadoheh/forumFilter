import pandas as pd

class TrainDB:
    @staticmethod
    def toxicBoardToTraining(toxicBoardToTraining, listOfQueries, quantity):
        appender = train.query(listOfQueries).head(quantity)
        toxicBoardToTraining = toxicBoardToTraining.append(appender)
        return(toxicBoardToTraining)


toxicitySeries = pd.read_csv('savedWord.csv')
toxicitySeries = toxicitySeries.rename(columns={'Unnamed: 0': 'words', '0': 'values'})
train = pd.read_csv('train.csv')

#findingThersholds = toxicitySeries.query('values > 0.28 and values < 0.74')  # this section will be checked

#rules
listOfQueries = ["(toxic>0 or severe_toxic>0) or (obscene>0 or threat>0) or (insult>0 or identity_hate>0)",
                  "(toxic>0 and severe_toxic>0) or (obscene>0 and threat>0) or (insult>0 and identity_hate>0)",
                 "(toxic>0 and severe_toxic>0 and obscene>0) or (threat>0 and insult>0 and identity_hate>0)",
             "toxic == 0 and severe_toxic == 0 and obscene == 0 and threat ==0 and insult == 0 and identity_hate == 0"]

listOfQuantity = [200, 200, 200, 400]   # may change 2 lists into 1 dict?

toxicBoardToTraining = pd.DataFrame(columns=['id', 'comment_text', 'toxic', 'severe_toxic', 'obscene', 'threat', 'insult'
                                             , 'identity_hate'])

for i in range(len(listOfQueries)):
    toxicBoardToTraining = TrainDB.toxicBoardToTraining(toxicBoardToTraining, listOfQueries[i], listOfQuantity[i])

print(toxicBoardToTraining)
toxicBoardToTraining.to_csv('toxicBoardToTraining.csv')



#TODO
# wybierz binarnie wartość z przedziału 'values > 0.20 and values < 0.80'
# sprawdź zgodność dla małej bazy (tysiąc komentarzy)
# potrzeba oddzielenia bazy tysiąca komentarzy (60% negatywnych, 40% pozytywnych)
# każde sprawdzenie zapisz do słownika - wybrany_thershold : accurancy
# wybierz maksymalną wartość

