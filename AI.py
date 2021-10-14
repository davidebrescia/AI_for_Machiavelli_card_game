from copy import deepcopy


def controllaComb(carte, scala):
    if len(carte) <= 2:
        return 0
    if scala == 0:
        carte.sort(key=lambda i: i.sem) #i semi uguali li mette vicini
        for i in range(len(carte)-1):
            if (carte[i].val != carte[i+1].val) or (carte[i].sem == carte[i+1].sem): #se ha i valori disuguali o i semi uguali, non va bene
                return 0
    else:
        carte = ordina_val(carte) #riordina dal più piccolo al più grande
        for i in range(len(carte)-1):
            if (not checkValScala(carte[i].val, carte[i+1].val)) or (carte[i].sem != carte[i+1].sem):
                return 0
    return 1


def ordina_val(carte):
    carte.sort(key=lambda i: i.val)
    if (carte[0].val == 1) and (carte[len(carte)-1].val == 13):  #se la prima carta è 1, l'ultima è il king, metti l'asso dopo il king
        carte.append(carte[0])
        del(carte[0])
    return carte


def checkValScala(valCarta1, valCarta2): #1 se sono due valori successivi nella scala
    if valCarta1 != valCarta2-1:
        if valCarta1 == 13 and valCarta2 == 1:
            return 1
        else:
            return 0
    else:
        return 1



class carta:
    def __init__(self, val, sem):
        self.val = val
        self.sem = sem
    def show(self):
        print("%d%c" % (self.val, self.sem), end = " ")


class comb:
    def __init__(self, carte, scala):
        self.carte = carte  #lista carte
        self.scala = scala  #1 se scala, 0 se comb stesso valore semi diversi    
    def show(self):
        for i in range(len(self.carte)):
            self.carte[i].show()
    def ordina(self):
        if self.scala == 1:
            self.carte = ordina_val(self.carte)
    def controlla(self): #restituisce 0 se comb non valida, 1 se valida
        return controllaComb(self.carte, self.scala)
    def calcLoss(self, posCarta): #restituisce il numero di carte sospese e il numero di tris monchi [0, 1, 2]
        if self.scala == 1:
            carteSospese = 0
            tot = len(self.carte)
            num1 = posCarta
            num2 = tot - num1 - 1
            if num1 == 0 or num1 >= 3:
                t1 = 1
            else:
                t1 = 0
                carteSospese += num1
            if num2 == 0 or num2 >= 3:
                t2 = 1
            else:
                t2 = 0
                carteSospese += num2
            trisMonchi = 2 - t1 - t2
            return trisMonchi, carteSospese
        else:
            if len(self.carte) >= 3:
                return 0, 0
            else:
                return 1, 2
    def calcDoubleLoss(self, pos1, pos2): #ps: pos1 e pos2 max distanti di 1
        if self.scala == 1:
            carteSospese = 0
            tot = len(self.carte)
            num1 = pos1
            num2 = tot - pos2 - 1
            mezzo = abs(pos2 - pos1) - 1
            if num1 == 0 or num1 >= 3:
                t1 = 1
            else:
                t1 = 0
                carteSospese += num1
            if num2 == 0 or num2 >= 3:
                t2 = 1
            else:
                t2 = 0
                carteSospese += num2
            carteSospese += mezzo
            trisMonchi = 2 - t1 - t2
            if mezzo >= 1:
                trisMonchi += 1
            return trisMonchi, carteSospese
        else:
            return 1, 2


class spazioDiComb:
    def __init__(self, combs): #lista di comb
        self.combs = combs
    def show(self):
        for i in range(len(self.combs)):
            self.combs[i].show()
            print()
    def cerca(self, val, sem): #ne cerca solo uno
        for index1, comb in enumerate(self.combs):
            for index2, carta in enumerate(comb.carte):
                if carta.val == val and carta.sem == sem:
                    return [index1, index2]
        return [-1] #non ne ha trovate
    def cercaTutte(self, val, sem): #ne cerca solo uno
        lista = []
        for index1, comb in enumerate(self.combs):
            for index2, carta in enumerate(comb.carte):
                if carta.val == val and carta.sem == sem:
                    lista.append([index1, index2])
        if len(lista)==0:
            return [-1]
        else:
            return lista           
    def numero(self):
        num = 0
        for i in self.combs:
            num += len(i.carte)
        return num


