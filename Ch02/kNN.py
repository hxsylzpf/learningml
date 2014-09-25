#coding:utf-8
'''
Created on Sep 16, 2010
kNN: k Nearest Neighbors

Input:      inX: vector to compare to existing dataset (1xN)
            inX:  和现存的数据集合进行比教的向量
            dataSet: size m data set of known vectors (NxM)
                  
            labels: data set labels (1xM vector)
                    数据集标签
            k: number of neighbors to use for comparison (should be an odd number)
                    用于比对的近邻数
            
Output:     the most popular class label 
Output:     最受欢迎类标签
@author: pbharrin（-<你丫的语文老师死的早，fuck your fucking code）
'''

#导入需要的模块

from numpy import *#严重破坏命名空间
import operator
from os import listdir


#分类函数
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()     
    classCount={}          
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


#创建数据集合
def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])#x
    labels = ['A','A','B','B']#y
    return group, labels



#文件2矩阵
def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())         #get the number of lines in the file(获得文件的行数)
    returnMat = zeros((numberOfLines,3))        #prepare matrix to return（准备要返回的矩阵【元素初始化为零的二维矩阵】）
    classLabelVector = []                       #prepare labels return   （准备要返回的标签【列表】）
    fr = open(filename)                         #这一语句不是没用，用于把文件指针重新移到文件开始处
    index = 0                                   #索引初始化为0
    for line in fr.readlines():                 #逐行读取文件
        line = line.strip()                     #去除换行符
        listFromLine = line.split('\t')         #通过\t对数据进行分割，返回列表
        returnMat[index,:] = listFromLine[0:3]  #读取前三个数据（group），第四个是标签（label）【注意那个逗号】
        classLabelVector.append(int(listFromLine[-1]))#追加标签
        index += 1
    return returnMat,classLabelVector 


#自动归一化，使得三类数据具有相同的权值   
def autoNorm(dataSet):
    minVals = dataSet.min(0) 
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))   #element wise divide
    return normDataSet, ranges, minVals
   
 #约会测试  
def datingClassTest():
    hoRatio = 0.50      #hold out 10% 提取1/10
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')       #load data setfrom file从文件导入数据
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print u"分类器判断为: %d, 真实答案为: %d" % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print u"判断错误率为: %f" % (errorCount/float(numTestVecs))
    print errorCount
 


 #图片2向量   
def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect


#手写数字测试
def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')           #load the training set
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    testFileList = listdir('testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print u"分类器判断为: %d, 真实答案为: %d" % (classifierResult, classNumStr)
        if (classifierResult != classNumStr): errorCount += 1.0
    print u"\n判断错误总数: %d" % errorCount
    print u"\n判断错误率: %f" % (errorCount/float(mTest))
