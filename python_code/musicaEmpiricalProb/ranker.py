import os
import matplotlib.pyplot as plt
import collections
import numpy as np
import json

#ciao
class CanzoneToJson:
    def __init__(self, c, spiegazione):
        self.title = c.title
        self.performer = c.performer
        self.spiegazione = spiegazione

class Canzone:
    def __init__(self, title, performer, g, attributes):
        self.title = title
        self.performer = performer
        self.genre = g
        self.attributes = attributes


class Prototipo:
    def __init__(self, name, rigide, tipiche, nHead, nMod):
        self.name = name
        self.rigide = rigide
        self.tipiche = tipiche
        self.nHead = nHead
        self.nMod = nMod


def leggiCanzone(path):
    f = open("./songs/" + path, "r")
    file_name = os.path.basename(path)
    datas = os.path.splitext(file_name)[0].split("#")
    attributes = {}
    for l in f:
        if l != "":
            line = l.split(":")
            line = [s.strip() for s in line]
            attributes[line[0]] = [line[1], line[2]]
    c = Canzone(datas[0], datas[1], datas[2], attributes)
    return c


def leggiPrototipo(path):
    name = ""
    rigide = []
    tipiche = []
    result = []
    index = 0
    indexr = 0
    nPropMod = 0
    totProp = 0
    nHead = 0
    nModifier = 0
    f = open("./prototipi/" + path, "r")
    for x in f:
        if x != "":
            if "Title :" in x:
                name = x.split(":")[1].strip().replace("\n", "")
            if "Result :" in x:
                app = x.split(":")[1].split(",")[:-1]
                result = [int(s.replace("'", "")) for s in app]
            else:
                app = x.replace("\n", "").split(",")
                app = [s.strip() for s in app]
                if "Head Concept Count :" in x:
                    nHead = int(x.split(":")[1])
                if "Modifier Concept Count :" in x:
                    nModifier = int(x.split(":")[1])
                if "T(modifier)" in x or "T(head)" in x:
                    totProp = totProp + 1
                    if "T(modifier)" in x:
                        nPropMod = nPropMod + 1
                    if app[1][0] == "-":
                        app[1] = app[1][1:]
                        app.append("-")
                    else:
                        app.append("+")
                    app[2] = float(app[2])
                    app[3] = int(app[3])
                    app.append(index)
                    tipiche.append(app)
                    index = index + 1
                elif "modifier" in x or "head" in x:
                    if app[1][0] == "-":
                        app[1] = app[1][1:]
                        app.append("-")
                    else:
                        app.append("+")
                    app.append(indexr)
                    rigide.append(app)
                    indexr = indexr + 1

    for i in range(len(result) - 1, -1, -1):
        if result[i] == 0:
            tipiche.pop(i)

    prot = Prototipo(name, rigide, tipiche, nHead, nModifier)
    return prot

def score(prototipo, canzone):
    punteggio = 0
    inComune = []
    inContrasto = []
    for r in prototipo.rigide:
        if r[1] in canzone.attributes:
            if r[2] == "+":
                punteggio = punteggio + 1
                inComune.append(r[1])
            else:
                punteggio = punteggio - 999
    for t in prototipo.tipiche:
        if t[1] in canzone.attributes:
            if t[4] == "+":
                if t[0] == "T(modifier)":
                    punteggio = punteggio + 1 * float(canzone.attributes[t[1]][0]) * float(t[3]/prototipo.nMod)
                    inComune.append([t[1],float(canzone.attributes[t[1]][0])])
                else:
                    punteggio = punteggio + 1 * float(canzone.attributes[t[1]][0]) * float(t[3] / prototipo.nHead)
                    inComune.append([t[1], float(canzone.attributes[t[1]][0])])
            else:
                if t[0] == "T(modifier)":
                    punteggio = punteggio - 1 * float(canzone.attributes[t[1]][0]) * float(t[3] / prototipo.nMod)
                    inContrasto.append([t[1],float(canzone.attributes[t[1]][0])])
                else:
                    punteggio = punteggio - 1 * float(canzone.attributes[t[1]][0]) * float(t[3] / prototipo.nHead)
                    inContrasto.append([t[1],float(canzone.attributes[t[1]][0])])
    msg = scriviMotivazione (inComune, inContrasto)
    return punteggio, msg

