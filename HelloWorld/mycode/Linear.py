from .Root import Root
from collections import Counter


# 应该改为输入bit长度和输出bit长度
class DESL_Feistel_Linear(Root):
    def __init__(self, Whichone, Blocksize, Round, Sbox_bit, Sbox_content, Matrix):
        super().__init__(Whichone, Blocksize, Sbox_bit, Sbox_content, Matrix)
        self.Round = Round
        self.HalfofBlocksize = self.Blocksize // 2
        self.sum = []

    def SboxSpecificSubjection(self, inX, outY):
        if self.Sbox_bit != 8:
            eqn = [
                f"ASSERT(NOT(S[{'0bin{0}@{1}@'.format('0' * (8 - self.Sbox_bit), inX) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), outY)}] = 0bin0));"]
            self.sum.append('|'.join(['{0}[{1}:{1}]'.format(inX, i) for i in range(self.Sbox_bit)]))
        else:
            eqn = [f"ASSERT(NOT(S[{'{0}@'.format(inX) + '{0}'.format(outY)}] = 0bin0));"]
            self.sum.append('|'.join(['{0}[{1}:{1}]'.format(inX, i) for i in range(self.Sbox_bit)]))
        return eqn

    def PSpecificSubjection(self, MiddV, outV):
        mid = ["{0}_{1}".format(MiddV, i) for i in range(self.HalfofBlocksize - 1, -1, -1)]
        out = super().Linear_Matrix_mul(mid)
        mid1 = "@".join(mid)
        out1 = "@".join(out)
        eqn = [f"ASSERT({'{0}'.format(MiddV) + '= {0}'.format(mid1)});",
               f"ASSERT({'{0}'.format(outV) + '= {0}'.format(out1)});"]
        return eqn

    def F_Subjection(self, InV, MiddV, OutV):
        eqn = []
        i = self.HalfofBlocksize // self.Sbox_bit
        for num in range(i):
            eqn += self.SboxSpecificSubjection(InV + "[{0}:{1}]".format(self.HalfofBlocksize - 1 - num * self.Sbox_bit,
                                                                        self.HalfofBlocksize - self.Sbox_bit - num * self.Sbox_bit),
                                               MiddV +
                                               "[{0}:{1}]".format(self.HalfofBlocksize - 1 - num * self.Sbox_bit,
                                                                  self.HalfofBlocksize - self.Sbox_bit - num * self.Sbox_bit))
        eqn += self.PSpecificSubjection(MiddV, OutV)
        return eqn

    def middVars_At_Round(self, r):
        assert (r >= 1)
        return 'midd_r' + str(r)

    def L_At_Round(self, r):
        assert (r >= 1)
        return 'L_r' + str(r)

    def F_Out_At_Round(self, r):
        assert (r >= 1)
        return 'fout_r' + str(r)

    def R_At_Round(self, r):
        assert (r >= 1)
        return 'R_r' + str(r)

    def genEncryptSubjectionAtRound(self, r):
        eqn = self.F_Subjection(self.Xor(self.R_At_Round(r), self.L_At_Round(r + 1)), self.middVars_At_Round(r),
                                self.F_Out_At_Round(r))
        eqn += ["ASSERT({0} = {1});".format(self.L_At_Round(r), self.F_Out_At_Round(r))]
        eqn += ["ASSERT({0} = {1});".format(self.F_Out_At_Round(r), self.R_At_Round(r + 1))]
        return eqn

    def genEncrypSubjection(self, totalRound):
        eqn = []
        for i in range(1, totalRound + 1):
            eqn += self.genEncryptSubjectionAtRound(i)
        return eqn

    def getVars(self, r):
        eqn = []

        for i in range(1, r + 2):
            eqn.append(self.L_At_Round(i))
            eqn.append(self.middVars_At_Round(i))
            eqn.append(self.F_Out_At_Round(i))
            eqn.append(self.R_At_Round(i))

        eqn = list(Counter(eqn))

        eqn = [','.join(eqn) + ' : BITVECTOR({0});'.format(self.HalfofBlocksize), 'zonggeshu : BITVECTOR(8);']

        for i in range(1, r + 1):
            eqn.append(','.join(["{0}_{1}".format(self.middVars_At_Round(i), j) for j in
                                 range(self.HalfofBlocksize - 1, -1, -1)]) + ' : BITVECTOR(1);')
        return eqn

