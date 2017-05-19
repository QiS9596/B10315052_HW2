import DESbox

class BlockCipherAgent:

    ECB_MODE = 0
    CBC_MODE = 1
    OFB_MODE = 2
    CTR_MODE = 3
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
        if self.mode == self.OFB_MODE:
            return self.OFBEncryption()
        if self.mode == self.CTR_MODE:
            return self.CTREncryption()

    def ECBEncryption(self):
        result = [None]*self.unhandledList.__len__()
        print(self.unhandledList.__len__())
        for a in range(0, self.unhandledList.__len__()):
            print(a)
            result[a] = self.DESAgent.encription(self.unhandledList[a])
        return result

    def CBCEncryption(self):
        result = [None]*self.unhandledList.__len__()
        print(self.unhandledList.__len__())
        temp = self.DESAgent.XOR(self.IV, self.unhandledList[0])
        result[0] = self.DESAgent.encription(temp)
        for i in range(1,self.unhandledList.__len__()):
            print(i)
            temp = self.DESAgent.XOR(result[i-1],self.unhandledList[i])
            result[i] = self.DESAgent.encription(temp)
        return result

    def OFBEncryption(self):
        result = [None]*self.unhandledList.__len__()
        a = self.IV
        for i in range(0,self.unhandledList.__len__()):
            print(i)
            a = self.DESAgent.encription(a)
            result[i] = self.DESAgent.XOR(a,self.unhandledList[i])
        return result

    def CTREncryption(self):
        result = []
        result.append(self.IV)
        for i in range(1,self.unhandledList.__len__()):
            print(i)
            result.append(self.binary_add1(result[i-1]))
            result[i-1] = self.DESAgent.encription(result[i-1])
            result[i-1] = self.DESAgent.XOR(result[i-1],self.unhandledList[i-1])
        end = self.unhandledList.__len__()-1
        result[end] = self.DESAgent.encription(result[end])
        result[end] = self.DESAgent.XOR(result[end], self.unhandledList[end])
        return result

    def decryption(self):
        if self.mode == self.ECB_MODE:
            return self.ECBDecryption()
        if self.mode == self.CBC_MODE:
            return self.CBCDecryption()
        if self.mode == self.OFB_MODE:
            return self.OFBDecryption()
        if self.mode == self.CTR_MODE:
            return self.CTRDecryption()



    def ECBDecryption(self):
        result = [None]*self.unhandledList.__len__()
        for a in range(0, self.unhandledList.__len__()):
            print(a)
            result[a] = self.DESAgent.decription(self.unhandledList[a])
        return result

    def CBCDecryption(self):
        result = [None]*self.unhandledList.__len__()
        temp = self.DESAgent.decription(self.unhandledList[0])
        result[0] = self.DESAgent.XOR(self.IV,temp)
        for i in range(1, self.unhandledList.__len__()):
            print(i)
            temp = self.DESAgent.decription(self.unhandledList[i])
            result[i] = self.DESAgent.XOR(temp, self.unhandledList[i-1])
        return result

    def OFBDecryption(self):
        return self.OFBEncryption()

    def CTRDecryption(self):
        return self.CTREncryption()

    def binary_add1(self, origin):
        carry = 1
        result = [None]*origin.__len__()
        for i in range(origin.__len__()-1,-1,-1):
            if carry == 1 and origin[i] == 1:
                result[i] = 0
                carry = 1
            elif carry == 1 and origin[i] == 0:
                result[i] = 1
                carry = 0
            else:
                result[i] = origin[i]
        return result

