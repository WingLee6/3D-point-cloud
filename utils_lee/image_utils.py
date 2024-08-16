# 常用工具类
import os
import matplotlib.pyplot as plt  
import cv2  
import numpy as np  
import random


def test():
    print('test')



class ImageUtils:

    def __init__(self):
        pass


    def test_in_class():
        print('test_in_class')
        
    
    def show_bgr_image_use_plt(image_BGR, str_image_title='output'):
        '''
        使用plt显示BGR格式的图像
        
        Parameters:
        - image_BGR (np.ndarray, BGR格式): BGR格式的图像
        - str_image_title (str, optional): 图像标题，默认'output'
        
        Returns:
        None
        '''
        # 显示预处理结果
        plt.imshow(cv2.cvtColor(image_BGR, cv2.COLOR_BGR2RGB))
        plt.title(str_image_title)
        plt.show()

    def show_image_with_findcontours_info(image_BGR, contours_list):
        '''
        画图标记质心点, 并记录质心坐标
        
        Parameters:
        - image_BGR (np.ndarray, BGR格式): BGR格式的图像
        - contours_list (list): 轮廓列表
        
        Returns:
        - image_BGR (np.ndarray, BGR格式): 画质心点的BGR格式图像
        - centroids_list (list): 质心坐标列表
        '''
        # 计算每个轮廓的中心点
        centroids_list = []
        # 有效序号
        valid_index = 1

        for contour in contours_list:
            M = cv2.moments(contour)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                centroids_list.append((cx, cy))
                
                # 画标记
                cv2.circle(img=image_BGR, center=(cx, cy), radius=5, color=(0, 0, 255), thickness=-1)
                cv2.putText(img=image_BGR, text=str(valid_index) + ': (' + str(cx) + ',' + str(cy) + ')', 
                            org=(cx, cy), fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                            fontScale=4.0, color=(0, 0, 255), thickness=15)
                print(f"Marker {valid_index} center: ({cx}, {cy})")
                
                valid_index += 1

        # 显示画图结果
        plt.figure(figsize=(20, 10))
        plt.imshow(cv2.cvtColor(image_BGR, cv2.COLOR_BGR2RGB))
        plt.show()
        
        return image_BGR, centroids_list

    
    def show_images_and_save(images_list, num_rows=1, num_cols=1, images_title_list=None, 
                    is_save_image=False, str_save_image_path='./output/result.png'):
        """
        画图函数，用于显示一组图像。

        Parameters:
        - images_list (list): 要显示的图像列表。每个图像应该是一个 NumPy 数组。
        - num_rows (int): 本组图像的行数
        - num_cols (int): 本组图像的列数
        - images_title_list (list, optional): 本组图像的标题列表，默认为空列表。
        - is_save_image (bool, optional): 是否保存图像，默认不保存。
        - str_save_image_path (str, optional): 保存图像的路径，默认'./output/result.png'。

        Returns:
        None
        """
        if images_list is None:
            return
        
        # 创建一个包含num_rows行num_cols列的子图, 每个图片尺寸设置为 figsize=(12, 4) 宽度为12英寸，高度为4英寸
        _, axs = plt.subplots(num_rows, num_cols, figsize=(20, 10)) 

        # 遍历图像路径列表，并将图像放入网格中  
        for i in range(num_rows):  
            for j in range(num_cols):  
                # 检查索引是否超出图像列表的范围  
                index = i * num_cols + j  
                if index < len(images_list):   
                    image = images_list[index]  
                    # 注意：OpenCV读取的图像是BGR格式，并且颜色通道顺序与matplotlib不同  
                    # 因此，如果直接显示，颜色可能会不正确。这里我们将其转换为RGB  
                    image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    # 显示图像  
                    axs[index].imshow(image_RGB)  
                    axs[index].axis('off')  # 关闭坐标轴 
                    axs[index].set_title(images_title_list[index] if images_title_list and index < len(images_title_list) else str(index+1))
                else:  
                    # 如果图像不够填充网格，可以选择留空或填充占位符  
                    axs[index].axis('off')  
                    axs[index].set_title('No Image')  

        # 调整子图之间的间距  
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.01, hspace=0.05) 

        if is_save_image:
            plt.savefig(str_save_image_path)
            print(f'图片已保存至 {str_save_image_path}')


    def draw_grayscale_histogram(image_BGR_list, label_list=None, 
                                 is_save_image=False, str_save_image_path='./output/grayscale_histogram.png'):
        '''
        绘图片的灰度直方图.
        - 多图像绘制在一张图中
        - 非灰度图, 自动转换为灰度图后绘制
        - 可选是否保存曲线图
        
        Parameters:
        - image_BGR_list (list, optional): 要绘制的图像列表, 图像格式为BGR. 默认为空列表.
        - label_list (list, optional): 图像标签列表. 默认为空列表.
        - is_save_image (bool, optional): 是否保存图像. 默认不保存.
        - str_save_image_path (str, optional): 保存图像的路径. 默认'./output/grayscale_histogram.png'.
        
        Returns:
        None
        '''
        if image_BGR_list is None:
            return

        plt.figure(figsize=(7, 4))  # 创建一个图形对象，指定大小

        # 可用的颜色和线型
        colors = list(plt.cm.tab10.colors)  # 从colormap获取一组颜色
        linestyles = ['-', '--', '-.', ':']

        for index, image in enumerate(image_BGR_list):
            image_BGR = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # 检查图像是否为BGR格式，并转换为RGB格式
            if len(image_BGR.shape) == 2:                   # 如果图像只有两个维度，说明它已经是灰度图像
                temp_gray_image = image_BGR
            else:
                temp_gray_image = cv2.cvtColor(image_BGR, cv2.COLOR_BGR2GRAY)

            # 计算灰度直方图  
            # 注意：cv2.calcHist的返回值是一个浮点数数组，需要进行归一化和转换  
            temp_hist = cv2.calcHist([temp_gray_image], [0], None, [256], [0, 256])  
            temp_hist_normalized = cv2.normalize(temp_hist, temp_hist).ravel() 

            x = np.linspace(0, 256, len(temp_hist_normalized)) 

            # 随机选择颜色和线型
            color = random.choice(colors)
            linestyle = random.choice(linestyles)
            # 绘制直方图
            plt.plot(x, temp_hist_normalized, label=label_list[index], color=color, linestyle=linestyle, linewidth=2) 
        
        # 添加标题和坐标轴标签  
        plt.title('Grayscale Histogram')  
        plt.xlabel('Bins')  
        plt.ylabel('# of Pixels')  
        
        # 添加图例  
        plt.legend()   
        
        # 显示图形  
        plt.tight_layout()  # 自动调整子图参数, 使之填充整个图像区域  
        plt.show()
        
        if is_save_image:
            plt.savefig(str_save_image_path)
            print(f'图片保存地址: {str_save_image_path}')

    def convert_if_bgr(image):
        '''
        检查图像是否为BGR格式.
        如果是,则转换为RGB格式.
        注意: OpenCV读取的图像是BGR格式, 并且颜色通道顺序与matplotlib不同  
        因此, 如果直接显示, 颜色可能会不正确. 这里我们将其转换为RGB 
        
        Parameters:
        - image (numpy.ndarray, BGR或RGB格式图像): 要转换的图像
        
        Returns:
        - image (numpy.ndarray, RGB格式图像): 转换后的图像
        '''

        
        # 若图片的通道数为3，并且每通道的像素值不完全相同，则判定为BGR格式
        # 检查图像是否为BGR格式
        if len(image.shape) == 3 and image.shape[2] == 3:
            # 判断是否是BGR格式，通常BGR格式的图像会在颜色通道上有特定的像素值范围
            if image[0, 0, 0] != image[0, 0, 1] and image[0, 0, 1] != image[0, 0, 2]:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    
    def convert_if_rgb(image):
        '''
        检查图像是否为RGB格式.
        如果是,则转换为BGR格式.
        注意: OpenCV读取的图像是BGR格式, 并且颜色通道顺序与matplotlib不同  
        因此, 如果直接显示, 颜色可能会不正确. 这里我们将其转换为RGB 
        
        Parameters:
        - image (numpy.ndarray, BGR或RGB格式图像): 要转换的图像
        
        Returns:
        - image (numpy.ndarray, BGR格式图像): 转换后的图像
        '''
        # 若图片的通道数为3，并且每通道的像素值不完全相同，则判定为BGR格式
        # 检查图像是否为BGR格式
        if len(image.shape) == 3 and image.shape[2] == 3:
            # 判断是否是BGR格式，通常BGR格式的图像会在颜色通道上有特定的像素值范围
            if image[0, 0, 0] != image[0, 0, 1] and image[0, 0, 1] != image[0, 0, 2]:
                return image
            else:
                return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


# import numpy as np  
  
# # 假设有三张随机生成的图片数据  
# img1 = np.random.rand(10, 10)  
# img2 = np.random.rand(10, 100)  
# img3 = np.random.rand(10, 1000)  

# imageList = []
# imageList.append(img1)
# imageList.append(img2)
# imageList.append(img3)

# utility_image = UtilityImage()

# utility_image.show_images(imagesList=imageList, imagesTitleList=['Image1', 'Image2', 'Image3'], num_rows=2, num_cols=3)