class Present_SPN_Linear(Root):
    def __init__(self, Whichone, Blocksize, Round, Sbox_bit, Sbox_content, Matrix):
        super().__init__(Whichone, Blocksize, Sbox_bit, Sbox_content, Matrix)
        self.Round = Round
        self.HalfofBlocksize = self.Blocksize // 2
        self.sum = []

    def SboxSpecificSubjection(self, inX, outY):
        if self.Sbox_bit != 8:
            eqn = [
                f"ASSERT(NOT(S[{'0bin{0}@{1}@'.format('0' * (8 - self.Sbox_bit), inX) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), outY)}] = 0bin0));"]
            self.sum.append('|'.join(['{0}[{1}:{1}]'.format(inX, i) for i in range(self.Sbox_bit)]))
        else:
            eqn = [f"ASSERT(NOT(S[{'{0}@'.format(inX) + '{0}'.format(outY)}] = 0bin0));"]
            self.sum.append('|'.join(['{0}[{1}:{1}]'.format(inX, i) for i in range(self.Sbox_bit)]))
        return eqn

    def PSpecificSubjection(self, MiddV, outV):
        mid = ["{0}_{1}".format(MiddV, i) for i in range(self.Blocksize - 1, -1, -1)]
        out = super().Linear_Matrix_mul(mid)
        mid1 = "@".join(mid)
        out1 = "@".join(out)
        eqn = [f"ASSERT({'{0}'.format(MiddV) + '= {0}'.format(mid1)});",
               f"ASSERT({'{0}'.format(outV) + '= {0}'.format(out1)});"]
        return eqn

    def F_Subjection(self, InV, MiddV, OutV):
        eqn = []
        i = self.Blocksize // self.Sbox_bit
        for num in range(i):
            eqn += self.SboxSpecificSubjection(InV + "[{0}:{1}]".format(self.Blocksize - 1 - num * self.Sbox_bit,
                                                                        self.Blocksize - self.Sbox_bit - num * self.Sbox_bit),
                                               MiddV +
                                               "[{0}:{1}]".format(self.Blocksize - 1 - num * self.Sbox_bit,
                                                                  self.Blocksize - self.Sbox_bit - num * self.Sbox_bit))
        eqn += self.PSpecificSubjection(MiddV, OutV)
        return eqn

    def middVars_At_Round(self, r):
        assert (r >= 1)
        return 'midd_r' + str(r)

    def inVars_At_Round(self, r):
        assert (r >= 1)
        if r == 1:
            return 'in_r' + str(r)
        else:
            return self.Out_At_Round(r - 1)

    def Out_At_Round(self, r):
        assert (r >= 1)
        return 'out_r' + str(r)

    def genEncryptSubjectionAtRound(self, r):
        inF_bits = self.inVars_At_Round(r)
        midd_bits = self.middVars_At_Round(r)
        fout_bits = self.Out_At_Round(r)
        eqn = self.F_Subjection(inF_bits, midd_bits, fout_bits)
        return eqn

    def genEncrypSubjection(self, totalRound):
        eqn = []
        for i in range(1, totalRound + 1):
            eqn += self.genEncryptSubjectionAtRound(i)
        return eqn

    def getVars(self, r):
        eqn = []

        for i in range(1, r + 1):
            eqn.append(self.inVars_At_Round(i))
            eqn.append(self.middVars_At_Round(i))
            eqn.append(self.Out_At_Round(i))

        eqn = list(Counter(eqn))

        eqn = [','.join(eqn) + ' : BITVECTOR({0});'.format(self.Blocksize), 'zonggeshu : BITVECTOR(8);']

        for i in range(1, r + 1):
            eqn.append(','.join(["{0}_{1}".format(self.middVars_At_Round(i), j) for j in
                                 range(self.Blocksize - 1, -1, -1)]) + ' : BITVECTOR(1);')
        return eqn