def scriviMotivazione(inComune, inContrasto):
    s = ""
    if inComune:
        s = s + "both the combined genre and the song are "
        appS = []
        appD = []
        andCheck = 0
        for p in inComune:
            if p[1]>0.8:
                appS.append(p[0])
            else:
                appD.append(p[0])
        if appS:
            s = s + "really " + str(appS)
            andCheck = 1
        if appD:
            if andCheck == 1:
                s = s +  " and "
            s = s + "a bit " + str(appD)
    if inContrasto:
        s= s + "but the song is " + str(inContrasto) + " and the genre is not"
    return s

def classifica(protipo, canzoni):
    classifica = []
    for c in canzoni:
        punteggio, inComune = score(protipo, c)
        classifica.append([c, punteggio, inComune])
    return sorted(classifica, key=lambda x:x[1], reverse=True)

def statistichePrototipi(listaPrototipi):
    rapportoHeadMod = {}
    for p in listaPrototipi:
        nHead = 0
        nMod = 0
        for t in p.tipiche:
            if t[0] == "T(modifier)":
                nMod = nMod + 1
            else:
                nHead = nHead +1
        key = str(nMod) + " - " + str(nHead)
        if key in rapportoHeadMod:
            rapportoHeadMod[key] = rapportoHeadMod[key] + 1
        else:
            rapportoHeadMod[key] = 1

    names = list(rapportoHeadMod.keys())
    values = list(rapportoHeadMod.values())
    plt.bar(range(len(rapportoHeadMod)), values, tick_label=names)
    plt.title("rapporto Head Modifier")
    plt.show()

    propertyOccurrences = {}
    for p in listaPrototipi:
        for r in p.rigide:
            if r[1] in propertyOccurrences.keys():
                propertyOccurrences[r[1]] = propertyOccurrences[r[1]] + 1
            else:
                propertyOccurrences[r[1]] = 1
        for t in p.tipiche:
            if t[1] in propertyOccurrences.keys():
                propertyOccurrences[t[1]] = propertyOccurrences[t[1]] + 1
            else:
                propertyOccurrences[t[1]] = 1
    propertyOccurrencesOrdered = dict(
        sorted(propertyOccurrences.items(), key=lambda item: item[1], reverse=True))
    plt.clf()
    labels = list(propertyOccurrencesOrdered.keys())
    valori = list(propertyOccurrencesOrdered.values())
    plt.bar(range(len(propertyOccurrencesOrdered)), valori, tick_label=labels)
    plt.title("most used property")
    plt.show()
    print("!")


