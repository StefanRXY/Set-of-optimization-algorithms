# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 09:42:08 2018

@author: ofersh@telhai.ac.il
Based on code by <github/Akavall>
"""
import numpy as np

"""
A class for defining an Ant Colony Optimizer for TSP-solving.
The c'tor receives the following arguments:
    Graph: TSP graph 
    Nant: Colony size  蚁群大小
    Niter: maximal number of iterations to be run  要运行的最大迭代次数
    rho: evaporation constant   蒸发常数
    alpha: pheromones' exponential weight in the nextMove calculation   信息素在nextMove计算中的指数权重
    beta: heuristic information's (\eta) exponential weight in the nextMove calculation   启发式信息在nextMove计算中的指数权重
    seed: random number generator's seed
    we consider a general solution for best packing with ACO
    
    每次迭代后，允许最佳蚂蚁放置信息素。放置量由该蚂蚁构建的溶液的适应度给出（f（s best））。
    在S最佳解决方案中，为每两个项目尺寸I和J放置了信息素。意思，τ（i，j）可以升级多次。该公式中的以下公式中可以描述信息素的更新：
    τ（i，j）=ρ·τ（i，j）+ m·f（1）在该公式中，m是i的次数j在垃圾箱里一起去了
    
"""
class AntforTSP(object) :
    def __init__(self, Items, Nant, Niter, rho, beta=1, seed=None):
        self.Items = Items    # 每个箱子的重量
        self.Nant = Nant      # 蚁群大小
        self.Niter = Niter    # 要运行的最大迭代次数
        self.rho = rho        # 蒸发常数
        self.beta = beta
        self.pheromone = np.ones([max(self.Items)+1, max(self.Items)+1])*20    # 信息素
        self.local_state = np.random.RandomState(seed)

    def run(self) :
        ## 定义蚁群算法的迭代更新计算函数，此为主函数，后面的所有函数均为嵌套函数
        #  Book-keeping: best tour ever
        shortest_path = None
        best_path = ("TBD", 0)
        for i in range(self.Niter):
            # 算法开始迭代
            all_paths = self.constructColonyPaths()   # 将all_path赋值到constructColonyPaths函数中计算
            # print(self.pheromone * self.rho)  #  evaporation  蒸发，返回蒸发浓度
            shortest_path = max(all_paths, key=lambda x: x[1])     # 返回最短距离中最小的即为所求
            if i % 5 == 0 and i != 0:
                self.depositPheronomes(best_path)
            else:
                self.depositPheronomes(shortest_path)           # 判断最小距离下信息素浓度
            print(i+1, ": ", len(shortest_path[0]), " ", shortest_path[0])
            if shortest_path[1] > best_path[1]:
                best_path = shortest_path        # 最佳距离为最短的路径
        return best_path

    def depositPheronomes(self, best_ant) :
        # 寄存信息素
        best_ant_packing = best_ant[0]     #  最佳包装
        best_fitness = best_ant[1]        # 最佳适应度计算
        for _bin in best_ant_packing:
            for i in range(0, len(_bin)):
                for j in range(i+1, len(_bin)):
                    self.pheromone[_bin[i]][_bin[j]] += best_fitness   # dist距离计算
                    self.pheromone[_bin[j]][_bin[i]] += best_fitness   # dist

    def constructColonyPaths(self) :
        # 构建群体路径
        all_paths = []
        for i in range(self.Nant):
            path = self.constructSolution()     #个体距离计算调用constructSolution函数，后面调用的所有函数都是以这个为主函数
            #constructing pairs: first is the tour, second is its length
            all_paths.append((path, self.evalTour(path))) 
        return all_paths   
    
    def evalTour(self, path) :
        #  旅行评估，计算sum_bins值
        sum_bins = 0
        C = 150
        k=2
        for _bin in path:
            F = 0
            for item in _bin:
                F += item
            sum_bins += (F/C)**k               
        return sum_bins/len(path)           
    
    def constructSolution(self) :#TO DO
        ##  构造解决方案
        items = list(np.copy(self.Items))  # 将Items复制给items为列表的格式
        path = []
        for i in range(len(self.Items)) :
            # 计算第一个个体装箱方案
            row = self.fillBin(items)
            # row = items
            path.append(row)
            if len(items) == 0: break
        return path
           
    def fillBin(self, items):
        bin_items = []  #设置方案结果为空列表
        _bin = 0  # 设置最小的重量为0
        max_bin = 150   # 设置最大的重量为0
        while len(items) != 0 and (max_bin - _bin) > min(items):
            for item in items:
                if self.ifToAddItem(max_bin - _bin, item, bin_items, items):
                    bin_items.append(item)
                    _bin += item
                    items.remove(item)
                    break
                if len(items) == 0 or (max_bin - _bin) < min(items) :
                    break
        return bin_items
           
    def ifToAddItem(self, bin_left_space, item, bin_items, items):
        # 如果要添加项目
        if item > bin_left_space:                     # 判断最小重量的箱子
            return False
        denom = 0
        for i in items:
           if i <= bin_left_space:                      # 将denom信息素浓度计算
                denom += (self.binTao(i, bin_items)*(i**self.beta)).astype(np.int64)
        nume = self.binTao(item, bin_items)*item**self.beta
        return self.local_state.uniform() < (nume/denom)
    
    def binTao(self, item, bin_items):
        phero_sum = 0                  # 设置初始的phero_sum=0
        if len(bin_items) == 0:
            return 1
        for i in bin_items:
            phero_sum += self.pheromone[i][item]
        return phero_sum/len(bin_items)    
    
        
    