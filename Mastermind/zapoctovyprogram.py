"""
Hra Logik 
Martin Kliment, Praha, MFF UK, Obecna matematika, Bakalarske studium, 1. rocnik
Letny semester 2022/2023
Programovani 2
"""

#generujeme pociatocne pole rekurzivnym generovanim
def generujpole(pozicie, farby, vysl):
    """
    pozicie - kolko prvkov ma hladana postupnost
    farby - kolko je farieb ktore sa pouzivaju
    vysl - premenna ktoru tvorime a ak ma dostatocnu dlzku pridame do pola
    """
    if len(vysl) == pozicie:
        pole.append(vysl.copy())
        return
    for i in range(1, farby+1):
        vysl.append(i)
        generujpole(pozicie, farby, vysl)
        vysl.pop()
    return

#odstranime nevyhovujuce
def odstrannevyhovujuce(pozicie, farby, pole, kombinacia, odpoved):
    """
    pozicie - kolko prvkov ma hladana postupnost
    farby - kolko je farieb ktore sa pouzivaju
    pole - je pole vsetkych moznych kombinacii vygenerovaneho hore pripadne skresane uz nejakymi krokmi
    kombinacie - je kombinacia ktoru program hadal a na ktoru dostaval odpoved
    odpoved - odpoved pouzivatela na danu kombinaciu je to konkretne zoznam kde odpoved[0] znaci pocet zhod vo farbach a odpoved[1] pocet zhod vo farbach aj poziciach
    """
    novepole = []
    #mame nejaku kombinaciu a zratame vyskyt jednotlivych farieb v nej
    vyskytodpoved = [0]*farby
    for i in range(pozicie):
        vyskytodpoved[kombinacia[i]-1] += 1
    #prejdeme postupne vsetky prvky pola
    for skusana in pole:
        #opat obdobne ako pri vstupnej kombinacii pre ne zratame pocet vyskytov jednotlivych farieb
        vyskytskusana = [0]*farby
        for j in range(pozicie):
            vyskytskusana[skusana[j]-1] += 1
        count = 0
        #zratame pocet zhod vo farbach
        for j in range(farby):
            count += min(vyskytodpoved[j],vyskytskusana[j])
        #ak je rovny odpoved[0] teda pozadovanemu poctu tak overime ci sedi aj druha podmienka a ak ano pridame tuto kombinaciu do novepole
        if count == odpoved[0]:
            count = 0
            for j in range(pozicie):
                if skusana[j] == kombinacia[j]:
                    count += 1
            if count == odpoved[1]:
                novepole.append(skusana)
    #novepole je teda uz len pole kombinacii ktore pripadaju v uvahu, tie ktore po predoslej odpovedi nie su mozne sme vyradili
    pole = novepole
    return pole

#naprogramujeme si minimax na zaklade ktoreho budeme skusat kombinacie
def minimax(pozicie, farby, x ,pole):
    """
    pozicie - kolko prvkov ma hladana postupnost
    farby - kolko je farieb ktore sa pouzivaju
    x - pole vsetkych moznosti ak je ale prilis velke tak ho musime zmensovat(re prilis velke polia je minimax nevyhodny to pozerame aj nakonci uz pri samotnom kode)
    pole - je pole vsetkych kombinacii ktore po predoslych odpovediach este stale prichadzaju do uvahy resp. mozu nastat
    """
    #ak je pole vsetkych moznosti prilis velke tak ho okresame aby nam program isiel rychlejsie
    if len(x) > 2000:
        x = pole.copy()
    #zjavne v najhorsom pripade bude skore len(pole), skore vyjadruje kolko prvkov zostane v poli pri najhorsej moznej odpovedi 
    naj = [len(pole), []]
    #pre kazdu kombinaciu v poli overime kolko prvkov by ostalo v poli pre vsetky mozne odpovede a vyberieme tu najhorsiu
    for kombinacia in x:
        skore = 0
        for i in range(pozicie+1):
            for j in range(i+1):
                pomocnepole = odstrannevyhovujuce(pozicie, farby, pole, kombinacia, [i, j])
                skore=max(skore, len(pomocnepole))
        #vyberame tu pre ktoru zostane v najhorsom pripade najmenej prvkov teda ma najlepsie skore a preferujeme kombinaciu z pola moznych kombinacii a nie vsetkych(teda kombinaciu z pole pred kombinaciou z x)
        if naj[0]>skore or (naj[0]==skore and naj[1] not in pole and kombinacia in pole):
            naj[0], naj[1] = skore, kombinacia
    #vraciame kombinaciu na ktoru sa je naidealnejsie spytat
    return naj[1]


print("Ahoj, tento program ti pomoze uhadnut kombinaciu v hre logik(podobna wordle).")
print("Nasjkor mi povedz rozmery tvojej hry.")
print("Pre velke cisla moze byt uzivatelovi obtiazne davat spravne odpoevede!!!")
print("")

#ziskame pociatocne informacie
pozicie = int(input("Pocet pozicii(cele cislo vacsie rovne 1):"))
farby = int(input("Pocet farieb(cele cislo vacsie rovne 1):"))
hladana = int(input("Napiste kombinaciu farieb,ktoru ma  program uhadnut(teda tolko ciferne cislo kolko je pozicii a na kazdom cifra z rozsahu 1 az pocet farieb):"))
print("")

#vygenerujeme cel pole
pole = []
generujpole(pozicie, farby, [])
celepole = pole.copy()

#vyuzijeme poznatok Knutha o tom aku kombinaciu je idealne hladat ako prvu
prvypokus, i = [], 0
while len(prvypokus)<pozicie:
    if len(prvypokus)%2==0:
        i+=1
    if i > farby:
        i = 1
    prvypokus.append(i)

#pomocou vytvorenych funkcii najdeme odpoved
print("Hádam kombináciu:","".join(map(str,prvypokus)))
odpoved = [int(i) for i in input("Zadaj odpoved v spravnom tvare(pocet uhadnutych farieb medzera pocet uhadnutych farieb aj pozicii):").split()]
pokus = prvypokus
while odpoved != [pozicie, pozicie]:
    pole = odstrannevyhovujuce(pozicie, farby, pole, pokus, odpoved)
    if len(pole) == 0:
        print("Pri zadavani odpovedi ste sravili chybu")
        break
    #pre vacsie polia je minimax neoptimalny na to si musime davat pozor
    if len(celepole) < 2000:
        pokus = minimax(pozicie, farby, celepole, pole)
    else:
        celepole = pole
        pokus = pole[0]        
    print("Hádam kombináciu:","".join(map(str,pokus)))
    odpoved = [int(i) for i in input("Zadaj odpoved v spravnom tvare(pocet uhadnutych farieb medzera pocet uhadnutych farieb aj pozicii):").split()]
#vyprintujeme najdenu odoved ak uzivatel nespravil chybu
if len(pole)>0:
    print("Odpoved je:","".join(map(str,pokus)))
