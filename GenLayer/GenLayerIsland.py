from GenLayer.Layer import Main


class GenLayerIsland(Main):
    def __init__(self, seed):
        super().__init__(seed)
        self.parent = []

    def getInts(self, aX, aY, aW, aH):
        for i in range(aH):
            for j in range(aW):
                self.initChunkSeed((aX + j, aY + i))
                self.putStorage(i, j, 1 if self.nextIntGen(10) == 0 else 0)

        aint = self.getStorageView(aW, aH)
        if 0 >= aX > -aW and 0 >= aY > -aH:
            self.putStorage(-aY, -aX, 1)
        aint=self.getStorageView(aW, aH)
        #for el in aint:
        #    print(int(el), end=" ")
        #print()
        return aint
