# D:\apps\python\python.exe manage.py runserver 0.0.0.0:8000
# '/home/giantbranch/Python-3.10.0/python' manage.py runserver 0.0.0.0:8000
# pip install pywinauto -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
# D:\apps\python\python.exe manage.py runserver 0.0.0.0:8000
# '/home/giantbranch/Python-3.10.0/python' manage.py runserver 0.0.0.0:8000
# 127.0.0.1:8000
# python manage.py migrate
# lsof -i:8000
# kill -9 xx
import zipfile


import numpy as np

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .mycode.Feistel_test import analyze
# from .. import mycode.Feistel_test

def input(request):
    return render(request, 'input.html')


def string_to_list(string):
    # 将字符串string转换为int元素的数组list
    if "\n" in string:
        list1 = list(string.split("\n"))
        list2 = []
        for i in range(len(list1)):
            if " " in list1[i]:
                list1[i] = list(list1[i].split(" "))
                for j in range(len(list1[i])):
                    if "," in list1[i][j]:
                        list1[i][j] = list1[i][j].replace(",", "")
                        if ~list1[i][j].isdigit(): return -1  # 输入格式有误
                list1[i] = list(map(int, list1[i]))
            elif "," in list1[i]:
                list1[i] = list(list1[i].split(","))
                for j in range(len(list1[i])):
                    if ~list1[i][j].isdigit(): return -1  # 输入格式有误
                list1[i] = list(map(int, list1[i]))
            else:
                return -1  # 输入格式有误
            list2.extend(list1[i])
        return list2
    else:
        if " " in string:
            list1 = list(string.split(" "))
            for i in range(len(list1)):
                if "," in list1[i]:
                    list1[i] = list1[i].replace(",", "")
                    if ~list1[i].isdigit(): return -1  # 输入格式有误
            list1 = list(map(int, list1))
        elif "," in string:
            list1 = list(string.split(","))
            for i in range(len(list1)):
                if ~list1[i].isdigit(): return -1  # 输入格式有误
            list1 = list(map(int, list1))
        else:
            return -1  # 输入格式有误
        return list1

def string_to_list2(string):
    # 将字符串string转换为int含元素的二维数组list
    list1 = list(string.split("\n"))
    # print(list1)
    for i in range(len(list1)):
        # print(list1[i])
        if " " in list1[i]:
            list1[i] = list(list1[i].split(" "))
            for j in range(len(list1[i])):
                if "," in list1[i][j]:
                    list1[i][j] = list1[i][j].replace(",", "")
                    if ~list1[i][j].isdigit(): return -1  # 输入格式有误
            # print('list1[i]1',list1[i])
            list1[i] = list(map(int, list1[i]))
            # print('list1[i]2',list1[i])
        elif "," in list1[i]:
            list1[i] = list(list1[i].split(","))
            for j in range(len(list1[i])):
                if ~list1[i][j].isdigit(): return -1  # 输入格式有误
            list1[i] = list(map(int, list1[i]))
        else:
            return -1  # 输入格式有误
    return list1

def IsSbox(_Sbox):
    # 判断输入的S盒是否合法
    for i in _Sbox:
        if i <= 15 and i >= 0:
            continue
        else:
            return False
    return True

def IsMartix(_Martix):
    # 判断输入的01矩阵是否合法
    for i in range(len(_Martix)):
        for j in _Martix[i]:
            if j == 1 or j == 0:
                continue
            else:
                return False
        return True
@csrf_exempt
def result(request):
    print(request.method)
    if request.method == 'POST':
        dic = request.POST
        print(dic)
        # whichone = 'Feistel'
        # block_length= '64'
        # round = '3'
        # Sbox_length= '4'
        # Sbox_number= '8'
        # activeSbox_number= '1'
        # Sbox_content = '2 0 7 4 1 3 6 5 9 11 13 15 14 12 10 8'
        # linear_matrix = '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1\n1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0'
        whichone = dic['struct']
        block_length = dic['block_length']
        round = dic['round']
        Sbox_length = dic['Sbox_length']
        Sbox_content = dic['Sbox_content']
        linear_matrix = dic['linear_matrix']


        if block_length.isdigit():
            block_length = int(block_length)
        else:
            print('block_length is not digit')
        if round.isdigit():
            round = int(round)
        else:
            print('round is not digit')
        if Sbox_length.isdigit():
            Sbox_length= int(Sbox_length)
        else:
            print('Sbox_length is not digit')
        # if activeSbox_number.isdigit():
        #     activeSbox_number = int(activeSbox_number)
        # else:
        #     print('activeSbox_number is not digit')
        if string_to_list(Sbox_content) == -1:
            # S盒输入有误
            print('Sbox_content is wrong')
            # print("-1")
        else:
            Sbox_content = string_to_list(Sbox_content)
            if not IsSbox(Sbox_content):
                print('linear_matrix not IsSbox')
        if string_to_list2(linear_matrix) == -1:
            # 矩阵输入有误
            print('linear_matrix is wrong')
            # print("-2")
        else:
            linear_matrix = string_to_list2(linear_matrix)
            if not IsMartix(linear_matrix):
                print('linear_matrix not IsMartix')
                # print("-2 ,")
        result_context = analyze(whichone,block_length,round,Sbox_length,Sbox_content,linear_matrix)


        # print("result_context:",result_context)
        anayalse_result = {'context':result_context}
        # print(anayalse_result)
        # print((anayalse_result["context"]))
        # print(type(anayalse_result["context"]))


        # 文件下载
        f = open("static/result/分析报告.txt", "w")
        for line in result_context:
            f.write(str(line) + "\n")
        f.close()


        zip_file = zipfile.ZipFile('static/分析结果.zip','w')
        # 把zfile整个目录下所有内容，压缩为new.zip文件
        # zip_file.write('static/result/',compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write('static/result/分析报告.txt',arcname='分析报告.txt',compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write('static/result/差分.txt',arcname='差分.txt',compress_type=zipfile.ZIP_DEFLATED)
        zip_file.write('static/result/线性.txt',arcname='线性.txt',compress_type=zipfile.ZIP_DEFLATED)
        

    # return传入的参数必须为dic 不是str
    return render(request, 'result.html',anayalse_result)

@csrf_exempt
def progress(request):
        return render(request,'process.html')
@csrf_exempt
def fina(request):
    return render(request,'finally.html')