class spazioDiMiste:
    def __init__(self, carte):
        self.carte = carte #lista di carte
    def show(self):
        for i in self.carte:
            i.show()
    def cerca(self, val, sem):
        for index, carta in enumerate(self.carte): #va bene che ne cerchi uno solo!
            if carta.val == val and carta.sem == sem:
                return index
        return -1
    def vuoto(self):
        if len(self.carte)==0:
            return 1
        else:
            return 0
    def eliminaUna(self, carta0):
        val = carta0.val
        sem = carta0.sem
        for i in range(len(self.carte)):
            if self.carte[i].val == val and self.carte[i].sem == sem:
                del(self.carte[i])
                return

def cartaPrima(val):
    if val == 1:
        return 13
    else:
        return val-1
    
def cartaDopo(val):
    if val == 13:
        return 1
    else:
        return val+1

def altriSemi(sem):
    tutti = ['c', 'q', 'f', 'p']
    tutti.remove(sem)
    return tutti

def combinazioni(A, B, coppie):
    for i in A:
        for j in B:
            coppie.append([i,j])
    return coppie

def genera_coppie(carta, limbo, tavolo): #cerca solo in limbo e tavolo (paradiso proverà dopo a inserirle)
    val = carta.val
    sem = carta.sem
    
    #ricerca sem
    risSem = [ [-1], [-1], [-1], sem]
    
    semiMancanti = altriSemi(sem)
    
    for index, semeM in enumerate(semiMancanti):
        risSem[index]+=(tavolo.cercaTutte(val, semeM))
    for index, semeM in enumerate(semiMancanti):
        risSem[index].append(limbo.cerca(val, semeM))
    
    #ricerca down up
    val1 = cartaPrima(val)
    val3 = cartaDopo(val)
    
    ris = [ [-1], [-1], val, [-1], [-1] ]
    
    ris[1]+=tavolo.cercaTutte(val1, sem)
    ris[1].append(limbo.cerca(val1, sem))
    if ris[1].count(-1) != len(ris[1]):  #ha trovato qualcosa in ris[1]
        ris[0]+=tavolo.cercaTutte(cartaPrima(val1), sem)
        ris[0].append(limbo.cerca(cartaPrima(val1), sem))
    
    ris[3]+=tavolo.cercaTutte(val3, sem)
    ris[3].append(limbo.cerca(val3, sem))
    if ris[3].count(-1) != len(ris[3]):  #ha trovato qualcosa in ris[3]
        ris[4]+=tavolo.cercaTutte(cartaDopo(val3), sem)
        ris[4].append(limbo.cerca(cartaDopo(val3), sem))    
    
    for i in [0,1,2]: #elimina i [-1]
        risSem[i] = list(filter(lambda x: x != -1, risSem[i]))
    for i in [0,1,3,4]:
        ris[i] = list(filter(lambda x: x != -1, ris[i]))
    
    coppie = []
    
    if len(risSem[0]) > 0 and len(risSem[1]) > 0:
        coppie = combinazioni(risSem[0], risSem[1], coppie)
    if len(risSem[1]) > 0 and len(risSem[2]) > 0:
        coppie = combinazioni(risSem[1], risSem[2], coppie)
    if len(risSem[0]) > 0 and len(risSem[2]) > 0:
        coppie = combinazioni(risSem[0], risSem[2], coppie)
        
    if len(ris[0]) > 0 and val != 2:
        coppie = combinazioni(ris[0], ris[1], coppie)
    if len(ris[4]) > 0 and val != 13:
        coppie = combinazioni(ris[3], ris[4], coppie)
    if len(ris[1]) > 0 and len(ris[3]) > 0 and val != 1:
        coppie = combinazioni(ris[1], ris[3], coppie)
    
    return coppie
    


def fit_paradiso(carta0, paradiso):
    lista = []
    combIndex=0
    for comb in paradiso.combs:
        combTest = deepcopy(comb)
        combTest.carte.append(carta0)
        if combTest.controlla() == 1:
            lista.append(combIndex)
        combIndex+=1
    return lista


