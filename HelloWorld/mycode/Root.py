import numpy as np


class Root(object):
    def __init__(self, Whichone, Blocksize, Sbox_bit, Sbox_content, Matrix):
        self.Blocksize = Blocksize
        self.HalfofBlocksize = self.Blocksize / 2
        self.Sbox_bit = Sbox_bit
        self.Sbox_content = Sbox_content
        self.Matrix = Matrix
        self.Whichone = Whichone
        if self.Whichone == 'SPN':
            self.DDT = []
            self.G_DDT()
            self.LAT = []
            self.G_LAT()
        elif self.Whichone == 'Feistel':
            self.DDT = []
            self.G_DDT()
            self.LAT = []
            self.G_LAT()
        elif self.Whichone == 'SIMON':
            self.DDT = []
            self.SIMON_DDT()
            self.LAT = []
            self.SIMON_LAT()
        elif self.Whichone == 'SPECK':
            pass
        elif self.Whichone == 'G_Feistel':
            self.DDT = []
            self.G_DDT()
            self.LAT = []
            self.G_LAT()


    def cyclic_left_shift(self, Var, Num):
        if Num == 0 or Num == self.HalfofBlocksize:
            return "{0}".format(Var)
        else:
            return "({0}[{1}:0]@{0}[{2}:{3}])".format(Var, self.HalfofBlocksize - Num - 1, self.HalfofBlocksize - 1,
                                                      self.HalfofBlocksize - Num)

    def cyclic_right_shift(self, Var, Num):
        if Num == 0 or Num == self.HalfofBlocksize:
            return "{0}".format(Var)
        else:
            return "({0}[{1}:0]@{0}[{2}:{3}])".format(Var, Num - 1, self.HalfofBlocksize - 1, Num)

    def Xor(self, Var1, Var2):
        return "BVXOR({0},{1})".format(Var1, Var2)

    def SIMON_DDT(self):
        DDT = [[0 for i in range(pow(2, 1))] for j in range(pow(2, 2))]

        for dif_x in range(pow(2, 2)):
            for x in range(pow(2, 1)):
                the_other_x = dif_x ^ x
                y = self.Sbox_content[x]
                the_other_y = self.Sbox_content[the_other_x]
                dif_y = y ^ the_other_y
                DDT[dif_x][dif_y] += 1

        for i in range(pow(2, 2)):
            for j in range(pow(2, 1)):
                if DDT[i][j] == 0:
                    self.DDT.append(f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);")
                else:
                    self.DDT.append(f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin1);")

    def SIMON_LAT(self):
        LAT = [[0 for i in range(pow(2, 1))] for j in range(pow(2, 2))]

        for S_in in range(pow(2, 2)):
            S_out = self.Sbox_content[S_in]
            for Alpha in range(pow(2, 2)):
                for Beta in range(pow(2, 1)):
                    a = self.Bitxor(S_in, Alpha)
                    b = self.Bitxor(S_out, Beta)
                    if a == b:
                        LAT[Alpha][Beta] += 1

        for i in range(pow(2, 2)):
            for j in range(pow(2, 1)):
                if LAT[i][j] == (pow(2, 2) / 2):
                    self.LAT.append(f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);")
                else:
                    self.LAT.append(f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin1);")


    def G_DDT(self):
        DDT = [[0 for i in range(pow(2, self.Sbox_bit))] for j in range(pow(2, self.Sbox_bit))]

        for dif_x in range(pow(2, self.Sbox_bit)):
            for x in range(pow(2, self.Sbox_bit)):
                the_other_x = dif_x ^ x
                y = self.Sbox_content[x]
                the_other_y = self.Sbox_content[the_other_x]
                dif_y = y ^ the_other_y
                DDT[dif_x][dif_y] += 1

        for i in range(pow(2, self.Sbox_bit)):
            for j in range(pow(2, self.Sbox_bit)):
                if DDT[i][j] == 0:
                    self.DDT.append(f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);")
                else:
                    self.DDT.append(f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin1);")

    def Bitxor(self, n, mask):
        bitlist = [int(x) for x in bin(n & mask)[2:]]
        return bitlist.count(1) % 2

    def G_LAT(self):
        LAT = [[0 for i in range(pow(2, self.Sbox_bit))] for j in range(pow(2, self.Sbox_bit))]

        for S_in in range(pow(2, self.Sbox_bit)):
            S_out = self.Sbox_content[S_in]
            for Alpha in range(pow(2, self.Sbox_bit)):
                for Beta in range(pow(2, self.Sbox_bit)):
                    a = self.Bitxor(S_in, Alpha)
                    b = self.Bitxor(S_out, Beta)
                    if a == b:
                        LAT[Alpha][Beta] += 1

        for i in range(pow(2, self.Sbox_bit)):
            for j in range(pow(2, self.Sbox_bit)):
                if LAT[i][j] == (pow(2, self.Sbox_bit) / 2):
                    self.LAT.append(f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin0);")
                else:
                    self.LAT.append(f"ASSERT(S[0bin{'{:08b}'.format(i) + '{:08b}'.format(j)}] = 0bin1);")

    def DIF_Matrix_mul(self, Input):
        row = len(self.Matrix)
        col = len(self.Matrix[0])
        Output = []

        for i in range(row):
            for j in range(col):
                if self.Matrix[i][j] == 0:
                    continue
                else:
                    Output.append(Input[j])

        return Output

    def Linear_Matrix_mul(self, Input):
        Matrix = np.linalg.inv(self.Matrix)
        row = len(Matrix)
        col = len(Matrix[0])
        Output = []
        for i in range(row):
            for j in range(col):
                if self.Matrix[i][j] == 0:
                    continue
                else:
                    Output.append(Input[j])

        return Output
