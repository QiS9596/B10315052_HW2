import DESbox

class BlockCipherAgent:

    ECB_MODE = 0
    DESAgent = DESbox.DES()

    def __init__(self, defaultMode = ECB_MODE):
        self.mode = defaultMode

    def setKey(self, key):
        if key.__len__() == 64:
            self.DESAgent.setKey(key)

    def setInput(self, blocks:list):
        for a in blocks:
            if a.__len__() != 64:
                return

        self.unhandledList = blocks

    def encryption(self):
        if self.mode == self.ECB_MODE:
            return self.ECBEncryption()

    def ECBEncryption(self):
        result = [None]*self.unhandledList.__len__()
        for a in range(0, self.unhandledList.__len__()):
            result[a] = self.DESAgent.encription(self.unhandledList[a])
        return result

    def decryption(self):
        if self.mode == self.ECB_MODE:
            return self.ECBDecryption()

    def ECBDecryption(self):
        result = [None]*self.unhandledList.__len__()
        for a in range(0, self.unhandledList.__len__()):
            result[a] = self.DESAgent.decription(self.unhandledList[a])
        return result

a = BlockCipherAgent()
a.setInput([[1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0]])
b = a.encryption()
print(b)
a.setInput(b)
print(a.decryption())