def statisticheClassifica(allClassifica):
    scoreMedi = {}
    for clas in allClassifica:
        scores = [row[1] for row in clas[1]]
        scoreSet = np.linspace(-1.5,1.5,13)
        dati = {}
        for s in scoreSet:
            dati[s] = sum(map(lambda x : x>=s and x<(s+0.25), scores))
        scoreMedi = {k: dati.get(k, 0) + scoreMedi.get(k, 0) for k in set(dati) | set(scoreMedi)}

    for k in scoreMedi.keys():
        scoreMedi[k] = scoreMedi[k] / len(allClassifica)
    plt.clf()
    scoreMediOrdered = dict(sorted(scoreMedi.items()))
    labels = list(scoreMediOrdered.keys())
    valori = list(scoreMediOrdered.values())
    plt.bar(range(len(scoreMediOrdered)), valori, tick_label=labels)
    plt.title("avg scores distribution")
    plt.show()

    punteggioMedioPerCanzone = {}
    for c in allClassifica[0][1]:
        punteggioMedioPerCanzone[c[0]] = [c[1]]
    for clas in allClassifica[1:]:
        for c in clas[1]:
            app = punteggioMedioPerCanzone[c[0]].copy()
            app.append(c[1])
            punteggioMedioPerCanzone[c[0]] = app
    for k in punteggioMedioPerCanzone.keys():
        punteggioMedioPerCanzone[k] = sum(punteggioMedioPerCanzone[k]) / len(punteggioMedioPerCanzone[k])

    plt.clf()
    punteggioMedioPerCanzoneOrdered = dict(sorted(punteggioMedioPerCanzone.items(), key=lambda item: item[1], reverse=True))
    labels = []
    for k in punteggioMedioPerCanzoneOrdered:
        labels.append(k.title)
    valori = list(punteggioMedioPerCanzoneOrdered.values())
    plt.bar(range(len(punteggioMedioPerCanzoneOrdered)), valori, tick_label=labels)
    plt.title("score medio per canzone")
    plt.show()

    plt.clf()
    nAttributes = []
    for c in punteggioMedioPerCanzoneOrdered.keys():
        nAttributes.append(len(c.attributes))
    plt.bar(range(len(punteggioMedioPerCanzoneOrdered)), nAttributes, tick_label=labels)
    plt.title("n Attributes per canzone")
    plt.show()

    scoreMaggioreZeroCont = {}
    for c in allClassifica[0][1]:
        if c[1]>0:
            scoreMaggioreZeroCont[c[0]] = 0
        else:
            scoreMaggioreZeroCont[c[0]] = 1
    for clas in allClassifica[1:]:
        for c in clas[1]:
            app = scoreMaggioreZeroCont[c[0]]
            if c[1]>0 :
                app=app+1
            scoreMaggioreZeroCont[c[0]] = app

    plt.clf()
    #scoreMaggioreZeroCont = dict(
    #    sorted(scoreMaggioreZeroCont.items(), key=lambda item: item[1], reverse=True))
    labels = []
    for k in scoreMaggioreZeroCont:
        labels.append(k.title)
    valori = list(scoreMaggioreZeroCont.values())
    plt.bar(range(len(scoreMaggioreZeroCont)), valori, tick_label=labels)
    plt.title("conteggio score maggiore 0 per canzone")
    plt.show()

    plt.clf()
    nCanzoniPerClassifica = {}
    for c in allClassifica:
        n = 0
        for s in c[1]:
            if s[1]>0:
                n=n+1
        nCanzoniPerClassifica[c[0].name] = n
    plt.clf()
   # nCanzoniPerClassifica = dict(
   #     sorted(nCanzoniPerClassifica.items(), key=lambda item: item[0], reverse=True))
    labels = []
    for k in nCanzoniPerClassifica:
        labels.append(k)
    valori = list(nCanzoniPerClassifica.values())
    plt.bar(range(len(nCanzoniPerClassifica)), valori, tick_label=labels)
    plt.title("n canzoni score maggiore 0 per prototipo")
    plt.show()

    nCanzoniAppartenentiAiGeneriBase = {}
    for c in allClassifica:
        n = 0
        g1 = c[0].name.split("#")[0]
        g2 = c[0].name.split("#")[1]
        for s in c[1]:
            if s[0].genre!=g1 and s[0].genre!=g2 and s[1]>0:
                n = n + 1
        nCanzoniAppartenentiAiGeneriBase[c[0].name] = n
    plt.clf()
    #nCanzoniAppartenentiAiGeneriBase = dict(
    #    sorted( nCanzoniAppartenentiAiGeneriBase.items(), key=lambda item: item[0], reverse=True))
    labels = []
    for k in  nCanzoniAppartenentiAiGeneriBase:
        labels.append(k)
    valori = list( nCanzoniAppartenentiAiGeneriBase.values())
    plt.bar(range(len( nCanzoniAppartenentiAiGeneriBase)), valori, tick_label=labels)
    plt.title("n canzoni non appartenenti ai generi di base")
    plt.show()

    print("!")

def scriviJson(toWrite):
    for el in toWrite:
        jsonString = ""
        jsonPrototipo = json.dumps(el[0].__dict__)
        jsonString=jsonString+jsonPrototipo
        jsonString = jsonString[:-1]
        jsonString = jsonString + ', "classifica": ['
        for c in el[1]:
            jsonCanzone = json.dumps(CanzoneToJson(c[0], c[2]).__dict__)
            jsonString = jsonString  + jsonCanzone + ","
        jsonString = jsonString[:-1] + "]}"
        f = open("classifiche/"+el[0].name.replace("#","_"), "w")
        f.write(jsonString)

if __name__ == '__main__':
    listaCanzoni = []
    listaProt = []
    allClassifiche = []
    file_list = os.listdir('./songs')
    for file in file_list:
        listaCanzoni.append(leggiCanzone(file))
    print("FINE LETTURA CANZONI")
    file_list = os.listdir('./prototipi')
    for file in file_list:
        listaProt.append(leggiPrototipo(file))
    print("FINE LETTURA PROTOTIPI")
    for p in listaProt:
        allClassifiche.append([p, classifica(p, listaCanzoni)])
    print("FINE CLASSIFICA")
    statistichePrototipi(listaProt)
    statisticheClassifica(allClassifiche)
    #scriviJson(allClassifiche)
    print("FINE STATISTICHE")
    print("!")
