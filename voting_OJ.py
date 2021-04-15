import pandas as pd

class analiza_ator:
    @staticmethod
    def split_comment(x):
        val = [word.strip(':,;"-_·()[]{}\n?!@|.') for word in x.split()]
        return val
    @staticmethod
    def calc_mean(lst,dictionary):
        sum=0
        for i in range(len(lst)):
            for j in dictionary.index:
                if dictionary.iloc[j][0]==lst[i]:
                    sum=sum+dictionary.iloc[j][1]
                    break;
        return sum/len(lst)
    @staticmethod
    def analyse_byMean(comment,dictionary):
        lst=analiza_ator.split_comment(comment)
        return analiza_ator.calc_mean(lst,dictionary)
    @staticmethod
    def analyse_byBus(comment,dictionary):
        lst=analiza_ator.split_comment(comment)
        max=0
        if len(lst)<3:
            max=analiza_ator.calc_mean(lst,dictionary)
        for i in range(len(lst)-2):
            tmp=analiza_ator.calc_mean(lst[i:i+2],dictionary)
            if tmp>max:
                max=tmp
        return max
    @staticmethod
    def decide(mean,bus):
        if mean>0.23:
            return "Toksyczne"
        if bus>0.69:
            return "Toksyczne"
        if mean>0.14:
            if bus>0.50:
                return "Toksyczne"
        return "Nietoksyczne"
    @staticmethod
    def stats(comment,dictionary):
        mean=analiza_ator.analyse_byMean(comment,dictionary)
        bus=analiza_ator.analyse_byBus(comment,dictionary)
        print("Komentarz:",comment)
        print("Toksycznosc wg sredniej:",mean)
        print("Toksycznosc wg max-local:",bus)
        print("Werdykt:",analiza_ator.decide(mean,bus))

frame=pd.read_csv('savedWord.csv')

analiza_ator.stats("i am really proud of you however i want to fuck you",frame)