class SIMON_Linear(Root):
    def __init__(self, Whichone, Blocksize, Round, Sbox_bit, Sbox_content, Matrix):
        super().__init__(Whichone, Blocksize, Sbox_bit, Sbox_content, Matrix)
        self.Round = Round
        self.HalfofBlocksize = self.Blocksize // 2
        self.sum = []

    def SboxSpecificSubjection(self, inX, outY):
        if self.Sbox_bit != 8:
            eqn = [
                f"ASSERT(NOT(S[{'0bin{0}@{1}@'.format('0' * (8 - 2), inX) + '0bin{0}@{1}'.format('0' * (8 - 1), outY)}] = 0bin0));"]
            self.sum.append('|'.join(['{0}[{1}:{1}]'.format(inX, i) for i in range(2)]))
        else:
            eqn = [f"ASSERT(NOT(S[{'{0}@'.format(inX) + '{0}'.format(outY)}] = 0bin0));"]
            self.sum.append('|'.join(['{0}[{1}:{1}]'.format(inX, i) for i in range(2)]))
        return eqn

    def F_Subjection(self, InV1, InV2, OutV):
        eqn = []
        for num in range(32):
            eqn += self.SboxSpecificSubjection("(" + InV1 + "[{0}:{0}]@".format(num) + InV2 + "[{0}:{0}]".format(num)+ ")",
                                               OutV +
                                               "[{0}:{0}]".format(num))
        return eqn

    def midd1Vars_At_Round(self, r):
        assert (r >= 1)
        return 'midd1_r' + str(r)

    def midd2Vars_At_Round(self, r):
        assert (r >= 1)
        return 'midd2_r' + str(r)

    def midd3Vars_At_Round(self, r):
        assert (r >= 1)
        return 'midd3_r' + str(r)

    def L_At_Round(self, r):
        assert (r >= 1)
        if r == 1:
            return 'L_r' + str(r)
        else:
            return self.R_At_Round(r - 1)

    def F_Out_At_Round(self, r):
        assert (r >= 1)
        return 'fout_r' + str(r)

    def R_At_Round(self, r):
        assert (r >= 1)
        return 'R_r' + str(r)

    def rotXorOut_At_Round(self, r):
        assert (r >= 1)
        return self.R_At_Round(r + 1)

    def genEncryptSubjectionAtRound(self, r):
        eqn = []
        inF_bits = self.L_At_Round(r)
        midd1_bits = self.midd1Vars_At_Round(r)
        midd2_bits = self.midd2Vars_At_Round(r)
        midd3_bits = self.midd3Vars_At_Round(r)
        fout_bits = self.F_Out_At_Round(r)
        right_bits = self.R_At_Round(r)
        rotout_bits = self.rotXorOut_At_Round(r)
        eqn += ["ASSERT({0} = ".format(midd2_bits) + self.Xor(inF_bits, midd1_bits) + ');']
        eqn = self.F_Subjection(self.cyclic_left_shift(midd1_bits,1), self.cyclic_left_shift(midd2_bits,8), right_bits)
        eqn += ["ASSERT({0} = {1});".format(midd3_bits,right_bits)]
        eqn += ["ASSERT({0} = ".format(rotout_bits) + self.Xor(self.cyclic_left_shift(midd3_bits,2), inF_bits) + ');']
        return eqn

    def genEncrypSubjection(self, totalRound):
        eqn = []
        for i in range(1, totalRound + 1):
            eqn += self.genEncryptSubjectionAtRound(i)
        return eqn

    def getVars(self, r):
        eqn = []

        for i in range(1, r + 1):
            eqn.append(self.L_At_Round(i))
            eqn.append(self.midd1Vars_At_Round(i))
            eqn.append(self.midd2Vars_At_Round(i))
            eqn.append(self.midd3Vars_At_Round(i))
            eqn.append(self.F_Out_At_Round(i))
            eqn.append(self.R_At_Round(i))
            eqn.append(self.rotXorOut_At_Round(i))

        eqn = list(Counter(eqn))

        eqn = [','.join(eqn) + ' : BITVECTOR({0});'.format(self.HalfofBlocksize), 'zonggeshu : BITVECTOR(8);']

        return eqn

