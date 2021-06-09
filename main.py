import position_map
import support

if __name__ == '__main__':
    ##构建地图
    start = input("请输入寻路起始点坐标 \nxy坐标用空格分割，例如：3 3: ")
    end = input("请输入寻路终止点坐标 \nxy坐标用空格分割，例如：9 9: ")
    start_xy_position = start.split(' ')
    end_xy_position = end.split(' ')
    if start_xy_position == end_xy_position:
        print("抱歉，输入起点等于终点，请重试")
    else:
        map = position_map.position_map()
        ##构建A*
        aStar = support.AStar(map, support.Node(support.xy_position(int(start_xy_position[0]) - 1, int(start_xy_position[1]) - 1)),
                              support.Node(support.xy_position(int(end_xy_position[0]) - 1, int(end_xy_position[1]) - 1)))
        print("使用A*算法寻路中......")
        ##开始寻路
        if aStar.start():
            aStar.draw_path()
            print("A*算法搜索路径如下：")
            map.print_map()
            print("寻路成功！程序正常结束。")
        else:
            print("寻路失败，请检查输入起始点和终止点坐标是否正确")