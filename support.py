#AStar算法中的节点对象
from position_map import Node
#节点的（x,y）坐标对象
from position_map import xy_position

class AStar:
    """
    A* 算法
    """
    def __init__(self, position_map, startNode, endNode):
        """
        position_map:      地图
        startNode:  起点坐标
        endNode:    终点坐标
        """
        #Open表
        self.OpenList = []
        #Close表
        self.CloseList = []
        #地图
        self.position_map = position_map
        #起始节点对象
        self.startNode = startNode
        #终止节点对象
        self.endNode = endNode
        #当前搜索节点
        self.currentNode = startNode
        #搜索完成标志
        self.end_flag = False
        #根据父节点指针寻找的路径
        self.pathlist = []
        return

    def min_F_node_inOpenList(self):
        """
        获得OpenList中F值最小的节点（F=g+h）
        """
        nodeTemp = self.OpenList[0]
        for node in self.OpenList:
            if node.g + node.h < nodeTemp.g + nodeTemp.h:
                nodeTemp = node
        return nodeTemp

    def judge_node_inOpenList(self,node):
        """
        判断一个节点是否在Open表中
        """
        for nodeTmp in self.OpenList:
            if nodeTmp.xy_position.x == node.xy_position.x \
            and nodeTmp.xy_position.y == node.xy_position.y:
                return True
        return False

    def judge_node_inCloseList(self,node):
        """
        判断一个节点是否在Close表中
        """
        for nodeTmp in self.CloseList:
            if nodeTmp.xy_position.x == node.xy_position.x \
            and nodeTmp.xy_position.y == node.xy_position.y:
                return True
        return False

    def get_node_in_OpenList(self,node):
        """
        如果搜索的节点在Open表中，就获取这个节点（用于判断是否需要更换该节点的父节点和g值）
        """
        for nodeTmp in self.OpenList:
            if nodeTmp.xy_position.x == node.xy_position.x \
            and nodeTmp.xy_position.y == node.xy_position.y:
                return nodeTmp
        return None

    def get_node_in_CloseList(self,node):
        """
        如果搜索的节点在Close表中，就获取这个节点（用于判断是否需要更换该节点的父节点和g值,以及送这个节点返回Open表）
        """
        for nodeTmp in self.CloseList:
            if nodeTmp.xy_position.x == node.xy_position.x \
            and nodeTmp.xy_position.y == node.xy_position.y:
                return nodeTmp
        return None

    def expand_one_node(self,node):
        """
        搜索一个节点（这个节点是当前节点附近的节点，也就是当前节点的子节点）
        x为是行坐标
        y为是列坐标
        """
        #对于障碍物直接返回
        if self.position_map.judge_obtions(node.xy_position) != True:
            return

        #G值计算
        if abs(node.xy_position.x - self.currentNode.xy_position.x) == 1 and abs(node.xy_position.y - self.currentNode.xy_position.y) == 1:
            gTemp = 14
        else:
            gTemp = 10

        #如果该节点不在OpenList中，就加入OpenList
        if self.judge_node_inOpenList(node) == False:
            node.reset_g(gTemp)
            #H值计算
            node.Euclid(self.endNode)
            self.OpenList.append(node)
            node.father = self.currentNode

        #如果已经在OpenList中，判断该节点的F值与之前计算的F值大小
        #如果更小，就重新计算OpenList中该节点的g值，并更改父节点
        else:
            node_before = self.get_node_in_OpenList(node)
            node.reset_g(gTemp + self.currentNode.g)
            node.Euclid(self.endNode)
            if node_before.g + node_before.h > node.g + node.h:
                node_before.g = node.g
                node_before.father = self.currentNode

        # 如果已经在CloseList中，判断该节点的F值与之前计算的F值大小
        # 如果更小，该节点的g值，并更改父节点，而后将节点重新加入OpenList中
        if self.judge_node_inCloseList(node) == True:
            node_before = self.get_node_in_CloseList(node)
            node.reset_g(gTemp + self.currentNode.g)
            node.Euclid(self.endNode)
            if node_before.g + node_before.h > node.g + node.h:
                node_before.g = node.g
                node_before.father = self.currentNode
                self.OpenList.append(node_before)
        return

    def search_currentnode_near(self):
        """
        对于当前节点周围的8个字节点分别搜索
        对于障碍物和边界之外的子节点不予以搜索
        (x-1,y-1)(x-1,y)(x-1,y+1)
        (x  ,y-1)(当前节点)(x  ,y+1)
        (x+1,y-1)(x+1,y)(x+1,y+1)
        """
        print("当前节点的非障碍物子节点：")
        if self.position_map.judge_obtions(xy_position(self.currentNode.xy_position.x - 1, self.currentNode.xy_position.y - 1)):
            print("( " + str(self.currentNode.xy_position.x - 1+1) + "," + str(self.currentNode.xy_position.y - 1+1) + " )")
            self.expand_one_node(Node(xy_position(self.currentNode.xy_position.x - 1, self.currentNode.xy_position.y - 1)))
        if self.position_map.judge_obtions(xy_position(self.currentNode.xy_position.x, self.currentNode.xy_position.y - 1)):
            print("( " + str(self.currentNode.xy_position.x+1) + "," + str(self.currentNode.xy_position.y - 1+1) + " )")
            self.expand_one_node(Node(xy_position(self.currentNode.xy_position.x, self.currentNode.xy_position.y - 1)))
        if self.position_map.judge_obtions(xy_position(self.currentNode.xy_position.x + 1, self.currentNode.xy_position.y - 1)):
            print("( " + str(self.currentNode.xy_position.x + 1+1) + "," + str(self.currentNode.xy_position.y - 1+1) + " )")
            self.expand_one_node(Node(xy_position(self.currentNode.xy_position.x + 1, self.currentNode.xy_position.y - 1)))
        if self.position_map.judge_obtions(xy_position(self.currentNode.xy_position.x - 1, self.currentNode.xy_position.y)):
            print("( " + str(self.currentNode.xy_position.x - 1+1) + "," + str(self.currentNode.xy_position.y+1) + " )")
            self.expand_one_node(Node(xy_position(self.currentNode.xy_position.x - 1, self.currentNode.xy_position.y)))
        if self.position_map.judge_obtions(xy_position(self.currentNode.xy_position.x + 1, self.currentNode.xy_position.y)):
            print("( " + str(self.currentNode.xy_position.x + 1+1) + "," + str(self.currentNode.xy_position.y+1) + " )")
            self.expand_one_node(Node(xy_position(self.currentNode.xy_position.x + 1, self.currentNode.xy_position.y)))
        if self.position_map.judge_obtions(xy_position(self.currentNode.xy_position.x - 1, self.currentNode.xy_position.y + 1)):
            print("( " + str(self.currentNode.xy_position.x - 1+1) + "," + str(self.currentNode.xy_position.y + 1+1) + " )")
            self.expand_one_node(Node(xy_position(self.currentNode.xy_position.x - 1, self.currentNode.xy_position.y + 1)))
        if self.position_map.judge_obtions(xy_position(self.currentNode.xy_position.x, self.currentNode.xy_position.y + 1)):
            print("( " + str(self.currentNode.xy_position.x+1) + "," + str(self.currentNode.xy_position.y + 1+1) + " )")
            self.expand_one_node(Node(xy_position(self.currentNode.xy_position.x, self.currentNode.xy_position.y + 1)))
        if self.position_map.judge_obtions(xy_position(self.currentNode.xy_position.x + 1, self.currentNode.xy_position.y + 1)):
            print("( " + str(self.currentNode.xy_position.x + 1+1) + "," + str(self.currentNode.xy_position.y + 1+1) + " )")
            self.expand_one_node(Node(xy_position(self.currentNode.xy_position.x + 1, self.currentNode.xy_position.y + 1)))
        return

    def start(self):
        '''''
        A*算法开始搜索
        '''
        #将初始节点加入开放列表
        self.startNode.Euclid(self.endNode)
        self.startNode.reset_g(0)
        self.OpenList.append(self.startNode)
        epoch = 1
        while True:
            #获取当前OpenList里F值最小的节点作为当前节点
            #将当前节点添加到CloseList，从OpenList中删除它
            print("\033[0;31m第"+str(epoch)+"次搜索\033[0m")
            print("当前Open表中节点数：" + str(len(self.OpenList)))
            for n in self.OpenList:
                print("     (" + str(n.xy_position.x+1) + "," + str(n.xy_position.y+1) + ")     ")
            self.currentNode = self.min_F_node_inOpenList()
            self.CloseList.append(self.currentNode)
            self.OpenList.remove(self.currentNode)
            print("从Open表中选择当前节点坐标：( " + str(self.currentNode.xy_position.x+1)+ "," + str(self.currentNode.xy_position.y+1) + " )")
            self.search_currentnode_near()
            epoch += 1

            #检验是否结束
            for nodeTmp in self.OpenList:
                if nodeTmp.xy_position.x == self.endNode.xy_position.x \
                        and nodeTmp.xy_position.y == self.endNode.xy_position.y:
                    self.end_flag = True
            if self.end_flag:
                print("当前节点的子节点中有终止节点，搜索结束")
                #搜索已结束，按照父节点指针寻找路径
                nodeTmp = self.get_node_in_OpenList(self.endNode)
                while True:
                    self.pathlist.append(nodeTmp)
                    if nodeTmp.father != None:
                        nodeTmp = nodeTmp.father
                    else:
                        return True
            elif len(self.OpenList) == 0:
                return False

    def draw_path(self):
        for node in self.pathlist:
            self.position_map.draw_path(node.xy_position)
        return