# Classe di supporto per prototyperGenre.py

import os


class Song:
    def __init__(self, title, performer, g, attribute):
        self.title = title
        self.performer = performer
        self.attributes = []
        self.dict = {}
        self.genre = g.replace(g.split("-")[-1], "")[:-1]
        print("g", self.genre)

        if len(attribute) >= 1:
            for i in range(len(attribute)):
                pair = attribute[i].split(" (")
                pair[1] = pair[1][0:1]
                self.attributes.append(pair)

    def __str__(self):
        return "title: {0}, performer: {1}, \nattributes: {2}" \
            .format(self.title, self.performer, self.attributes)

    def writeWordInf(self, file, word, value, n):
        spaces = 35 - len(word) + 1
        stri = word + ":"
        for idx in range(spaces):
            stri = stri + " "

        stri = stri + str(value) + " : " + str(n)
        file.write(stri + "\n")

    def toPercent(self):
        MAX_SCORE = 0.9
        MIN_SCORE = 0.6
        minFreq = 1
        maxFreq = 0

        for i in range(len(self.attributes)):
            freq = int(self.attributes[i][1]) / len(self.attributes)
            minFreq = min(minFreq, freq)
            maxFreq = max(maxFreq, freq)

        rangeFreq = maxFreq - minFreq
        rangeScore = MAX_SCORE - MIN_SCORE
        print("songs/", self.title, "#", self.performer, ".txt", "w+")
        f = open("songs/" + self.title + "#" + self.performer + "#"+self.genre+ ".txt", "w+")

        # for i in range(len(self.attributes)):
        for pair in sorted(self.attributes, key=lambda kv: kv[1], reverse=True):

            freq = int(pair[1]) / len(self.attributes)

            score = MAX_SCORE
            if rangeFreq > 0:
                score = MIN_SCORE + (rangeScore * (freq - minFreq) / rangeFreq)
                self.writeWordInf(f, pair[0], str(score), int(pair[1]))

        f.close()
        if rangeFreq <= 0:
            os.remove("songs/" + self.title + "#" + self.performer + "#"+self.genre+ ".txt")
