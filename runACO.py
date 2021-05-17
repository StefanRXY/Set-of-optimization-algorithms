# -*- coding: utf-8 -*-
"""
@author: ofersh@telhai.ac.il
"""
from ACO import AntforTSP as ACO
import numpy as np


if __name__ == "__main__" :
   
    #Running for 120 groups
    # 提取文件，将提供的txt文件读取后，储存到data120中
    fname120 = open("roskilde_250groups.dat.txt")
    data120 = []
    for line in fname120:
        data120.append(int(line))
    n120 = len(data120)  # n120是data120的长度，为120
    # epochs = 10**2
    epochs = 2  # 蚁群算法的迭代次数
    Population  = 12  # 蚁群算法的种群数量
    ## 调用ACO.py文件中的AntforTSP类，并将初始参数传递到类中
    ant_colony_120 = ACO(data120,Population , epochs, rho=0.95, beta=5)
    # 最短距离为AntforTSP中的run()函数计算得到
    shortest_path_120 = ant_colony_120.run()
    # print("shotest_path_120: {}".format(shortest_path_120), ' ', len(shortest_path_120[0]))
    print("shotest_path_120:",shortest_path_120[0])
    
    #Running for 250 groups
    # fname250 = open("roskilde_250groups.dat.txt")
    # data250 = []
    # epochs = 10**2
    # Population  = 250
    # for line in fname250:
    #     data250.append(int(line))
    # n250 = len(data250)
    # ant_colony_250 = ACO(data250,Population , epochs, rho=0.95, beta=10)
    # shortest_path_250 = ant_colony_250.run()
    # print("shotest_path_250: {}".format(shortest_path_250), ' ', len(shortest_path_250[0]))
    
    