# 常用工具类
import os
import random
import re
import yaml


def test():
    print('test')


class FileUtils:

    def __init__(self):
        pass


    def test_in_class():
        print('test_in_class_file')

    
    def read_image_directory_path_to_file_path_list(str_directory_path=None):
        '''
        读取指定目录下所有图片的路径并按数字键进行排序
        图片文件格式支持jpg, jpeg, png, bmp
        
        Parameters:
        - str_directory_path (str): 图片目录路径
        
        Returns:
        - sorted_file_list (list): 图片路径列表
        '''

        def _natural_sort_key(s):
            '''
            使用正则表达式对文件名排序, 按数字分组并按数字进行排序
            例如: '0_back', '2_back', '10_back' 被分为 ['0_', '2_', '10_']
            再按 ['0', '2', '10'] 进行排序

            Parameters:
            - s (str): 文件名

            Returns:
            - key (list): 按数字键进行排序的列表
            '''
            # 提取字符串中的数字并转换为整数
            return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', s)]

        # 若 str_directory_path 为 None, 则返回 None
        if str_directory_path is None:
            return None
  
        # 图片地址列表
        image_path_list = []
        # 定义图片扩展名列表，用于后面仅检查图片
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']

        # 遍历目录下的所有文件和文件夹  
        for filename in os.listdir(str_directory_path):  
            # 排除隐藏文件(.开头文件) 和 检查文件扩展名是否是图片文件  
            if not filename.startswith('.') and any(filename.lower().endswith(ext) for ext in image_extensions):
                image_path_list.append(os.path.join(str_directory_path, filename)) 

        # 对文件名进行排序，以便按数字键进行排序
        # 若普通排序无法对字符串0_back, 2_back和10_back进行排序
        sorted_file_list = sorted(image_path_list, key=_natural_sort_key)  
        
        return sorted_file_list
    
    def read_yaml_file(yaml_file_path):
        '''
        读取yaml文件

        Parameters:
        - yaml_file_path (str): yaml文件路径

        Returns:
        - data (dict): yaml文件内容
        '''
        with open(yaml_file_path, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        
        return data
        
    

