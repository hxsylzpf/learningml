#coding : tuf-8
"""
    绘制散点图
"""
#导入相应模块
from numpy import *
import kNN
import matplotlib
import matplotlib.pyplot as plt


fig = plt.figure() #创建figure对象
ax = fig.add_subplot(111)   #在图片对象实例上添加一个坐标轴其中的111是坐标轴比例
datingDataMat,datingLabels = kNN.file2matrix('datingTestSet2.txt') #获得数据文件中的数据矩阵
#ax.scatter(datingDataMat[:,1], datingDataMat[:,2]) #在坐标实例上绘制散点图
ax.scatter(datingDataMat[:,0], datingDataMat[:,1], 15.0*array(datingLabels), 15.0*array(datingLabels))
#ax.axis([-2,25,-0.2,2.0]) #坐标轴的区间
plt.xlabel('Percentage of Time Spent Playing Video Games') #x轴标签
plt.ylabel('Liters of Ice Cream Consumed Per Week')#y轴标签
plt.show()#显示