def crea_classifica(coppie, limbo, tavolo): #Tris scoperti e carte scoperte
    nuove_coppie = []
    for c in coppie:
        if type(c[0]) == type(c[1]) == int:
            punteggio = -10.0
        if type(c[0]) == type(c[1]) == list:
            if c[0][0] != c[1][0]:
                [tris1,carte1] = tavolo.combs[c[0][0]].calcLoss(c[0][1]) #prima carta della coppia
                [tris2,carte2] = tavolo.combs[c[1][0]].calcLoss(c[1][1]) #seconda
                punteggio = tris1 + tris2 + 0.001*(carte1 + carte2)
            else: #fanno parte dello stesso tris
                [trisD,carteD] = tavolo.combs[c[0][0]].calcDoubleLoss(c[0][1], c[1][1])
                punteggio = trisD + 0.001*carteD
        if type(c[0]) != type(c[1]):
            if type(c[0]) == list:
                [trisS,carteS] = tavolo.combs[c[0][0]].calcLoss(c[0][1])
            else:
                [trisS,carteS] = tavolo.combs[c[1][0]].calcLoss(c[1][1])
            punteggio = trisS + 0.001*carteS
        nuove_coppie.append(c + [punteggio])
        
    nuove_coppie.sort(key=lambda c: c[2])
    
    return nuove_coppie


def killTris(killList, limbo, tavolo):
    if len(killList) == 0:
        return limbo, tavolo
    if len(killList) == 2:
        if killList[0][0] == killList[1][0]: #stesso tris
            combin = killList[0][0]
            pos1 = killList[0][1]
            pos2 = killList[1][1]
            if pos2 < pos1:
                pos2, pos1 = pos1, pos2
            exTris = tavolo.combs[combin]
            combNuove = [comb(exTris.carte[:pos1], exTris.scala), comb(exTris.carte[pos1+1:pos2], exTris.scala), comb(exTris.carte[pos2+1:], exTris.scala)]
            del(exTris.carte[pos2]) #MANTENERE IN QUESTO VERSO quando elimino pos1, tutte le posizioni dopo scalano di 1
            del(exTris.carte[pos1])
            for j in [0,1,2]:
                if len(combNuove[j].carte) > 0:
                    if combNuove[j].controlla() == 1:
                        tavolo.combs.append(combNuove[j])
                    else:
                        limbo.carte += combNuove[j].carte
            del(tavolo.combs[killList[0][0]])
        else: #tris diversi
            for i in [0,1]:
                exTris = tavolo.combs[killList[i][0]]
                combNuove = [comb(exTris.carte[:killList[i][1]], exTris.scala), comb(exTris.carte[killList[i][1]+1:], exTris.scala)]
                del(exTris.carte[killList[i][1]])
                if exTris.controlla() == 0: #il tris non è più valido
                    for j in [0,1]:
                        if len(combNuove[j].carte) > 0:
                            if combNuove[j].controlla() == 1:
                                tavolo.combs.append(combNuove[j])
                            else:
                                limbo.carte += combNuove[j].carte
                else: #il tris è ancora valido, non eliminare
                    tavolo.combs.append(exTris)
            comb1, comb2 = killList[0][0], killList[1][0]
            if comb1 > comb2:
                comb1, comb2 = comb2, comb1
            del(tavolo.combs[comb2])  #PRIMA IL 2
            del(tavolo.combs[comb1])            
    if len(killList) == 1:
        exTris = tavolo.combs[killList[0][0]]
        combNuove = [comb(exTris.carte[:killList[0][1]], exTris.scala), comb(exTris.carte[killList[0][1]+1:], exTris.scala)]
        del(exTris.carte[killList[0][1]])
        if exTris.controlla() == 0: #tris non più valido
            for i in [0,1]:
                if len(combNuove[i].carte) > 0:
                    if combNuove[i].controlla() == 1:
                        tavolo.combs.append(combNuove[i])
                    else:
                        limbo.carte += combNuove[i].carte
            del(tavolo.combs[killList[0][0]])
    
    return limbo, tavolo

def verifica(limbo, tavolo, paradiso):
    global carteTot
    nLimbo = len(limbo.carte)
    nTavolo = tavolo.numero()
    nParadiso = paradiso.numero()
    if nLimbo + nTavolo + nParadiso != carteTot:
        return 0
    return 1

def verificaPesante(tavolo, paradiso):
    for i in tavolo.combs:
        if i.controlla() != 1:
            return 0
    for i in paradiso.combs:
        if i.controlla() != 1:
            return 0
    return 1

def utili(mano, tavolo): #data la mano, dà la lista di carte non inutili
    listaCarte = []
    for carta0 in mano.carte:
        limboTest = deepcopy(mano)
        limboTest.eliminaUna(carta0)
        lista_coppie = genera_coppie(carta0, limboTest, tavolo)
        if len(lista_coppie) > 0: #non è inutile
            listaCarte.append(carta0)
    return listaCarte

