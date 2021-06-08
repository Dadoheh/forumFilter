from tkinter import *
import pandas as pd

window = Tk()
window.geometry("800x800")
window.title(" Commentary filter ")

class Voting:
    toxicitySeries = pd.read_csv('savedWord.csv')

    @staticmethod
    def voting(sampleSplit):
        toxicitySeries = pd.read_csv('savedWord.csv')
        averageToxicity = 0.72  # = toxicitySeries.mean()
        counter = 0
        if type(sampleSplit) is not list:
            sampleSplit = (sampleSplit.split(' '))
        lenSampleSplit = len(sampleSplit)
        wrong = 0
        for i in range(len(sampleSplit)):
            if not toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[i]].empty:
                counter += float(toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[i], '0'].item())
            else:
                lenSampleSplit -= 1  # setting unknown word as not important
                wrong += 1

        toxicityOfWord = counter / lenSampleSplit

        if toxicityOfWord > averageToxicity:
            #result = ("Bad sentence with ", toxicityOfWord, "toxicity ratio",
                      #" Avg toxicity =", averageToxicity)
            result = [False, toxicityOfWord]
        else:
            #result = ("Good sentence with ", toxicityOfWord, "toxicity ratio",
                      #" Avg toxicity = ", averageToxicity)
            result = [True, toxicityOfWord]
        byBus = Voting.analyse_by_bus(sampleSplit)
        if byBus is not None:
            #result = ("Bad sentence with ", byBus, "toxicity ratio",
                      #" By local")
            result = [False, toxicityOfWord]
        return result

    @staticmethod
    def analyse_by_bus(sampleSplit):  # method will be refactored (by using checking_toxicity_from_one_bus(sampleSplit)
        # sample = sample.split(' ')
        toxicitySeries = pd.read_csv('savedWord.csv')
        counter, modulo = 0, 0

        if len(sampleSplit) % 3 == 1:
            modulo = 1
        elif len(sampleSplit) % 3 == 2:
            modulo = 2

        for i in range(0, len(sampleSplit) - modulo, 3):
            tmp = []
            tmp.extend((sampleSplit[i], sampleSplit[i + 1], sampleSplit[i + 2]))
            for j in range(len(tmp)):
                if not toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == tmp[j]].empty:
                    counter += float(toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == tmp[j], '0'].item())
            # print(tmp)                                     # to remove
            if counter > 0.69:  # static threshold to be replaced with heuristic
                return counter
            else:
                counter = 0
        if modulo == 1:
            if not toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[-1]].empty:
                counter += float(toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[-1], '0'].item())
            if counter > 0.69:  # static threshold to be replaced with heuristic
                return counter
        if modulo == 2:
            for k in range(1, 3):
                if not toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[-k]].empty:
                    counter += float(
                        toxicitySeries.loc[toxicitySeries['Unnamed: 0'] == sampleSplit[-k], '0'].item())
            if counter > 0.69:  # static threshold to be replaced with heuristic
                return counter


def result(textIn, listBox):  # odpowiedzialne za wyswietlenie wyniku

    review = textIn.get("1.0", "end-1c")
    #print(review)
    global outcome

    result = (Voting.voting(review))

    #result = False # zmienna reprezentujaca czy recenzja jest pozytywna czy negatywna

    if (result[0] == False):
        outcome = f"{review} - Negative - {round(result[1],2)} toxicity ratio"
    else:
        outcome = f"{review} - Positive - {round(result[1],2)} toxicity ratio"
    listBox.insert(END, outcome)


def gui():
    label = Label(text="Type text:", font=("Arial", 20))

    inputTXT = Text(window, height=25,
                    width=50,
                    bg="light cyan")

    Display1 = Button(window,
                     text="Show", font=("Arial", 15),  # tu jako nazwa przycisku, nazwa metody
                     command=lambda: result(inputTXT, lBox))

    lBox = Listbox(window, width=45, height=7, font=("Arial", 15))  # tworzę kontrolkę listbox

    label.pack()
    inputTXT.pack()
    Display1.pack()
    lBox.pack()

    #Display1.place(bordermode=OUTSIDE, x='360', y='500', height=40, width=70)

gui()
mainloop()
