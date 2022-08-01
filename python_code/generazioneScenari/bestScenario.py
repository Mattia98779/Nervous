import numpy as np

def CoCoS (path,maxProp=-1, write_to_file=False):
  rigide = []
  tipiche = []
  index = 0
  indexr = 0
  nPropMod = 0
  totProp = 0
  f = open(path, "r")
  print("FILE PATH: ", path)
  print("LETTURA PROPRIETA...")
  for x in f:
    if x != "":
      app = x.replace("\n","").replace(" ","").split(",")
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

  print("PROPRIETA RIGIDE = ",rigide)
  print("PROPRIETA TIPICHE = ", tipiche)
  print("INDIVIDUAZIONE POTENZIALI CONFLITTI...")
  # rileva conflitti
  conflitti = {}
  for r in rigide:
    if r[1] in conflitti.keys():
      conflitti[r[1]] = conflitti[r[1]]+[[r[3],"R"]]
    else:
      conflitti[r[1]] = [[r[3],"R"]]
  for t in tipiche:
    if t[1] in conflitti.keys():
      conflitti[t[1]] = conflitti[t[1]] + [[t[4],"T"]]
    else:
      conflitti[t[1]] = [[t[4],"T"]]

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
        if rigide[index[0][0]][2] != tipiche[index[1][0]][3]:
          sempreZero.append(index[1][0])
          if tipiche[index[1][0]][0] == "T(head)":
            generaTutto=1
      elif index[0][1] == "T" and index[1][1] == "T":
        # segno diverso
        if tipiche[index[0][0]][3] != tipiche[index[1][0]][3]:
          if tipiche[index[0][0]][0] == "T(modifier)" and tipiche[index[1][0]][0] == "T(head)":
            sempreZero.append(index[0][0])


  if stop!=1:
    current_prop = totProp-len(sempreZero)
    tipiche_filtered = tipiche.copy()
    if generaTutto == 0:
      minimo = min(tipiche[nPropMod:], key=lambda x: x[2])
      sempreZero.append(tipiche.index(minimo))
      del tipiche_filtered[tipiche.index(minimo)]
      current_prop=current_prop-1
    if maxProp!=-1:
      while current_prop>maxProp:
        minimo = min(tipiche_filtered, key=lambda x: x[2])
        sempreZero.append(minimo[4])
        del tipiche_filtered[tipiche_filtered.index(minimo)]
        current_prop = current_prop - 1
    best = np.ones(totProp)
    for el in sempreZero:
      best[el] = 0
    print("CALCOLO PROBABILITA...")
    p = 1
    c = 0
    for el in best:
      if el < 0.5:
        p = p * (1 - tipiche[c][2])
      else:
        p = p * tipiche[c][2]
      c = c + 1

    out = "Result : "
    for s in best:
      out = out + "'" + str(int(s)) + "', "
    out = out + str(p)
    print("MIGLIOR SCENARIO =", best, " ", p)
    if write_to_file==True:
      f = open(path, "a")
      f.write("\n")
      f.write(out)
  else:
    return -1
