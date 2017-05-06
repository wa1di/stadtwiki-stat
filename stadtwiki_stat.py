import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from bs4 import BeautifulSoup
import urllib.request

#Einlesen der HTML Daten aus der Webseite in filedata

with urllib.request.urlopen('https://ka.stadtwiki.net/Stadtwiki:Meilensteine') as response:
   filedata = response.read()
   
filedata = str(filedata)


#Vereinheitlichung relevanter Stellen
filedata = filedata.replace("\\xc2\\xa0", " ")
filedata = filedata.replace("<b>","")
filedata = filedata.replace("</b>","")
filedata = filedata.replace(". Artikel"," Artikel")
filedata = filedata.replace("&nbsp;", " ")
filedata = filedata.replace("%C3%A4", "ä")
filedata = filedata.replace("  ", " ")

#soup als Variable, mit der BeautifulSoup arbeitet
soup = BeautifulSoup(filedata, 'html.parser')

#Erstellung von 2d-Liste JahrDat wie folgt: [Position, 'Jahreszahl']
JahrDat = []
for i in range ( 1, len(soup.find_all('h3'))-1 ):
    if str(soup.find_all('h3')[i]).startswith("<h3><span class=\"mw-headline\""):
        JahrDat.append([filedata.find(str(soup.find_all('h3')[i])), soup.find_all('h3')[i].get_text()])
JahrDat.append([len(filedata),'end'])

#Erstellung 2d-Liste DatArt mit ['Datum', Artikel]
Dat = []
Art = []
DatArt = []
for i in range( 0, len(soup.find_all('li'))-1 ):
        
    if(len(soup.find_all('li')[i].get_text().split())>2):
        test_a = filedata.find( soup.find_all('li')[i].get_text().split()[0] + " " + soup.find_all('li')[i].get_text().split()[1] ) #Extraktion von Datum und Artikelzahl, mit Leerzeichen separiert
        test_c = soup.find_all('li')[i].get_text().split()[2] 
    else:
        test_c = ""
        test_a = "-1"
    if(test_c.startswith("Artikel")): #um zu überprüfen, ob auch alle Datensätze als drittes Wort "Artikel" stehen haben
        
            for j in range(0, len(JahrDat)-1):
                if(test_a>JahrDat[j][0] and test_a < JahrDat[j+1][0]): 
                       tmp_a = soup.find_all('li')[i].get_text().split()[0][:-1]+JahrDat[j][1] #extrahiertes Datum mit Jahreszahl darüber kombinieren
                
            tmp_b = int(soup.find_all('li')[i].get_text().split()[1].replace(".","")) #Punkte aus Artikelzahlen entfernen
            Dat.extend([tmp_a])
            Art.extend([tmp_b])
            
Dat.extend(['22.07.2004']) #Festes Datum der Erstellung des Wikis
Art.extend([0])
DatArt.append(Dat) # DatArt[0] als Datum-Liste
DatArt.append(Art) # DatArt[1] als Artikelanzahlliste

# Abbildung der extrahierten Daten           
x = [dt.datetime.strptime(d,'%d.%m.%Y').date() for d in DatArt[0]]
y = DatArt[1]
plt.plot(x,y)
plt.grid(linestyle="dotted")
plt.xlabel('Datum')
plt.ylabel('Artikel')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
plt.show()
