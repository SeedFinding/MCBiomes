from collections import Counter

import numpy as np


class Main:
    def __init__(self, seed=None):
        self.size = 512
        self.storage = np.empty(self.size * self.size, dtype=int)

        if seed:
            self.baseSeed = seed
            self.baseSeed *= self.baseSeed * 6364136223846793005 + 1442695040888963407
            self.baseSeed += seed
            self.baseSeed *= self.baseSeed * 6364136223846793005 + 1442695040888963407
            self.baseSeed += seed
            self.baseSeed *= self.baseSeed * 6364136223846793005 + 1442695040888963407
            self.baseSeed += seed
            self.baseSeed = self.javaInt64(self.baseSeed)

    def javaInt64(self, val):
        return ((val + (1 << 63)) % (1 << 64)) - (1 << 63)

    def initChunkSeed(self, chunk):
        self.chunkSeed = self.worldGenSeed
        for i in range(2):
            self.chunkSeed *= (self.chunkSeed * 6364136223846793005 + 1442695040888963407)
            self.chunkSeed += chunk[0]
            self.chunkSeed *= (self.chunkSeed * 6364136223846793005 + 1442695040888963407)
            self.chunkSeed += chunk[1]
            self.chunkSeed = self.javaInt64(self.chunkSeed)

    def getStorage(self, x, z):
        return self.storage[x * self.size + z]

    def putStorage(self, x, z, value):
        self.storage[x * self.size + z] = value

    def getStorageView(self,aW,aH):
        res=np.zeros(aW*aH)
        for x in range(aH):
            for z in range(aW):
                res[x*aW+z]=self.getStorage(x,z)
        return res
    def generate(self,x,z,aW,aH):
        return None

    def countIt(self, array):
        dic = Counter(array)
        print(list(array))
        return [str(el) + " " + str(dic[el] / array.size) for el in dic]

    def initWorldSeed(self, seed):
        self.worldGenSeed = seed
        for el in self.parent:
            if el[1]:
                el[0].initWorldSeed(seed)
        self.worldGenSeed *= self.worldGenSeed * 6364136223846793005 + 1442695040888963407
        self.worldGenSeed += self.baseSeed
        self.worldGenSeed *= self.worldGenSeed * 6364136223846793005 + 1442695040888963407
        self.worldGenSeed += self.baseSeed
        self.worldGenSeed *= self.worldGenSeed * 6364136223846793005 + 1442695040888963407
        self.worldGenSeed += self.baseSeed
        self.worldGenSeed = self.javaInt64(self.worldGenSeed)

    def nextIntGen(self, limit):
        i = (self.chunkSeed >> 24) % limit
        if i < 0:
            i += limit
        self.chunkSeed *= (self.chunkSeed * 6364136223846793005 + 1442695040888963407)
        self.chunkSeed += self.worldGenSeed
        self.chunkSeed = self.javaInt64(self.chunkSeed)
        return i

    def selectRandom(self, l):
        return l[self.nextIntGen(len(l))]

    def isBiomeOceanic(self, biomeID):
        return biomeID in [24, 10, 0]

    def isValidId(self, id):
        x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
             29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 127, 129, 130, 131, 132, 133, 134, 140, 149, 151, 155, 156,
             157, 158, 160, 161, 162, 163, 164, 165, 166, 167]
        return id in x

    def sameClass(self, biomeA, biomeB):
        flag = False
        biomeClass = {"ocean": [0, 10, 24],
                      "plains": [1, 129],
                      "desert": [2, 17, 130],
                      "hills": [3, 20, 34, 131, 162],
                      "forest": [4, 18, 132, 157, 27, 28, 29],
                      "taiga": [5, 19, 30, 31, 32, 33, 133, 158, 160, 161],
                      "swamp": [6, 134],
                      "river": [7, 11],
                      "hell": [8],
                      "end": [9],
                      "mushroom": [14, 15],
                      "mesa": [37, 38, 39],
                      "savanna": [35, 36],
                      "beach": [16, 26],
                      "stonebeach": [25],
                      "jungle": [21, 22, 23, 149, 151],
                      "savannaMutated": [163, 164],
                      "forestMutated": [155, 156],
                      "snow": [12, 13, 140],
                      "void": [127]}
        for el in biomeClass:
            if biomeB in biomeClass[el] and biomeA in biomeClass[el]:
                flag = True
        return flag

    def getTempCategory(self, biome):
        cold, medium, warm = 0, 1, 2
        if biome in [30, 158, 12, 140, 11, 26, 127, 10]:
            return cold  # below 0.2
        elif biome in [35, 163, 2, 130, 37, 165, 38, 166, 36, 39, 164, 167, 8, 17]:
            return warm  # above 1.0
        else:
            return medium

    def biomesEqualOrMesaPlateau(self, biomeA, biomeB):

        if biomeA == biomeB:
            return True
        else:
            if self.isValidId(biomeA) and self.isValidId(biomeB):
                if biomeA != 38 and biomeA != 39:  # mesa rock and clear rock
                    return biomeA == biomeB or self.sameClass(biomeA, biomeB)

                else:
                    return biomeB == 38 or biomeB == 39
            else:
                return False

    def isSnowy(self, id):
        return id in [10, 11, 12, 13, 26, 30, 31, 140, 158]

    def selectModeOrRandom(self, j, l, k, i):

        if l == k and k == i:

            return l

        elif (j == l and j == k):

            return j

        elif (j == l and j == i):

            return j
        elif (j == k and j == i):

            return j

        elif (j == l and k != i):

            return j

        elif (j == k and l != i):

            return j

        elif (j == i and l != k):

            return j

        elif (l == k and j != i):

            return l

        elif (l == i and j != k):

            return l

        else:

            return k if k == i and j != l else self.selectRandom([j, l, k, i])

