from . import DIF
from . import Linear


class test():
    def __init__(self, Whichone, Blocksize, Round, Sbox_bit, Sbox_content, Matrix):
        self.HalfBlocksize = Blocksize // 2
        if Whichone == 'SPN':
            self.MySPNDIF = DIF.Present_SPN_DIF(Whichone, Blocksize, Round, Sbox_bit, Sbox_content, Matrix)
            self.MySPNLinear = Linear.Present_SPN_Linear(Whichone, Blocksize, Round, Sbox_bit, Sbox_content, Matrix)
        elif Whichone == 'Feistel':
            self.MyFeistelDIF = DIF.DESL_Feistel_DIF(Whichone, Blocksize, Round, Sbox_bit, Sbox_content, Matrix)
            self.MyFeistelLinear = Linear.DESL_Feistel_Linear(Whichone, Blocksize, Round, Sbox_bit, Sbox_content,
                                                              Matrix)
        elif Whichone == 'SIMON':
            self.MySIMONDIF = DIF.SIMON_DIF(Whichone, Blocksize, Round, Sbox_bit, Sbox_content, Matrix)
            self.MySIMONLinear = Linear.SIMON_Linear(Whichone, Blocksize, Round, Sbox_bit, Sbox_content, Matrix)
        elif Whichone == 'SPECK':
            self.MySPECKDIF = DIF.SPECK_DIF(Whichone, Blocksize, Round, Sbox_bit, Sbox_content, Matrix)
            self.MySPECKLinear = Linear.SPECK_Linear(Whichone, Blocksize, Round, Sbox_bit, Sbox_content, Matrix)
        elif Whichone == 'G_Feistel':
            self.MyG_FeistelDIF = DIF.G_Feistel_DIF(Whichone, Blocksize, Round, Sbox_bit, Sbox_content, Matrix)
            self.MyG_FeistelLinear = Linear.G_Feistel_Linear(Whichone, Blocksize, Round, Sbox_bit, Sbox_content,
                                                             Matrix)


    def FeistelDIFanalyse(self,S_num):
        DIFresult1 = self.MyFeistelDIF.genEncrypSubjection(self.MyFeistelDIF.Round)
        DIFresult2 = self.MyFeistelDIF.getVars(self.MyFeistelDIF.Round)
        DIFlp_file = r"/home/giantbranch/Desktop/DIF.cvc"
        with open(DIFlp_file, 'a') as OFile:
            OFile.seek(0)
            OFile.truncate()

            OFile.write('S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n')

            for i in self.MyFeistelDIF.DDT:
                OFile.write(i + '\n')

            for i in DIFresult2:
                OFile.write(i + '\n')

            for i in DIFresult1:
                OFile.write(i + '\n')

            OFile.write('ASSERT(BVPLUS(8,' + ','.join(['0bin0000000@(%s)' % (self.MyFeistelDIF.sum[i]) for i in range(
                self.MyFeistelDIF.Round * 8)]) + ')' + ' = ' + 'zonggeshu' + ');' + '\n')

            OFile.write('ASSERT(BVLE(zonggeshu,0bin' + bin(S_num)[2:].zfill(8) + '));\n')
            OFile.write('ASSERT(BVGT(R_r1 , ' + '0bin' + '0' * 32 + '));' + '\n')

            OFile.write('QUERY FALSE; \n')
            OFile.write('COUNTEREXAMPLE; \n')

            OFile.close()

    def FeistelLinearanalyse(self,S_num):
        Linearresult1 = self.MyFeistelLinear.genEncrypSubjection(self.MyFeistelLinear.Round)
        Linearresult2 = self.MyFeistelLinear.getVars(self.MyFeistelLinear.Round)
        Linearlp_file = r"/home/giantbranch/Desktop/Linear.cvc"
        with open(Linearlp_file, 'a') as OFile:
            OFile.seek(0)
            OFile.truncate()

            OFile.write('S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n')

            for i in self.MyFeistelLinear.LAT:
                OFile.write(i + '\n')

            for i in Linearresult2:
                OFile.write(i + '\n')

            for i in Linearresult1:
                OFile.write(i + '\n')

            OFile.write('ASSERT(BVPLUS(8,' + ','.join(['0bin0000000@(%s)' % (self.MyFeistelLinear.sum[i]) for i in range(
                self.MyFeistelLinear.Round * 8)]) + ')' + ' = ' + 'zonggeshu' + ');' + '\n')

            OFile.write('ASSERT(BVLE(zonggeshu,0bin' + bin(S_num)[2:].zfill(8) + '));\n')
            OFile.write('ASSERT(BVGT(R_r1 , ' + '0bin' + '0' * 32 + '));' + '\n')

            OFile.write('QUERY FALSE; \n')
            OFile.write('COUNTEREXAMPLE; \n')

            OFile.close()

    def SPNDIFanalyse(self,S_num):
        DIFresult1 = self.MySPNDIF.genEncrypSubjection(self.MySPNDIF.Round)
        DIFresult2 = self.MySPNDIF.getVars(self.MySPNDIF.Round)
        DIFlp_file = r"/home/giantbranch/Desktop/DIF.cvc"
        with open(DIFlp_file, 'a') as OFile:
            OFile.seek(0)
            OFile.truncate()

            OFile.write('S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n')

            for i in self.MySPNDIF.DDT:
                OFile.write(i + '\n')

            for i in DIFresult2:
                OFile.write(i + '\n')

            for i in DIFresult1:
                OFile.write(i + '\n')

            OFile.write('ASSERT(BVPLUS(8,' + ','.join(['0bin0000000@(%s)' % (self.MySPNDIF.sum[i]) for i in range(
                self.MySPNDIF.Round * 16)]) + ')' + ' = ' + 'zonggeshu' + ');' + '\n')

            OFile.write('ASSERT(BVLE(zonggeshu,0bin' + bin(S_num)[2:].zfill(8) + '));\n')
            OFile.write('ASSERT(BVGT(in_r1 , ' + '0bin' + '0' * 64 + '));' + '\n')

            OFile.write('QUERY FALSE; \n')
            OFile.write('COUNTEREXAMPLE; \n')

            OFile.close()

    def SPNLinearanalyse(self,S_num):
        Linearresult1 = self.MySPNLinear.genEncrypSubjection(self.MySPNLinear.Round)
        Linearresult2 = self.MySPNLinear.getVars(self.MySPNLinear.Round)
        Linearlp_file = r"/home/giantbranch/Desktop/Linear.cvc"
        with open(Linearlp_file, 'a') as OFile:
            OFile.seek(0)
            OFile.truncate()

            OFile.write('S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n')

            for i in self.MySPNLinear.LAT:
                OFile.write(i + '\n')

            for i in Linearresult2:
                OFile.write(i + '\n')

            for i in Linearresult1:
                OFile.write(i + '\n')

            OFile.write('ASSERT(BVPLUS(8,' + ','.join(
                ['0bin0000000@(%s)' % (self.MySPNLinear.sum[i]) for i in range(
                    self.MySPNLinear.Round * 16)]) + ')' + ' = ' + 'zonggeshu' + ');' + '\n')

            OFile.write('ASSERT(BVLE(zonggeshu,0bin' + bin(S_num)[2:].zfill(8) + '));\n')
            OFile.write('ASSERT(BVGT(in_r1 , ' + '0bin' + '0' * 64 + '));' + '\n')

            OFile.write('QUERY FALSE; \n')
            OFile.write('COUNTEREXAMPLE; \n')

            OFile.close()

    def SIMONDIFanalyse(self,S_num):
        DIFresult1 = self.MySIMONDIF.genEncrypSubjection(self.MySIMONDIF.Round)
        DIFresult2 = self.MySIMONDIF.getVars(self.MySIMONDIF.Round)
        DIFlp_file = r"/home/giantbranch/Desktop/DIF.cvc"
        with open(DIFlp_file, 'a') as OFile:
            OFile.seek(0)
            OFile.truncate()

            OFile.write('S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n')

            for i in self.MySIMONDIF.DDT:
                OFile.write(i + '\n')

            for i in DIFresult2:
                OFile.write(i + '\n')

            for i in DIFresult1:
                OFile.write(i + '\n')

            OFile.write('ASSERT(BVPLUS(8,' + ','.join(['0bin0000000@(%s)' % (self.MySIMONDIF.sum[i]) for i in range(
                self.MySIMONDIF.Round * 8)]) + ')' + ' = ' + 'zonggeshu' + ');' + '\n')

            OFile.write('ASSERT(BVLE(zonggeshu,0bin' + bin(S_num)[2:].zfill(8) + '));\n')
            OFile.write('ASSERT(BVGT(L_r1 , ' + '0bin' + '0' * 32 + '));' + '\n')

            OFile.write('QUERY FALSE; \n')
            OFile.write('COUNTEREXAMPLE; \n')

            OFile.close()

    def SIMONLinearanalyse(self,S_num):
        Linearresult1 = self.MySIMONLinear.genEncrypSubjection(self.MySIMONLinear.Round)
        Linearresult2 = self.MySIMONLinear.getVars(self.MySIMONLinear.Round)
        Linearlp_file = r"/home/giantbranch/Desktop/Linear.cvc"
        with open(Linearlp_file, 'a') as OFile:
            OFile.seek(0)
            OFile.truncate()

            OFile.write('S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n')

            for i in self.MySIMONLinear.LAT:
                OFile.write(i + '\n')

            for i in Linearresult2:
                OFile.write(i + '\n')

            for i in Linearresult1:
                OFile.write(i + '\n')

            OFile.write('ASSERT(BVPLUS(8,' + ','.join(['0bin0000000@(%s)' % (self.MySIMONLinear.sum[i]) for i in range(
                self.MySIMONLinear.Round * 8)]) + ')' + ' = ' + 'zonggeshu' + ');' + '\n')

            OFile.write('ASSERT(BVLE(zonggeshu,0bin' + bin(S_num)[2:].zfill(8) + '));\n')
            OFile.write('ASSERT(BVGT(R_r1 , ' + '0bin' + '0' * 32 + '));' + '\n')
            OFile.write('QUERY FALSE; \n')
            OFile.write('COUNTEREXAMPLE; \n')

            OFile.close()

    def SPECKDIFanalyse(self, S_num):
        DIFresult1 = self.MySPECKDIF.genEncrypSubjection(self.MySPECKDIF.Round)
        DIFresult2 = self.MySPECKDIF.getVars(self.MySPECKDIF.Round)
        DIFlp_file = r"/home/giantbranch/Desktop/DIF.cvc"
        with open(DIFlp_file, 'a') as OFile:
            OFile.seek(0)
            OFile.truncate()

            for i in DIFresult2:
                OFile.write(i + '\n')

            for i in DIFresult1:
                OFile.write(i + '\n')

            OFile.write('ASSERT(BVGT(L_r1@R_r1 , ' + '0hex' + '0' * 16 + '));' + '\n')

            Cunjieguo = []
            for i in range(1, self.MySPECKDIF.Round + 1):
                for j in range(0, 31):
                    Cunjieguo.append('0bin000000000000000@w_r%s[%s:%s]' % (i, j, j))

            OFile.write(
                'ASSERT(BVPLUS(16,' + ','.join(Cunjieguo) + ')' + ' = ' + '0bin' + bin(S_num)[2:].zfill(16) + ');' + '\n')

            OFile.write('QUERY FALSE; \n')
            OFile.write('COUNTEREXAMPLE; \n')

            OFile.close()

    def SPECKLinearanalyse(self, S_num):
        Linearresult1 = self.MySPECKLinear.genEncrypSubjection(self.MySPECKLinear.Round)
        Linearresult2 = self.MySPECKLinear.getVars(self.MySPECKLinear.Round)
        Linearlp_file = r"/home/giantbranch/Desktop/Linear.cvc"
        with open(Linearlp_file, 'a') as OFile:
            OFile.seek(0)
            OFile.truncate()

            for i in Linearresult2:
                OFile.write(i + '\n')

            for i in Linearresult1:
                OFile.write(i + '\n')

            OFile.write('ASSERT(BVGT(L_r1@R_r1 , ' + '0hex' + '0' * 16 + '));' + '\n')

            command = 'ASSERT(BVPLUS(16,'
            for i in range(1, self.MySPECKLinear.Round + 1):
                for j in range(1, self.HalfBlocksize):
                    if i == self.MySPECKLinear.Round and j == (self.HalfBlocksize - 1):
                        command += '0bin000000000000000@s_r' + str(i) + '[' + str(j) + ':' + str(
                            j) + ']' + ') = 0bin' + bin(S_num)[2:].zfill(16) +');'
                    else:
                        command += '0bin000000000000000@s_r' + str(i) + '[' + str(j) + ':' + str(j) + ']' + ','

            OFile.write(command + '\n')

            OFile.write('QUERY FALSE; \n')
            OFile.write('COUNTEREXAMPLE; \n')

            OFile.close()

    def G_FeistelDIFanalyse(self, S_num):
        DIFresult1 = self.MyG_FeistelDIF.genEncrypSubjection(self.MyG_FeistelDIF.Round)
        DIFresult2 = self.MyG_FeistelDIF.getVars(self.MyG_FeistelDIF.Round)
        DIFlp_file = r"/home/giantbranch/Desktop/DIF.cvc"
        with open(DIFlp_file, 'a') as OFile:
            OFile.seek(0)
            OFile.truncate()

            OFile.write('S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n')

            for i in self.MyG_FeistelDIF.DDT:
                OFile.write(i + '\n')

            for i in DIFresult2:
                OFile.write(i + '\n')

            for i in DIFresult1:
                OFile.write(i + '\n')

            OFile.write('ASSERT(BVGT(In_r1 , ' + '0hex' + '0' * 16 + '));' + '\n')

            OFile.write(
                'ASSERT(BVPLUS(8,' + ','.join(['0bin0000000@(%s)' % (self.MyG_FeistelDIF.sum[i]) for i in range(
                    self.MyG_FeistelDIF.Round * 8)]) + ')' + ' = ' + 'zonggeshu' + ');' + '\n')
            
            OFile.write('ASSERT(BVLE(zonggeshu,0bin' + bin(S_num)[2:].zfill(8) + '));\n')
            # OFile.write('ASSERT(BVGT(R_r1 , ' + '0bin' + '0' * 32 + '));' + '\n')

            OFile.write('QUERY FALSE; \n')
            OFile.write('COUNTEREXAMPLE; \n')

            OFile.close()

    def G_FeistelLinearanalyse(self,S_num):
        Linearresult1 = self.MyG_FeistelLinear.genEncrypSubjection(self.MyG_FeistelLinear.Round)
        Linearresult2 = self.MyG_FeistelLinear.getVars(self.MyG_FeistelLinear.Round)
        Linearlp_file = r"/home/giantbranch/Desktop/Linear.cvc"
        with open(Linearlp_file, 'a') as OFile:
            OFile.seek(0)
            OFile.truncate()

            OFile.write('S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n')

            for i in self.MyG_FeistelLinear.LAT:
                OFile.write(i + '\n')

            for i in Linearresult2:
                OFile.write(i + '\n')

            for i in Linearresult1:
                OFile.write(i + '\n')

            OFile.write('ASSERT(BVGT(In_r1 , ' + '0hex' + '0' * 16 + '));' + '\n')

            OFile.write(
                'ASSERT(BVPLUS(8,' + ','.join(['0bin0000000@(%s)' % (self.MyG_FeistelLinear.sum[i]) for i in range(
                    self.MyG_FeistelLinear.Round * 8)]) + ')' + ' = ' + 'zonggeshu' + ');' + '\n')

            OFile.write('ASSERT(BVLE(zonggeshu,0bin' + bin(S_num)[2:].zfill(8) + '));\n')
            # OFile.write('ASSERT(BVGT(R_r1 , ' + '0bin' + '0' * 32 + '));' + '\n')

            OFile.write('QUERY FALSE; \n')
            OFile.write('COUNTEREXAMPLE; \n')

            OFile.close()




