inputText = "Look at them, they come to this place when they know they are not pure. Tenno use the keys, but they are mere trespassers. Only I, Vor, know the true power of the Void. I was cut in half, destroyed, but through it's Janus Key, the Void called to me. It brought me here and here I was reborn. We cannot blame these creatures, they are being led by a false prophet, an impostor who knows not the secrets of the Void. Behold the Tenno, come to scavenge and desecrate this sacred realm. My brothers, did I not tell of this day? Did I not prophesize this moment? Now, I will stop them. Now I am changed, reborn through the energy of the Janus Key. Forever bound to the Void. Let it be known, if the Tenno want true salvation, they will lay down their arms, and wait for the baptism of my Janus key. It is time. I will teach these trespassers the redemptive power of my Janus key. They will learn it's simple truth. The Tenno are lost, and they will resist. But I, Vor, will cleanse this place of their impurity."



class ReducerXScheme:
    def __init__(self, reducerID, reducerLen, includedLetters):
        self.start = int(reducerID * reducerLen)
        self.stop = int(self.start + reducerLen)
        self.scheme = []

        for x in range(self.start, self.stop):
            self.scheme.append(includedLetters[x])


def calculateReducerScheme(reducerAmount):
    includedLetters = ["a", "A", "b", "B", "c", "C", "d", "D", "e", "E", "f", "F", "g", "G", "h", "H", "i", "I", "j", "J", "k", "K", "l", "L", "m", "M", "n", "N", "o", "O", "p", "P", "q", "Q", "r", "R", "s", "S", "t", "T", "u", "U", "v", "V", "w", "W", "x", "X", "y", "Y", "z", "Z"]

    reducerLen = len(includedLetters)/reducerAmount

    resReducerScheme = []
    i = 0
    while i < (reducerAmount-1):
        reducerXScheme = ReducerXScheme(i, reducerLen, includedLetters).scheme
        resReducerScheme.append(reducerXScheme)
        i = i+1
    
    return resReducerScheme

reducerScheme = calculateReducerScheme(2)