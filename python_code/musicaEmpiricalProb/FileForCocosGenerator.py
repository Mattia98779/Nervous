# Classe recuperata da DENOTER e modificata
#

from operator import itemgetter
import os

n_prop_negative = -2
n_prop = 8

all_attr = open("attributes.txt", 'r')
all_attributes = []
for l in all_attr:
    app = l.split(":")
    all_attributes.append([app[0],(int)(app[1].strip())])

all_attributes = sorted(all_attributes, key=itemgetter(1), reverse=True)
print("a")





class Property:
    name = ""
    prob = 0.0
    nItem = 0

    def __init__(self, name, prob, nItem):
        self.name = name
        self.prob = prob
        self.nItem = nItem

def getProperties(file, con_negative_rigide=False, con_negative_tipiche=False):

    l_t = []
    list_rigid = []
    list_typical = []
    f = open(file, 'r')
    cont = 0
    nCanzoni = 0
    for line in f:
        if "#Numero di canzoni:" in line:
            nCanzoni=int(str(line.split(':')[1]).strip().replace('\n', ''))
        else:
            if line.strip() != '' and cont == 0:
                list_rigid.append(line.strip())
            elif line.strip() == '':
                cont += 1
            else:
                p = Property(line.split(':')[0],
                             float(str(line.split(':')[1].split(",")[0]).strip().replace('\n', '')),
                             int(str(line.split(':')[1].split(",")[1]).strip().replace('\n', '')))
                list_typical.append(p)
                l_t.append(line.split(':')[0])

    if con_negative_rigide:
        list_negative_r = []
        for n in all_attributes:
            if (n[0] not in l_t) and (n[0] not in list_rigid):
                list_negative_r.append(n)
        for n_p in list_negative_r[:2]:
            list_rigid.append("-"+n_p[0])

    if con_negative_tipiche:
        last = list_typical[n_prop_negative:]
        list_typical=list_typical[:n_prop_negative]
        for el in last:
            p = Property("-"+el.name, 0.9, nCanzoni-1)
            list_typical.insert(0,p)





    return list_rigid, list_typical, nCanzoni

def createFileForCocos(head, modifier):

    list_head_rigid, list_head_typical, nCanzoniHead = getProperties('./genres/' + head, con_negative_tipiche=True)
    list_modifier_rigid, list_modifier_typical, nCanzoniModifier = getProperties('./genres/' + modifier, con_negative_tipiche=True)
    list_modifier_typical = list_modifier_typical[:n_prop]
    list_head_typical = list_head_typical[:n_prop]
    head = head.replace(".txt", "")
    modifier = modifier.replace(".txt", "")
    print(head, modifier)


    f = open("prototipi/" + head + "_" + modifier, "w")
    f.write("#Title composizione\n")
    f.write("Title : " + head + "#" + modifier + "\n\n")
    f.write("#Concetto Principale\n")
    f.write("Head Concept Name : " + head +"\n")
    f.write("Head Concept Count : " + str(nCanzoniHead)  + "\n\n")
    f.write("#Concetto Modificatore\n")
    f.write("Modifier Concept Name : " + modifier + "\n")
    f.write("Modifier Concept Count : " + str(nCanzoniModifier)  + "\n\n")

    # Proprietà Dure -
    for p in list_head_rigid:
        f.write("head, " + p + "\n")
    f.write("\n\n")

    for p in list_modifier_rigid:
        f.write("modifier, " + p + "\n")
    f.write("\n\n")


    # Properietà Deboli
    for i in range(len(list_modifier_typical)):
        f.write("T(modifier), " + list_modifier_typical[i].name + ", " + str(list_modifier_typical[i].prob) +", "+ str(list_modifier_typical[i].nItem)+ "\n")
    f.write("\n")


    for i in range(len(list_head_typical)):
        f.write("T(head), " + list_head_typical[i].name + ", " + str(list_head_typical[i].prob) + ", "+str(list_head_typical[i].nItem) +"\n")
    f.write("\n")
    f.close()


# Main : lettura generi da associare creativamente tramite argomento di linea di comando, lettura proprietà dai file, scrittura file per COCOS
if __name__ == '__main__':
    file_list = os.listdir('./genres')
    for file in file_list:
        for file2 in file_list:
            if file != file2:
                createFileForCocos(file, file2)
