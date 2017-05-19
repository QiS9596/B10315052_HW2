


from PIL import Image

class imageReader:
    def openImgAndGetData(self, name = 'test.bmp'):
        self.image = Image.open(name)
        self.width = self.image.width
        self.height = self.image.height
        return self.image.getdata()

    def listToBinaryList(self, origin):
        result = []
        for a in origin:
            temp = bin(a)[2:bin(a).__len__()]
            while temp.__len__()<8:
                temp = '0'+temp
            for a in temp:
                result.append(int(a))
        return result

    R = 0
    G = 1
    B = 2
    def getChannelToList(self,channel):
        result = []
        for a in self.image.getdata():
            result.append(a[channel])
        return result

    def getEntireImageToList(self):
        result = []
        for a in self.image.getdata():
            for b in a:
                result.append(b)
        return result

    def padding(self,binaryList):
        result = []
        for i in range(0,binaryList.__len__(),64):
            if i + 64 >= binaryList.__len__():
                end = binaryList.__len__()
            else:
                end = i+64
            temp = binaryList[i:end]
            while temp.__len__()<64:
                temp.append(0)
            result.append(temp)
        return result

    def unpadding(self,listOfList):
        result = []
        for a in listOfList:
            for b in a:
                result.append(b)
        return result

    def binaryListToList(self,bl):
        result = []
        for i in range(0,bl.__len__(),8):
            temp = ""
            for g in range(0,8):
                temp = temp + str(bl[i+g])
            result.append(int(temp,2))
        return result

    def listToData(self,lst):
        result = []
        for i in range(0,lst.__len__(),3):
            result.append((lst[i],lst[i+1],lst[i+2]))
        return result

    def listRGBToData(self,R,G,B):
        result = []
        for i in range(0,R.__len__()):
            result.append((R[i],G[i],B[i]))
        return result

    def handleEntireImage(self):
        a = self.getEntireImageToList()
        a = self.listToBinaryList(a)
        a = self.padding(a)
        return a

    def handleEntireListToEntireImage(self,a):
        a = ir.unpadding(a)
        a = ir.binaryListToList(a)
        a = ir.listToData(a)
        return a

from BlockCipher import BlockCipherAgent
ir = imageReader()
bca = BlockCipherAgent()
def saveNewImage(a,name):
    tm = Image.new('RGB',(512,512))
    tm.putdata(a)
    tm.save(name)
"""
a = ir.openImgAndGetData()
a = ir.handleEntireImage()

bca.setInput(a)
bca.setMode(bca.CBC_MODE)
a = bca.encryption()
bca.setMode(bca.OFB_MODE)
b = bca.encryption()
bca.setMode(bca.CTR_MODE)
c = bca.encryption()

a = ir.handleEntireListToEntireImage(a)
b = ir.handleEntireListToEntireImage(b)
c = ir.handleEntireListToEntireImage(c)



saveNewImage(a,'result2.bmp')
saveNewImage(b,'result3.bmp')
saveNewImage(c,'result4.bmp')"""
def rgbhanleImage(outputname,mode,name = 'test.bmp'):
    a = ir.openImgAndGetData(name)
    r = ir.getChannelToList(ir.R)
    g = ir.getChannelToList(ir.G)
    b = ir.getChannelToList(ir.B)
    r = ir.listToBinaryList(r)
    g = ir.listToBinaryList(g)
    b = ir.listToBinaryList(b)
    r = ir.padding(r)
    g = ir.padding(g)
    b = ir.padding(b)
    bca.setInput(r)
    bca.setMode(mode)
    r = bca.encryption()
    bca.setInput(g)
    g = bca.encryption()
    bca.setInput(b)
    b = bca.encryption()
    r = ir.unpadding(r)
    g = ir.unpadding(g)
    b = ir.unpadding(b)
    r = ir.binaryListToList(r)
    g = ir.binaryListToList(g)
    b = ir.binaryListToList(b)
    saveNewImage(ir.listRGBToData(r,g,b),outputname)

rgbhanleImage("result7.bmp",bca.OFB_MODE)
rgbhanleImage("result8.bmp",bca.CTR_MODE)