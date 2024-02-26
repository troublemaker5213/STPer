# from .mycode.mytest import mytest
from .test import test
# import mytest
# from . import test
import time,os

# def stp_out(analyse,context):
#     if(analyse=='DIF'):
#         lp_file = r"/home/giantbranch/Desktop/DIF.txt"
#     elif(analyse=='Linear'):
#         lp_file = r"/home/giantbranch/Desktop/Linear.txt"
#     with open(lp_file, 'a') as OFile:
#         OFile.seek(0)
#         OFile.truncate()
#         OFile.write(context)
#         OFile.close()

def out_result(flag_stop,flag_analyse,round_i,Sbox_num_min,result_list):
    
    if(flag_stop == 0):
        result_list.append("success！"+str(round_i)+"轮达到最少S盒个数为"+str(Sbox_num_min))
        print("success！"+str(round_i)+"轮达到最少S盒个数为"+str(Sbox_num_min))
    elif(flag_stop == 1):
        result_list.append("time out!运行到第"+str(round_i)+"轮，最少S盒个数为"+str(Sbox_num_min))
        print("time out!运行到第"+str(round_i)+"轮，最少S盒个数为"+str(Sbox_num_min))
    elif(flag_stop == 2):
        result_list.append("到达指定轮数，运行到第"+str(round_i)+"轮，最少S盒个数为"+str(Sbox_num_min))
        print("到达指定轮数，运行到第"+str(round_i)+"轮，最少S盒个数为"+str(Sbox_num_min))
    else:
        print("unknow error!")
        return

    
    # context = str(round_i)+"轮达到最小S盒个数为"+str(Sbox_num_min)
    # print(context)
    # if(flag_analyse == "DIF"):
    #     lp_file = r"./DIF.txt"
    # elif(flag_analyse=='Linear'):
    #     lp_file = r"./Linear.txt"
    # with open(lp_file, 'a') as OFile:
    #     OFile.seek(0)
    #     OFile.truncate()
    #     for i in range(0, len(context)):
    #         res = context[i]
    #         OFile.write(res)       
    #     OFile.close()

def testDIFanalyse(whichone,len_bit,round,len_Sbox,Sbox_num_min,Sbox,Matrix):
    result_list = []
    
    for round_i in range(1,round+1):
        left = 0
        Mytest = test(whichone,len_bit,round_i, len_Sbox, Sbox, Matrix)
        for S_num_i in range(left,Sbox_num_min+1):

            if whichone == 'SPN':
                Mytest.SPNDIFanalyse(S_num_i)
            elif whichone == 'Feistel':
                Mytest.FeistelDIFanalyse(S_num_i)
            elif whichone == 'SIMON':
                Mytest.SIMONDIFanalyse(S_num_i)
            elif whichone == 'SPECK':
                Mytest.SPECKDIFanalyse(S_num_i)
            elif whichone == 'G_Feistel':
                Mytest.G_FeistelDIFanalyse(S_num_i)


            # Mytest.FeistelDIFanalyse(S_num_i)



            time_start=time.time()
            re = (os.popen("'/home/giantbranch/stp/build/stp'  '/home/giantbranch/Desktop/DIF.cvc'"))
            re = (re.readlines())
            # print(re)
            time_end=time.time()
            timetime = time_end-time_start

            if(re[-1] == 'Invalid.\n'):
                
                left = S_num_i
                print(str(round_i)+"轮，最少活跃S盒个数为"+str(S_num_i))
                result_list.append(str(round_i)+"轮，最少活跃S盒个数为"+str(S_num_i))
                # print("第"+str(round_i)+"轮，最小活跃S盒个数为"+str(S_num_i)+"  STP求解用时"+str(timetime)+"s")
                if(left == Sbox_num_min or timetime >= 3000):

                    f = open("static/result/差分.txt", "w")
                    # print(f)
                    for line in re:
                        f.write(str(line))
                    f.close()

                    if(left == Sbox_num_min):
                        out_result(0,"DIF",round_i,Sbox_num_min,result_list)
                        # print("success！"+str(round_i)+"轮达到最小S盒个数为"+str(Sbox_num_min))
                    elif(timetime >= 300):
                        out_result(1,"DIF",round_i,S_num_i,result_list)
                        # print("time out!运行到第"+str(round_i)+"轮，最小S盒个数为"+str(S_num_i))

                    # lp_file = r"/home/giantbranch/Desktop/DIF.txt"
                    # with open(lp_file, 'a') as OFile:
                    #     OFile.seek(0)
                    #     OFile.truncate()
                    #     for i in range(0, len(re)):
                    #         res = re[i]
                    #         OFile.write(res)       
                    #     OFile.close()
                    return result_list
                break
        if(round_i == round):
            f = open("static/result/差分.txt", "w")
            # print(f)
            for line in re:
                f.write(str(line))
            f.close()
            out_result(2,"DIF",round_i,S_num_i,result_list)
    return result_list

