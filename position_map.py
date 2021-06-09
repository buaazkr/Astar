from __future__ import print_function
import math

class xy_position:
    """docstring for xy_position"""
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

class Node:
    def __init__(self, xy_position, g = 0, h = 0):
        self.xy_position = xy_position        #节点自身坐标
        self.father = None        #父节点指针
        self.g = g                #节点g值
        self.h = h                #节点h值

    """
    h估价公式：欧几里得距离，每个格子长度为10
     """
    def Euclid(self, endNode):
        self.h = math.sqrt((10*(endNode.xy_position.x - self.xy_position.x))**2 + (10*(endNode.xy_position.y - self.xy_position.y))**2)
    def reset_g(self, g):
        self.g = g

    def setFather(self, node):
        self.father = node

class position_map:
    """
    地图数据
    """
    def __init__(self):
        """
        地图尺寸以及障碍物和可通过点以及寻得路径的标志
        """
        self.map = [list("□□□□□□□□□□"),
                     list("■□□■□□□□■□"),
                     list("□□□□□■□□□□"),
                     list("□□■□□□■□■□"),
                     list("□□□□□□□□□□"),
                     list("□□□□■□□□□□"),
                     list("□□□□□□□□□□"),
                     list("□□■□□□■□□□"),
                     list("□□□□□□□□□□"),
                     list("■□■□□□□□■□")]
        self.passTag = '□'
        self.obtions = '■'
        self.pathTag = '★'
        self.height = 10
        self.width = 10

    def print_map(self):
        for x in range(0, self.height):
            for y in range(0, self.width):
                print(self.map[x][y], end='')
            print(" ")
        return

    def draw_path(self, xy_position):
        self.map[xy_position.x][xy_position.y] = self.pathTag
        return

    def judge_obtions(self, xy_position):
        if (xy_position.x < 0 or xy_position.x > self.height - 1) or (xy_position.y < 0 or xy_position.y > self.width - 1):
            return False

        if self.map[xy_position.x][xy_position.y] == self.passTag:
            return True