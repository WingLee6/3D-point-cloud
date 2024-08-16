import os
import numpy as np
import open3d as o3d
import random

def generate_hard_features_plane(width, height, num_points, groove_depth, slope_factor, elevation):
    # 创建网格平面
    x = np.linspace(-width / 2, width / 2, num_points)
    y = np.linspace(-height / 2, height / 2, num_points)
    X, Y = np.meshgrid(x, y)
    
    # 生成基础平面
    Z = np.full_like(X, elevation)  # 可控的整体高度
    
    # 添加坡口 (slope)
    Z += slope_factor * X  # 根据X坐标添加坡度
    
    # 添加凹槽 (groove)
    groove_width = width / random.uniform(8, 12)  # 凹槽宽度
    groove_region = (np.abs(X) < groove_width / 2)
    Z[groove_region] -= groove_depth
    
    # 添加不规则小丘陵形状的鼓包
    for _ in range(random.randint(2, 4)):  # 添加随机数量的小丘陵
        bump_center_x = random.uniform(-width / 2, width / 2)
        bump_center_y = random.uniform(-height / 2, height / 2)
        bump_radius = random.uniform(1.0, 3.0)  # 小丘陵的半径
        bump_height = random.uniform(1.0, 3.0)  # 小丘陵的高度
        
        # 计算小丘陵形状
        bump_mask = ((X - bump_center_x)**2 + (Y - bump_center_y)**2) < bump_radius**2
        bump_distance = np.sqrt((X - bump_center_x)**2 + (Y - bump_center_y)**2)
        bump_profile = bump_height * np.exp(-bump_distance**2 / (2 * (bump_radius/2)**2))
        Z += bump_profile  # 将鼓包添加到平面上

    # 添加类似工件的几何形状（如长方体、圆柱体、锥体）
    for _ in range(random.randint(1, 3)):  # 添加随机数量的工件形状
        shape_type = random.choice(["cuboid", "cylinder", "cone"])
        center_x = random.uniform(-width / 2, width / 2)
        center_y = random.uniform(-height / 2, height / 2)
        
        if shape_type == "cuboid":
            size_x = random.uniform(1.0, 3.0)
            size_y = random.uniform(1.0, 3.0)
            height = random.uniform(1.0, 3.0)
            x_min, x_max = center_x - size_x / 2, center_x + size_x / 2
            y_min, y_max = center_y - size_y / 2, center_y + size_y / 2
            Z[np.logical_and(X >= x_min, X <= x_max)] = np.maximum(
                Z[np.logical_and(X >= x_min, X <= x_max)], 
                elevation + height
            )
            Z[np.logical_and(Y >= y_min, Y <= y_max)] = np.maximum(
                Z[np.logical_and(Y >= y_min, Y <= y_max)], 
                elevation + height
            )

        elif shape_type == "cylinder":
            radius = random.uniform(1.0, 2.0)
            height = random.uniform(1.0, 3.0)
            distance_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
            # 计算圆柱的侧面
            mask_side = distance_from_center < radius
            Z[mask_side] = np.maximum(Z[mask_side], elevation + height)
            
            # 计算圆柱的顶部
            top_mask = np.abs(distance_from_center - radius) < 0.1
            Z[top_mask] = np.maximum(Z[top_mask], elevation + height)
            
            # 确保圆柱顶部与底面之间没有悬空
            for d in np.linspace(0, height, num=10):
                Z[np.logical_and(mask_side, np.abs(Z - (elevation + d)) < 0.1)] = np.maximum(
                    Z[np.logical_and(mask_side, np.abs(Z - (elevation + d)) < 0.1)],
                    elevation + d
                )

        elif shape_type == "cone":
            radius = random.uniform(1.0, 2.0)
            height = random.uniform(1.0, 3.0)
            distance_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
            mask = distance_from_center < radius
            Z[mask] = np.maximum(Z[mask], elevation + height * (1 - distance_from_center[mask] / radius))
            
            # 添加圆锥的顶部
            top_mask = (np.abs(distance_from_center - radius) < 0.1)  # 圆锥顶部的厚度
            Z[top_mask] = np.maximum(Z[top_mask], elevation + height)
            
            # 确保圆锥顶部与底面之间没有悬空
            for d in np.linspace(0, height, num=10):
                Z[np.logical_and(mask, np.abs(Z - (elevation + d)) < 0.1)] = np.maximum(
                    Z[np.logical_and(mask, np.abs(Z - (elevation + d)) < 0.1)],
                    elevation + d
                )

    return X, Y, Z