def testLinearanalyse(whichone,len_bit,round,len_Sbox,Sbox_num_min,Sbox,Matrix):
    result_list = []
    for round_i in range(1,round+1):
        left = 0

        for S_num_i in range(left,Sbox_num_min+1):
            Mytest = test(whichone ,len_bit ,round_i, len_Sbox, Sbox, Matrix)
            if whichone == 'SPN':
                Mytest.SPNLinearanalyse(S_num_i)
            elif whichone == 'Feistel':
                Mytest.FeistelLinearanalyse(S_num_i)
            elif whichone == 'SIMON':
                Mytest.SIMONLinearanalyse(S_num_i)
            elif whichone == 'SPECK':
                Mytest.SPECKLinearanalyse(S_num_i)
            elif whichone == 'G_Feistel':
                Mytest.G_FeistelLinearanalyse(S_num_i)


            time_start=time.time()
            re = (os.popen("'/home/giantbranch/stp/build/stp'  '/home/giantbranch/Desktop/Linear.cvc'"))
            re = (re.readlines())
            time_end=time.time()
            timetime = time_end-time_start
            
            if(re[-1] == 'Invalid.\n'):
                left = S_num_i
                # print("第"+str(round_i)+"轮，最小活跃S盒个数为"+str(S_num_i)+"  STP求解用时"+str(timetime)+"s")
                print(str(round_i)+"轮，最少活跃S盒个数为"+str(S_num_i))
                result_list.append(str(round_i)+"轮，最少活跃S盒个数为"+str(S_num_i))
                if(left == Sbox_num_min or timetime >= 300):

                    f = open("static/result/线性.txt", "w")
                    for line in re:
                        f.write(str(line))
                    f.close()

                    if(left == Sbox_num_min):
                        result_list.append("0")
                        out_result(0,"Linear",round_i,S_num_i,result_list)
                        # print("success！"+str(round_i)+"轮达到最小S盒个数为"+str(Sbox_num_min))
                    elif(timetime >= 300):
                        out_result(1,"Linear",round_i,S_num_i,result_list)
                        # print("time out!运行到第"+str(round_i)+"轮，最小S盒个数为"+str(S_num_i))

                    # lp_file = r"/home/giantbranch/Desktop/Linear.txt"
                    # with open(lp_file, 'a') as OFile:
                    #     OFile.seek(0)
                    #     OFile.truncate()
                    #     for i in range(0, len(re)):
                    #         res = re[i]
                    #         OFile.write(res)       
                    #     OFile.close()
                    return result_list
                break
        if(round_i == round):
            f = open("static/result/线性.txt", "w")
            # print(f)
            for line in re:
                f.write(str(line))
            f.close()
            out_result(2,"Linear",round_i,S_num_i,result_list)
    return result_list

    # Mytest.DIFanalyse(S_num_i)
    # Mytest.Linearanalyse(S_num_i)

def analyze(whichone,len_bit, round, len_Sbox,Sbox,matrix):
    Sbox_num_min = 100
    result_context = []
    print("==========差分分析==========")
    DIF_context = testDIFanalyse(whichone,len_bit,round,len_Sbox,Sbox_num_min,Sbox,matrix)
    # print(DIF_context)

    # if(Sbox_num_min > int(DIF_context[0][-1]) or round > int(DIF_context[0][0])):
    #     DIF_context[1] = '安全'
    # else:
    #     DIF_context[1] = '不安全'
    # DIF_context[1] = 

    print("==========线性分析==========")
    Linaer_context = testLinearanalyse(whichone,len_bit,round,len_Sbox,Sbox_num_min,Sbox,matrix)
    # print(Linaer_context)
    # if(Sbox_num_min > int(DIF_context[0][-1]) or round > int(DIF_context[0][0])):
    #     Linaer_context[1] = '安全'
    # else:
    #     Linaer_context[1] = '不安全'
    result_context.append("========差分分析=======")
    result_context+=DIF_context
    result_context.append("========线性分析=======")
    result_context+=Linaer_context


    # print(result_context)
    return result_context
