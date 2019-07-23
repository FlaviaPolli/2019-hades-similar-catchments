import pandas as pd
import numpy as np

###Import data
data_200 = pd.read_csv("/Users/Flavia/PycharmProjects/projectHADES/Einzugsgebiete_200m.csv", sep=";")
#print(data_200)


##################### Auswahl durch USER ######################

#ID auswählen
#featureID = int(input("Choose your feature ID: "))
#print("You choose the id" + " " + str(featureID))
featureID = 109342

###Auswahl Quantils durch Benutzer
#quantile = int(input("Choose your quantile: "))
quantile = 4

###################################################################

criteriachosenbyuser = ('mH_04','N20slp8_12')

###Berechnung Quantile der ausgewählten Kriterien
for x in criteriachosenbyuser:
    data_200['Quantile_rank_'+ str(x)] = pd.qcut(data_200[x], quantile, labels=False)
print(data_200)

###Zeile der ausgesuchten id extrahieren
chosenID = data_200.loc[data_200.id==featureID, : ]
print(chosenID)


############################# Hilfe von Andreas #################################

quantilliste=[]
for x in criteriachosenbyuser:
    ###Gib die Quantile der ausgewählten ID aus (der ausgewählten Kriterien)
    quantilliste.append(chosenID['Quantile_rank_'+ str(x)].iloc[0])

#Totale Anzahl an Zeilen ausgeben
total_rows = data_200.shape[0]
print(total_rows)

#durch alle Zeilen durchitterieren mit einer while-Schlaufe:
ergebnisliste=[]
i=0
while i < total_rows:
    tempquantilliste=[]
    for x in criteriachosenbyuser:
        #Quantile der gerade prozessierenden Zeile auswählen (und in die Liste 'tempquantilliste' speichern)...
        tempquantilliste.append(int(data_200.iloc[i]['Quantile_rank_' + str(x)]))
        # ...wenn die Quantile mit den Quantilen der vom User ausgewählten ID ('quantilliste') übereinstimmen,
        # und in die Liste 'ergebnisliste' speichern
        if quantilliste == tempquantilliste:
            ergebnisliste.append(data_200.iloc[i]['id'])
    i += 1

print(ergebnisliste)

######################### alter Versuch mit Dictionary ##############################

d = {}
e = {}
for x in criteriachosenbyuser:
    ###Gib das Quantil der ausgewählten ID aus (der ausgewählten Kriterien)
    d['Q_' + str(x)] = chosenID['Quantile_rank_'+ str(x)].iloc[0]
    print("The attribute ...{}... of the chosen catchment is in the {} Quantile." .format(str(x), str(d['Q_' + str(x)])))

    ###wähle alle IDs mit dem selben Quantil bei den ausgewählten Kriterien aus
    e[str(x) + '_sameq'] = list(data_200.loc[data_200['Quantile_rank_'+ str(x)]==d['Q_' + str(x)], 'id'])
    print('regarding the criteria ...{}... the following catchments are similar (in the same quantile): \n {} \n' .format(str(x), e[str(x) + '_sameq']))

print(e)

#### dictionary umformatieren um intersection zum laufen zu bringen :( #####################

# convert dictionary "e" to a Numpy Dataframe
df = pd.DataFrame({k:pd.Series(v) for k,v in e.items()}).T
print(df)
#oder:      df = pd.DataFrame(list(e.values()), index=e.keys())


### change rows & columns in the DataFrame
df = df.transpose()
print(df)

##################### create an intersection of all the arrays in the Dataframe ##################

from functools import reduce
result = reduce(np.intersect1d, [df])

#result = set.intersection(*map(set,df))
#result = list(reduce(set.intersection, [set(item) for item in df]))

#for x in criteriachosenbyuser:
#    df['C'] = [len(set(a).intersection(b)) for a, b in zip(e.str(x) + '_sameq')]

###################################################################################################

print('\033[1m' + "the following catchments are similar to your chosen catchment {} "
                  "in regard to the middle hight(mH_04) and the slope(N20slp8_12) as well as your quantile {}:"
                 .format(featureID, quantile))
print(result)
#'\033[0m'

