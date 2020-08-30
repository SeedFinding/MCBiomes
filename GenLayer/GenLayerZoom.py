import numpy as np

from GenLayer.Layer import Main


class GenLayerZoom(Main):
    def __init__(self, seed, layer, fuzzy, goup, WorldGenSeedDisable):
        super().__init__(seed)
        self.parent = [(layer, goup)]
        self.fuzzy = fuzzy
        self.switchs = WorldGenSeedDisable

    def getInts(self, aX, aY, aW, aH):
        if not self.switchs:
            self.worldGenSeed = 0
        pX, pZ, pWidth, pHeight = aX >> 1, aY >> 1, (aW >> 1) + 2, (aH >> 1) + 2

        aint = self.parent[0][0].getInts(pX, pZ, pWidth, pHeight)

        newWidth = (pWidth - 1) << 1
        newHeight = (pHeight - 1) << 1

        aint1 = [0] * ((newWidth + 1) * (newHeight + 1))

        for k1 in range(pHeight - 1):
            idx = (k1 << 1) * newWidth
            a = aint[k1 * pWidth]
            b = aint[(k1 + 1) * pWidth]
            for i2 in range(pWidth - 1):
                a1 = aint[i2 + 1 + k1 * pWidth]
                b1 = aint[i2 + 1 + (k1 + 1) * pWidth]
                self.initChunkSeed(((i2 + pX) << 1, (k1 + pZ) << 1))

                aint1[idx] = a
                aint1[idx + newWidth] = self.selectRandom([a, b])
                idx += 1
                aint1[idx] = self.selectRandom([a, a1])
                if self.fuzzy:
                    aint1[idx + newWidth] = self.selectRandom([a, a1, b, b1])
                else:
                    aint1[idx + newWidth] = self.selectModeOrRandom(a, a1, b, b1)
                idx += 1
                a, b = a1, b1

        aint2 = np.empty(aW * aH, dtype=int)
        for j3 in range(aH):
            aint2[j3 * aW:(j3 + 1) * aW] = np.copy(
                aint1[(j3 + (aY & 1)) * newWidth + (aX & 1): (j3 + (aY & 1)) * newWidth + (aX & 1) + aW])

        return aint2

    @staticmethod
    def magnify(seed, layer, coeff, fuzzy, goup, switch):
        for i in range(coeff):
            layer = GenLayerZoom(seed + i, layer, fuzzy, goup, switch)
        return layer
