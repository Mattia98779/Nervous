import numpy
import numpy as np
import itertools
import os
import CreateOntology as ontology

def checkConsistency(scenario, tipiche, rigide):
  scenarioOntologia = []
  for el in scenario:
    scenarioOntologia.append(str((int)(el)))
  scenarioOntologia.pop(len(scenarioOntologia)-1)

  tipicheOntologia = []
  for t in tipiche:
    if t[0] == "T(modifier)":
      if t[4]=="-":
        tipicheOntologia.append(("-"+t[1],t[2],False))
      else:
        tipicheOntologia.append((t[1], t[2], False))
    else:
      if t[4]=="-":
        tipicheOntologia.append(("-"+t[1],t[2],True))
      else:
        tipicheOntologia.append((t[1], t[2], True))

  rigideOntologia = []
  for r in rigide:
    if r[0] == "T(modifier)":
      if r[2]=="-":
        rigideOntologia.append(("-"+r[1],False))
      else:
        rigideOntologia.append((r[1], False))
    else:
      if r[2]=="-":
        rigideOntologia.append(("-"+r[1],True))
      else:
        rigideOntologia.append((r[1], True))

  #ex_t = [("attr2", 0.5, False), ("attr1", 0.5, False), ('-attr3', 0.7, True)]
  #ex_not_t = [("-attr1", True)]
  x = ontology.ManageOntology(tipicheOntologia, rigideOntologia, scenarioOntologia)
  consistency = x.is_consistent()
  print(consistency)
  # da chiamare create ontology
  return consistency

def CoCoS (path,maxProp=-1, write_to_file=False):
  # leggo proprietà rigide e tipiche del prototipo
  rigide = []
  tipiche = []
  index = 0
  indexr = 0
  nPropMod = 0
  totProp = 0
  nHead = 0
  nModifier = 0
  print("path =", path)
  f = open(path, "r")
  for x in f:
    if x != "":
      app = x.replace("\n","").replace(" ","").split(",")
      if "Head Concept Count :" in x:
        nHead = int(x.split(":")[1])
      if "Modifier Concept Count :" in x:
        nModifier = int(x.split(":")[1])
      if "T(modifier)" in x or "T(head)" in x:
        totProp=totProp+1
        if "T(modifier)" in x:
          nPropMod=nPropMod+1
        if app[1][0] == "-":
          app[1]=app[1][1:]
          app.append("-")
        else:
          app.append("+")
        app[2] = float(app[2])
        app[3] = int(app[3])
        app.append(index)
        tipiche.append(app)
        index = index+1
      elif "modifier" in x or "head" in x:
        if app[1][0] == "-":
          app[1]=app[1][1:]
          app.append("-")
        else:
          app.append("+")
        app.append(indexr)
        rigide.append(app)
        indexr=indexr+1

  # rileva conflitti
  conflitti = {}
  for r in rigide:
    if r[1] in conflitti.keys():
      conflitti[r[1]] = conflitti[r[1]]+[[r[3],"R"]]
    else:
      conflitti[r[1]] = [[r[3],"R"]]
  for t in tipiche:
    if t[1] in conflitti.keys():
      conflitti[t[1]] = conflitti[t[1]] + [[t[5],"T"]]
    else:
      conflitti[t[1]] = [[t[5],"T"]]

  sempreZero = []
  stop =0
  generaTutto = 0
  for c in conflitti:
    index = conflitti[c]
    if len(index)>=2:
      # due proprietà rigide in conflitto tra loro
      if index[0][1] == "R" and index[1][1] == "R" :
        if rigide[index[0][0]][2] != rigide[index[1][0]][2]:
          stop = 1
      # prima proprietà rigida e seconda tipica
      elif index[0][1] == "R" and index[1][1] == "T":
        # segno diverso
        if rigide[index[0][0]][2] != tipiche[index[1][0]][4]:
          sempreZero.append(index[1][0])
          if tipiche[index[1][0]][0] == "T(head)":
            generaTutto=1
      # due proprietà tipiche in conflitto
      elif index[0][1] == "T" and index[1][1] == "T":
        # segno diverso
        if tipiche[index[0][0]][4] != tipiche[index[1][0]][4]:
          if tipiche[index[0][0]][0] == "T(modifier)" and tipiche[index[1][0]][0] == "T(head)":
            sempreZero.append(index[0][0])

  if stop==0:
    propListIndexes = [ x for x in list(range(0, len(tipiche))) if x not in sempreZero]

    propListIndexesModifier = []
    propListIndexesHead = []

    for i in propListIndexes:
      if tipiche[i][0] == "T(modifier)":
        propListIndexesModifier.append(i)
      else:
        propListIndexesHead.append(i)


    allScenariosHead = list(map(list, itertools.product([0, 1], repeat=len(propListIndexesHead))))
    allScenariosModifier = list(map(list, itertools.product([0, 1], repeat=len(propListIndexesModifier))))
    if generaTutto==0:
      allScenariosHead.pop(-1)
    allScenarios = []
    for elHead in allScenariosHead:
      for elMod in allScenariosModifier:
        allScenarios.append(elHead+elMod)

    maxScenari = len(allScenarios)

    matrixScenarios = np.zeros((maxScenari, (len(tipiche))))

    columns = []
    for c in range(len(propListIndexes)):
      columns.append([item[c] for item in allScenarios] )

    for index in propListIndexes:
      matrixScenarios[:, index] = columns.pop()

    if maxProp!=-1:
      toDelete = []
      nRow = 0
      for r in matrixScenarios:
        if np.sum(r)>maxProp:
          toDelete.append(nRow)
        nRow = nRow+1
      matrixScenarios = np.delete(matrixScenarios, toDelete, axis=0)

    # aggiungo probabilità
    prob = []
    modH = (min(nModifier,nHead) / max(nModifier,nHead)) * 0.5 + 0.5
    modM = 1
    if nModifier < nHead:
      modM= modH
      modH=1

    for r in matrixScenarios:
      p = 0
      c = 0
      for el in r:
        if el < 0.5:
          if tipiche[c][0] == "T(modifier)":
            p = p + ((1 - tipiche[c][2]) * (tipiche[c][3] / nModifier)) * modM
          else:
            p = p + ((1 - tipiche[c][2]) * (tipiche[c][3] / nHead)) * modH
        else:
          if tipiche[c][0] == "T(modifier)":
            p = p + ((tipiche[c][2] * (tipiche[c][3] / nModifier))) * modM
          else:
            p = p + ((tipiche[c][2] * (tipiche[c][3] / nHead))) * modH
        c = c + 1
      prob.append([p])

    matrixProb = numpy.append(matrixScenarios, prob, axis=1)
    matrixProbOrdered = matrixProb[matrixProb[:,-1].argsort()]
    np.set_printoptions(suppress=True)
    tentativo = -1
    best = matrixProbOrdered[tentativo]
    while not (checkConsistency(best, tipiche, rigide)):
      tentativo = tentativo -1
      best = matrixProbOrdered[tentativo]
    out = "Result : "
    for s in best[:-1]:
      out = out + "'" + str(int(s)) + "', "
    out = out + str(best[-1])
    print("MIGLIOR SCENARIO = ", best)
    if write_to_file==True:
      f = open(path, "a")
      f.write("\n")
      f.write(out)
    return matrixProbOrdered
  else:
    return -1