def powerset(s):
    x = len(s)
    res = []
    for i in range(1 << x):
        res.append([s[j] for j in range(x) if (i & (1 << j))])
    res.remove([])
    return res

def ordinaPower(lista):
    nuovaLista = []
    for numeroCarte in range(len(lista)):
        for i in lista:
            if len(i) == numeroCarte:
                nuovaLista.append(i)
    return nuovaLista

def printaRis(carte,tavolo,paradiso, lunMano):
    print('\n --- Avanzamento: %d / %d ---\n' % (len(carte), lunMano) )
    print('Carte: ', end = '')
    for i in carte:
        i.show()
    print('\n\nTavolo:')
    tavolo.show()
    print()
    paradiso.show()
    return
    
def cercaDaManoUtile(manoUtile, tavolo):
    lista_risultati = []
    limbo = spazioDiMiste([])
    powerSetList = powerset(manoUtile.carte)
    powerSetList = ordinaPower(powerSetList)
    nMaxTrovato = 0
    for i in powerSetList:
        if nMaxTrovato < len(i):
            limbo.carte = i
            risultato, tavoloF, paradisoF = ugo(limbo, tavolo, spazioDiComb([]))
            if risultato == 1:
                lista_risultati.append([i,tavoloF,paradisoF])
                nMaxTrovato = len(i)
                printaRis(i,tavoloF,paradisoF, len(manoUtile.carte))
    return lista_risultati

def ugo(limbo, tavolo, paradiso):
    global ugo_attivazioni,errore,errorePesante #########
    ugo_attivazioni += 1
    '''
    ver = verifica(limbo, tavolo, paradiso)
    checkPesante = verificaPesante(tavolo, paradiso)
    if ver == 0:
        errore+=1
    if checkPesante == 0:
        errorePesante+=1
    
    print('___UGO___',ugo_attivazioni,'___',ver)
    print("--- Limbo ---")
    limbo.show()
    print("\n--- Tavolo ---")
    tavolo.show()
    print("--- Paradiso ---")
    paradiso.show()
    cacca=input()'''
        
    if limbo.vuoto() == 1:
        return 1, tavolo, paradiso  #Limbo vuoto = Si può! Ritorna il tavolo e paradiso finale
    else:
        new_limbo = deepcopy(limbo)
        carta0 = new_limbo.carte[0] #consideriamo la prima carta del limbo, adesso non è più nel limbo
        del(new_limbo.carte[0])
        #dove si può mettere sta carta, tutti i posti possibili?
        lista_coppie = genera_coppie(carta0, new_limbo, tavolo) #guarda tutte le coppie possibili del tavolo, lista di due elementi: elemento=coppia di indici o singolo (in tal caso) viene dal limbo
        lista_coppie_ordinata = crea_classifica(lista_coppie, new_limbo, tavolo)
        lista_paradiso = fit_paradiso(carta0, paradiso) #guarda quali sono i tris del paradiso in cui può mettere la carta, lista di interi
        classifica = lista_paradiso + lista_coppie_ordinata  #ATTENZIONE. non usare più le liste di sopra, perché vengono modificate magari quando si modifica classifica
        
        if len(classifica) == 0:
            return 0, None, None
        else:
            for pos in classifica:
                new2_limbo = deepcopy(new_limbo)
                new_tavolo = deepcopy(tavolo)
                new_paradiso = deepcopy(paradiso)
                '''print('___CLASSIFICA___', pos, '%d%c' % (carta0.val,carta0.sem))
                print("--- Limbo ---")
                new2_limbo.show()
                print("\n--- Tavolo ---")
                new_tavolo.show()
                print("--- Paradiso ---")
                new_paradiso.show()
                cacca=input()'''
                if type(pos) == int: #metti in paradiso         #MODIFICA PARADISO-TAVOLO-LIMBO   
                    new_paradiso.combs[pos].carte.append(deepcopy(carta0))
                    new_paradiso.combs[pos].ordina()  
                else:
                    cartaP = [0, 0, 0]
                    cartaP[2] = deepcopy(carta0)
                    killList = []
                    for i in [0,1]:
                        if type(pos[i]) == int:
                            cartaP[i] = deepcopy(new2_limbo.carte[pos[i]])
                        else:
                            cartaP[i] = deepcopy(new_tavolo.combs[pos[i][0]].carte[pos[i][1]])
                            killList.append(pos[i])
                    for i in [0,1]:
                        if type(pos[i]) == int:
                            new2_limbo.eliminaUna(cartaP[i])
                    new2_limbo, new_tavolo = killTris(killList, new2_limbo, new_tavolo)
                    if cartaP[0].val == cartaP[1].val:
                        scala = 0
                    else:
                        scala = 1
                    nuovoTrisParadiso = comb([cartaP[0], cartaP[1], cartaP[2]], scala)
                    nuovoTrisParadiso.ordina()
                    new_paradiso.combs.append(nuovoTrisParadiso)
                risultato, tavoloFinale, paradisoFinale = ugo(new2_limbo, new_tavolo, new_paradiso)
                if risultato == 1:
                    return 1, tavoloFinale, paradisoFinale
            return 0, None, None

        '''
        #if classifica vuota --> return 0, None, None.  impossibile mettere quella carta e quindi tutto il limbo
        #else
        for pos in classifica:
            nuovoLimbo = copy(limbo)
            nuovoTavolo = copy(tavolo)
            nuovoParadiso = copy(paradiso)
            metti la carta nel tris in questione/sfalda la coppia e crea il nuovo tris e mettilo in Nuovo paradiso, riordina quel tris.
            il tris precedente, se sfaldato non più valido, mettilo nel limbo, all'inizio
            [ris, tavoloF, paradisoF] = ugo(nuovo limbo, nuovo tavolo, nuovo paradiso)
            if ris == 1:
                return 1, tavoloF, paradisoF
            else:
                rimetti com era prima
        #se sei arrivato qui nessuna carta in classifica ha funzionato
        return 0, None, None
'''

