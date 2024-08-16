import numpy as np
import open3d as o3d

def test():
    print('test')

class PointCloudUtils:

    def __init__(self):
        pass


    def test_in_class():
        print('test_in_class')
        
    
    def read_point_cloud_off_file(str_file_path):
        """从 OFF 文件中读取点云数据"""
        with open(str_file_path, 'r') as file:
            lines = file.readlines()
        
        # 读取点数和面数
        header = lines[1].split()
        num_points = int(header[0])
        
        # 读取点坐标
        points = []
        for line in lines[2:2+num_points]:
            point = list(map(float, line.strip().split()))
            points.append(point)

        return np.array(points)