class SPECK_Linear(Root):
    def __init__(self, Whichone, Blocksize, Round, Sbox_bit, Sbox_content, Matrix):
        super().__init__(Whichone, Blocksize, Sbox_bit, Sbox_content, Matrix)
        self.Round = Round
        self.HalfofBlocksize = self.Blocksize // 2
        self.sum = []

    def L_At_Round(self, r):
        assert (r >= 1)
        return 'L_r' + str(r)

    def R_At_Round(self, r):
        assert (r >= 1)
        return 'R_r' + str(r)

    def XorOut_At_Round(self, r):
        assert (r >= 1)
        return self.R_At_Round(r + 1)

    def ModuloOut_At_Round(self, r):
        assert (r >= 1)
        return self.L_At_Round(r + 1)

    def S_zhi_At_Round(self, r):
        assert (r >= 1)
        return 's_r' + str(r)

    def shift(self, A, num):
        if num != 0 or num != 32:
            return "({0} << {1})[31:0]".format(A, num)
        else:
            return "{0}".format(A)

    def linear_conditions_addition(self, a1, a2, b, s):
        constraints = []
        for i in range(self.HalfofBlocksize ):
            constraints = constraints + [
                'ASSERT(BVGE(BVPLUS({0}, 0bin00@({1}[{5}:{5}]),0bin00@({4}[{6}:{6}]),0bin00@({1}[{6}:{6}])), BVPLUS({0},0bin00@({2}[{6}:{6}]),0bin00@({3}[{6}:{6}]))));'.format(
                    3, s, b, a1, a2, i + 1, i)]
            constraints = constraints + [
                'ASSERT(BVGE(BVPLUS({0}, 0bin00@({1}[{5}:{5}]),0bin00@({2}[{6}:{6}]),0bin00@({1}[{6}:{6}])), BVPLUS({0},0bin00@({3}[{6}:{6}]),0bin00@({4}[{6}:{6}]))));'.format(
                    3, s, b, a1, a2, i + 1, i)]
            constraints = constraints + [
                'ASSERT(BVGE(BVPLUS({0}, 0bin00@({1}[{5}:{5}]),0bin00@({2}[{6}:{6}]),0bin00@({4}[{6}:{6}])), BVPLUS({0},0bin00@({3}[{6}:{6}]),0bin00@({1}[{6}:{6}]))));'.format(
                    3, s, b, a1, a2, i + 1, i)]
            constraints = constraints + [
                'ASSERT(BVGE(BVPLUS({0}, 0bin00@({2}[{6}:{6}]),0bin00@({3}[{6}:{6}]),0bin00@({4}[{6}:{6}]),0bin00@({1}[{6}:{6}])), 0bin00@({1}[{5}:{5}])));'.format(
                    3, s, b, a1, a2, i + 1, i)]
            constraints = constraints + [
                'ASSERT(BVGE(BVPLUS({0}, 0bin00@({1}[{5}:{5}]),0bin00@({2}[{6}:{6}]),0bin00@({3}[{6}:{6}])), BVPLUS({0},0bin00@({4}[{6}:{6}]),0bin00@({1}[{6}:{6}]))));'.format(
                    3, s, b, a1, a2, i + 1, i)]
            constraints = constraints + [
                'ASSERT(BVGE(BVPLUS({0}, 0bin00@({1}[{5}:{5}]),0bin00@({3}[{6}:{6}]),0bin00@({1}[{6}:{6}])), BVPLUS({0},0bin00@({2}[{6}:{6}]),0bin00@({4}[{6}:{6}]))));'.format(
                    3, s, b, a1, a2, i + 1, i)]
            constraints = constraints + [
                'ASSERT(BVGE(BVPLUS({0}, 0bin00@({1}[{5}:{5}]),0bin00@({3}[{6}:{6}]),0bin00@({4}[{6}:{6}])), BVPLUS({0},0bin00@({2}[{6}:{6}]),0bin00@({1}[{6}:{6}]))));'.format(
                    3, s, b, a1, a2, i + 1, i)]
            constraints = constraints + [
                'ASSERT(BVLE(BVPLUS({0}, 0bin00@({1}[{5}:{5}]),0bin00@({2}[{6}:{6}]),0bin00@({3}[{6}:{6}]),0bin00@({4}[{6}:{6}]),0bin00@({1}[{6}:{6}])), 0bin100));'.format(
                    3, s, b, a1, a2, i + 1, i)]

        constraints = constraints + ['ASSERT({0}[{1}:{1}] = 0bin0);'.format(s, self.HalfofBlocksize )]
        return constraints

    def F_Subjection(self, A, B, C, S):
        eqn = []
        eqn += self.linear_conditions_addition(A, B, C, S)
        return eqn


    def genEncryptSubjectionAtRound(self, r):
        eqn = []
        inF_bits = self.L_At_Round(r)
        right_bits = self.R_At_Round(r)
        Xorout_bits = self.XorOut_At_Round(r)
        Moduloout_bits = self.ModuloOut_At_Round(r)
        s = self.S_zhi_At_Round(r)
        eqn += self.F_Subjection(self.cyclic_right_shift(inF_bits, 8), self.Xor(right_bits, self.cyclic_right_shift(Xorout_bits, 3)), self.Xor(Moduloout_bits, Xorout_bits), s)

        return eqn

    def genEncrypSubjection(self, totalRound):
        eqn = []
        for i in range(1, totalRound + 1):
            eqn += self.genEncryptSubjectionAtRound(i)
        return eqn

    def getVars(self, r):
        eqn = []

        for i in range(1, r + 1):
            eqn.append(self.L_At_Round(i))
            eqn.append(self.R_At_Round(i))
            eqn.append(self.XorOut_At_Round(i))
            eqn.append(self.ModuloOut_At_Round(i))

        eqn = [','.join(list(Counter(eqn).keys())) + ' : BITVECTOR(32);']

        eqn1 = []

        for i in range(1, r + 1):
            eqn1.append(self.S_zhi_At_Round(i))

        eqn1 = [','.join(list(Counter(eqn1).keys())) + ' : BITVECTOR(33);']

        eqn += eqn1

        return eqn