def impostaTavolo(listaStringhe):
    tavolo = spazioDiComb([])
    listaTris = []
    for stringa in listaStringhe:
        listaCarte = []
        tris = comb([],0)
        listaCarteStr = stringa.split()
        for cartaStr in listaCarteStr:
            seme = cartaStr[len(cartaStr)-1]
            cartaStr = cartaStr[:-1]
            valore = int(cartaStr)
            listaCarte.append(carta(valore, seme))
        tris.carte = listaCarte
        if listaCarte[0].val == listaCarte[1].val:
            tris.scala = 0
        else:
            tris.scala = 1
        listaTris.append(tris)
    tavolo.combs = listaTris
    return tavolo

def impostaMano(stringa):
    mano = spazioDiMiste([])
    listaCarte = []
    listaCarteStr = stringa.split()
    for cartaStr in listaCarteStr:
        seme = cartaStr[len(cartaStr)-1]
        cartaStr = cartaStr[:-1]
        valore = int(cartaStr)
        listaCarte.append(carta(valore, seme))
    mano.carte = listaCarte
    return mano

        
'''
PS: mano.
Scartare carte inutili
mettere tutte le carte nel limbo, avviare ugo e ricordarsi il tavolo e paradiso quante carte contiene, rifare con tutto il limbo tranne quella carta

vedere quali tra queste ha più carte

'''

ugo_attivazioni = 0

t = ['7p 7q 7f ',
    '12p 12q 12c ',
    '12f 12q 12c ',
    '7f 7p 7q ',
    '1c 1f 1q 1p ',
    '3c 3q 3p ',
    '4c 4f 4q ',
    '9c 10c 11c ',
    '3c 3f 3p ',
    '5c 6c 7c ',
    '5c 5p 5q',
    '6c 7c 8c 9c 10c',
    '4f 4p 4q ',
    '2c 2q 2f 2p ']

m = "6q 9q 9q 10f 10f 12p 13f"

tavolo = impostaTavolo(t)
mano = impostaMano(m)
paradiso = spazioDiComb([])
limbo = spazioDiMiste([]) 

manoUtile = spazioDiMiste(utili(mano, tavolo))
lista_risultati = cercaDaManoUtile(manoUtile, tavolo)



'''
nLimbo = len(limbo.carte)
nTavolo = tavolo.numero()
nParadiso = paradiso.numero()
carteTot = nLimbo + nTavolo + nParadiso
errore = 0
ugo_attivazioni = 0
errorePesante = 0


risultato, tavoloF, paradisoF = ugo(limbo, tavolo, spazioDiComb([]))


print('___VERO___')
print("--- Limbo ---")
limbo.show()
print("\n--- Tavolo ---")
tavolo.show()
print("--- Paradiso ---")
paradiso.show()

if risultato == 1:
    print('\n___FINALE___')
    print("--- Limbo ---")
    print("\n--- Tavolo ---")
    tavoloF.show()
    print("--- Paradiso ---")
    paradisoF.show()
else:
    print('\n Impossibile svuotare il limbo')
'''