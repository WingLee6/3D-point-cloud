import open3d as o3d
import numpy as np

# 创建一个光滑的平面
plane = o3d.geometry.TriangleMesh.create_box(width=1.0, height=0.1, depth=1.0)
plane.compute_vertex_normals()
plane = plane.subdivide_midpoint(number_of_iterations=2)
plane.translate([-0.5, -0.05, -0.5])

# 创建槽1
groove1 = o3d.geometry.TriangleMesh.create_box(width=0.1, height=0.12, depth=1.0)
groove1.compute_vertex_normals()
groove1 = groove1.subdivide_midpoint(number_of_iterations=2)
groove1.translate([-0.05, -0.06, -0.5])

# 创建槽2
groove2 = o3d.geometry.TriangleMesh.create_box(width=1.0, height=0.12, depth=0.1)
groove2.compute_vertex_normals()
groove2 = groove2.subdivide_midpoint(number_of_iterations=2)
groove2.translate([-0.5, -0.06, -0.05])

# 生成圆柱
cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=0.05, height=0.12)
cylinder.compute_vertex_normals()
cylinder = cylinder.subdivide_midpoint(number_of_iterations=2)
cylinder.translate([0, -0.06, 0])

# 创建斜面
ramp = o3d.geometry.TriangleMesh.create_box(width=0.4, height=0.02, depth=0.6)
ramp.compute_vertex_normals()
ramp = ramp.subdivide_midpoint(number_of_iterations=2)
ramp.translate([-0.2, 0.02, -0.3])
ramp.rotate(o3d.geometry.get_rotation_matrix_from_xyz((np.pi/6, 0, 0)), center=ramp.get_center())

# 合并所有几何体形成一个复杂工件
combined_mesh = plane + groove1 + groove2 + cylinder + ramp

# 提取表面点云
combined_mesh.compute_vertex_normals()
pcd = combined_mesh.sample_points_poisson_disk(number_of_points=20000)

# 模拟扫描，只保留可见表面点云
camera_location = np.array([2, 2, 2])
_, pt_map = pcd.hidden_point_removal(camera_location, radius=2.5)

# 获取可见点
visible_pcd = pcd.select_by_index(pt_map)

# 可视化点云
o3d.visualization.draw_geometries([visible_pcd])

# 保存可见表面点云为ply文件
o3d.io.write_point_cloud("visible_surface.ply", visible_pcd)
