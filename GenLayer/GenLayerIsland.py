from GenLayer.Layer import Main


class GenLayerIsland(Main):
    def __init__(self, seed):
        super().__init__(seed)
        self.parent = []

    def getInts(self, aX, aZ, aW, aH):
        for z in range(aH):
            for x in range(aW):
                self.initChunkSeed((aX + x, aZ + z))

                self.putStorage(z, x, 1 if self.nextIntGen(10) == 0 else 0)



        if 0 >= aX > -aW and 0 >= aZ > -aH:
            self.putStorage(-aZ, -aX, 1)
        aint=self.getStorageView(aW, aH)

        return aint