def generate_noisy_plane(X, Y, Z, bumpiness):
    # 复制基础Z坐标
    Z_noisy = np.copy(Z)
    
    # 添加轻微随机凹凸 (增加噪声)
    Z_noisy += np.sin(2 * np.pi * X / X.shape[1]) * np.cos(2 * np.pi * Y / Y.shape[0]) * bumpiness
    Z_noisy += np.random.normal(0, bumpiness, Z.shape)  # 添加更多随机噪声
    
    # 添加奇怪的噪点和干扰项
    for _ in range(random.randint(5, 15)):  # 添加随机数量的干扰点
        ix = random.randint(0, X.shape[0] - 1)
        iy = random.randint(0, Y.shape[1] - 1)
        Z_noisy[ix, iy] += random.uniform(-3, 3)  # 随机高度变化，制造突兀点
    
    # 将平面转换为点云
    points_noisy = np.stack((X.ravel(), Y.ravel(), Z_noisy.ravel()), axis=-1)
    return points_noisy

def generate_smooth_plane(X, Y, Z):
    # 直接使用基础Z坐标生成平滑平面
    points_smooth = np.stack((X.ravel(), Y.ravel(), Z.ravel()), axis=-1)
    return points_smooth

def create_point_cloud(points):
    # 创建Open3D点云对象
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    return point_cloud

def save_point_cloud(point_cloud, filename):
    # 保存点云为.ply文件
    o3d.io.write_point_cloud(filename, point_cloud)

# 创建存储点云数据的目录
train_dir = "point_clouds_simulated/train"
val_dir = "point_clouds_simulated/validation"
test_dir = "point_clouds_simulated/test"
smooth_dir = "point_clouds_simulated/smooth"
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)
os.makedirs(smooth_dir, exist_ok=True)

# 生成50套带有硬性凸起和凹陷的点云数据，并基于这些生成相应的平滑无噪点的点云数据
for i in range(50):
    # 随机化每个平面的参数
    groove_depth = random.uniform(0.5, 2.0)
    slope_factor = random.uniform(-0.2, 0.2)
    bumpiness = random.uniform(0.05, 0.15)
    elevation = random.uniform(-1.0, 1.0)
    
    # 生成带有硬性凸起和凹陷的基础平面
    X, Y, Z = generate_hard_features_plane(width=10, height=10, num_points=100, groove_depth=groove_depth, slope_factor=slope_factor, elevation=elevation)
    
    # 基于硬性特征生成带噪点和干扰项的点云
    points_noisy = generate_noisy_plane(X, Y, Z, bumpiness)
    point_cloud_noisy = create_point_cloud(points_noisy)
    
    # 保存带噪点的点云到训练集、验证集和测试集
    train_filename = os.path.join(train_dir, f"bumpy_plane_train_{i+1}.ply")
    val_filename = os.path.join(val_dir, f"bumpy_plane_val_{i+1}.ply")
    test_filename = os.path.join(test_dir, f"bumpy_plane_test_{i+1}.ply")
    
    save_point_cloud(point_cloud_noisy, train_filename)
    save_point_cloud(point_cloud_noisy, val_filename)
    save_point_cloud(point_cloud_noisy, test_filename)
    
    # 基于相同硬性特征生成对应的平滑无噪点的点云
    points_smooth = generate_smooth_plane(X, Y, Z)
    point_cloud_smooth = create_point_cloud(points_smooth)
    
    # 保存到平滑数据集
    smooth_filename = os.path.join(smooth_dir, f"smooth_plane_{i+1}.ply")
    save_point_cloud(point_cloud_smooth, smooth_filename)

print("训练集、验证集、测试集和平滑点云数据生成完成，并分别保存在相应的目录中。")