class G_Feistel_Linear(Root):
    def __init__(self, Whichone, Blocksize, Round, Sbox_bit, Sbox_content, Matrix):
        super().__init__(Whichone, Blocksize, Sbox_bit, Sbox_content, Matrix)
        self.Matrix = Matrix
        self.Round = Round
        self.onefBlocksize = self.Blocksize // 16
        self.sum = []

    def SboxSpecificSubjection(self, inX, outY):
        if self.Sbox_bit != 8:
            eqn = [
                f"ASSERT(NOT(S[{'0bin{0}@{1}@'.format('0' * (8 - self.Sbox_bit), inX) + '0bin{0}@{1}'.format('0' * (8 - self.Sbox_bit), outY)}] = 0bin0));"]
            self.sum.append('|'.join(['{0}[{1}:{1}]'.format(inX, i) for i in range(self.Sbox_bit)]))
        else:
            eqn = [f"ASSERT(NOT(S[{'{0}@'.format(inX) + '{0}'.format(outY)}] = 0bin0));"]
            self.sum.append('|'.join(['{0}[{1}:{1}]'.format(inX, i) for i in range(self.Sbox_bit)]))
        return eqn

    def F_Subjection(self, InV, MiddV):
        eqn = []
        eqn += self.SboxSpecificSubjection(InV, MiddV)
        return eqn

    def Out_At_Round(self, r):
        assert (r >= 1)
        return 'Out_r' + str(r)

    def In_At_Round(self, r):
        assert (r >= 1)
        return 'In_r' + str(r)

    def ano_At_Round_4(self, r):
        assert (r >= 1)
        eqn = []
        for i in range(16):
            eqn.append("In_r{0}_{1}".format(r + 1, i))
        return eqn

    def In_At_Round_4(self, r):
        assert (r >= 1)
        eqn = []
        for i in range(16):
            eqn.append("In_r{0}_{1}".format(r, i))
        return eqn

    def Out_At_Round_4(self, r):
        assert (r >= 1)
        eqn = []
        for i in range(16):
            eqn.append("Out_r{0}_{1}".format(r, i))
        return eqn

    def genEncryptSubjectionAtRound(self, r):
        eqn = []
        inF_bits = self.In_At_Round(r)
        ano_bits = self.ano_At_Round_4(r)
        midd_bits = self.Out_At_Round(r)
        fout_bits = self.In_At_Round_4(r)
        right_bits = self.Out_At_Round_4(r)
        for i in range(8):
            eqn += self.F_Subjection(self.Xor(fout_bits[2 * i], fout_bits[2 * i]), right_bits[i * 2 + 1])
        for i in range(8):
            eqn.append("ASSERT({0} = {1});".format(fout_bits[i*2 + 1], right_bits[i*2 + 1]))
        eqn.append("ASSERT(" + inF_bits + "=" + "@".join(fout_bits) + ");")
        eqn.append("ASSERT(" + midd_bits + "=" + "@".join(right_bits) + ");")
        if (r < self.Round):
            for i in range(16):
                eqn.append("ASSERT(" + ano_bits[self.Matrix[i]] + "=" + right_bits[i] + ");")
        return eqn

    def genEncrypSubjection(self, totalRound):
        eqn = []
        for i in range(1, totalRound + 1):
            eqn += self.genEncryptSubjectionAtRound(i)
        return eqn

    def getVars(self, r):
        eqn = []
        eqn1 = []

        for i in range(1, r + 1):
            eqn.append(self.In_At_Round(i))
            eqn.append(self.Out_At_Round(i))

        for i in range(1, r + 1):
            eqn1 += self.In_At_Round_4(i)
            eqn1 += self.Out_At_Round_4(i)

        eqn = list(Counter(eqn))

        eqn1 = list(Counter(eqn1))

        eqn = [','.join(eqn) + ' : BITVECTOR(64);', 'zonggeshu : BITVECTOR(8);']

        eqn += [','.join(eqn1) + ' : BITVECTOR(4);']

        return eqn