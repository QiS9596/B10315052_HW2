import DESbox

class BlockCipherAgent:

    ECB_MODE = 0
    CBC_MODE = 1
    DESAgent = DESbox.DES()

    def __init__(self, defaultMode = ECB_MODE):
        self.mode = defaultMode
        self.defaultIV = [1,1,1,1,1,0,1,1]*8
        self.IV = self.defaultIV

    def setMode(self, mode):
        self.mode = mode

    def setIV(self, IV):
        self.IV = IV

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
        if self.mode == self.CBC_MODE:
            return self.CBCEncryption()

    def ECBEncryption(self):
        result = [None]*self.unhandledList.__len__()
        for a in range(0, self.unhandledList.__len__()):
            result[a] = self.DESAgent.encription(self.unhandledList[a])
        return result

    def CBCEncryption(self):
        result = [None]*self.unhandledList.__len__()
        temp = self.DESAgent.XOR(self.IV, self.unhandledList[0])
        result[0] = self.DESAgent.encription(temp)
        for i in range(1,self.unhandledList.__len__()):
            temp = self.DESAgent.XOR(result[i-1],self.unhandledList[i])
            result[i] = self.DESAgent.encription(temp)
        return result

    def decryption(self):
        if self.mode == self.ECB_MODE:
            return self.ECBDecryption()
        if self.mode == self.CBC_MODE:
            return self.CBCDecryption()

    def ECBDecryption(self):
        result = [None]*self.unhandledList.__len__()
        for a in range(0, self.unhandledList.__len__()):
            result[a] = self.DESAgent.decription(self.unhandledList[a])
        return result

    def CBCDecryption(self):
        result = [None]*self.unhandledList.__len__()
        temp = self.DESAgent.decription(self.unhandledList[0])
        result[0] = self.DESAgent.XOR(self.IV,temp)
        for i in range(1, self.unhandledList.__len__()):
            temp = self.DESAgent.decription(self.unhandledList[i])
            result[i] = self.DESAgent.XOR(temp, self.unhandledList[i-1])
        return result

a = BlockCipherAgent()
a.setMode(a.CBC_MODE)
c = [[1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0]]
print(c*2)
a.setInput(c*2)
b = a.encryption()
print(b)
a.setInput(b)
print(a.decryption())