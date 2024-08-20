from pathlib import Path
import numpy as np
import open3d as o3d
import pythreejs as p3
from IPython.display import display

def test():
    print('test')

class PointCloudUtils:

    def __init__(self):
        pass


    def test_in_class():
        print('test_in_class')
        


    def load_point_cloud(file_path: str) -> dict:
        """
        加载点云数据，并返回一个包含点云及相关信息的字典。

        支持的文件格式包括：
        - .ply: Polygon File Format
        - .pcd: Point Cloud Data
        - .off: Object File Format
        
        参数:
        - file_path (str): 点云文件的路径。

        返回:
        - dict: 包含以下键的字典：
            - "points" (np.ndarray): 点云坐标数据，形状为 (n, 3)，表示点的 (x, y, z) 坐标。
            - "colors" (np.ndarray or None): RGB 颜色数据，形状为 (n, 3)，表示每个点的 (r, g, b) 颜色值。若文件不包含颜色数据，则为 None。
            - "normals" (np.ndarray or None): 法向量数据，形状为 (n, 3)，表示每个点的法向量 (nx, ny, nz)。若文件不包含法向量数据，则为 None。
            - "intensity" (np.ndarray or None): 强度数据，形状为 (n, 1)，表示每个点的强度值（主要用于激光雷达数据）。若文件不包含强度数据，则为 None。
            - "faces" (np.ndarray or None): 面数据，形状为 (m, k)，表示面片的顶点索引，其中 m 是面片数量，k 是顶点数量（通常为 3 或 4）。若文件不包含面数据，则为 None。

        异常:
        - FileNotFoundError: 如果文件不存在，则抛出此异常。
        - ValueError: 如果文件格式不受支持，则抛出此异常。

        示例:
        ```python
        point_cloud_data = load_point_cloud('example.ply')
        points = point_cloud_data["points"]
        colors = point_cloud_data["colors"]
        normals = point_cloud_data["normals"]
        faces = point_cloud_data["faces"]
        ```

        支持的文件格式说明:
        - `.ply`: 可存储点云的坐标、颜色和法向量信息，支持 ASCII 和二进制两种编码方式。该函数会尝试读取所有相关数据。
        - `.pcd`: 点云库（PCL）专用格式，可能包含点云的坐标、颜色、法向量以及强度数据。函数会根据文件内容读取相关数据。
        - `.off`: 用于几何模型，通常包含顶点和面片信息。该函数会读取点坐标和面数据，但通常不包含颜色和法向量信息。

        注意事项:
        - 如果文件中不存在某些数据（如颜色或法向量），则对应的返回值将为 None。
        - 对 `.off` 文件，函数将解析文件头以确定顶点和面片的数量，并返回相应数据。
        - 函数当前未实现对 `.pcd` 文件中的强度数据读取，若有需要可进行扩展。

        潜在扩展:
        - 可扩展以支持其他点云文件格式（如 `.xyz`, `.las`）。
        - 可实现对强度数据的支持，以便更好地处理激光雷达数据。
        """

        file_path = Path(file_path)
        
        # 检查文件是否存在
        if not file_path.exists():
            raise FileNotFoundError(f"文件 '{file_path}' 不存在。")

        point_cloud_data = {
            "points": None,
            "colors": None,
            "normals": None,
            "intensity": None,
            "faces": None,
        }

        # 处理 .ply 和 .pcd 格式
        if file_path.suffix.lower() in ['.ply', '.pcd']:
            point_cloud = o3d.io.read_point_cloud(str(file_path))
            point_cloud_data["points"] = np.asarray(point_cloud.points)

            # 如果文件包含颜色数据，则读取；否则为 None
            point_cloud_data["colors"] = (
                np.asarray(point_cloud.colors) if point_cloud.has_colors() else None
            )
            # 如果文件包含法向量数据，则读取；否则为 None
            point_cloud_data["normals"] = (
                np.asarray(point_cloud.normals) if point_cloud.has_normals() else None
            )
            # 目前不处理强度数据
            point_cloud_data["intensity"] = None

        # 处理 .off 格式
        elif file_path.suffix.lower() == '.off':
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # 解析文件头部信息
            header_line = lines[0].strip()
            if header_line.startswith("OFF"):
                header_info = header_line[3:].strip()
                start_line = 2 if not header_info else 1
                if not header_info:
                    header_info = lines[1].strip()
            else:
                header_info = header_line
                start_line = 1

            # 解析点和面片的数量
            header_values = header_info.split()
            num_points = int(header_values[0])
            num_faces = int(header_values[1]) if len(header_values) > 1 else 0

            # 读取点数据
            points = [
                list(map(float, line.strip().split()[:3]))
                for line in lines[start_line:start_line + num_points]
            ]
            point_cloud_data["points"] = np.array(points)

            # OFF 文件通常不包含颜色和法向量数据
            point_cloud_data["colors"] = None
            point_cloud_data["normals"] = None

            # 读取面片数据，如果存在
            faces = [
                list(map(int, line.strip().split()[1:]))
                for line in lines[start_line + num_points:start_line + num_faces]
            ] if num_faces > 0 else None

            point_cloud_data["faces"] = np.array(faces) if faces else None

        else:
            raise ValueError(f"不支持的文件格式: {file_path.suffix}")

        return point_cloud_data


    def render_point_cloud_with_axes(points_array: np.ndarray = None,
                                    colors_array: np.ndarray = None,
                                    normals_array: np.ndarray = None,
                                    intensity_array: np.ndarray = None,
                                    file_path: str = None, 
                                    point_size: float = 0.05, 
                                    axis_length: float = None, 
                                    canvas_dimensions: tuple = (400, 300),
                                    point_color: str = '#00ff00',
                                    max_points: int = None, 
                                    show_axes: bool = True,
                                    show_light: bool = True):
        """
        渲染点云数据并显示在 Jupyter Notebook 中，带有可选的坐标轴和光照。

        参数:
        - points_array (np.ndarray, optional): 点云数据数组，形状为 (n, 3)。如果提供，直接使用此数据进行渲染。
        - file_path (str, optional): 点云文件路径。支持 .ply, .pcd, .off 文件格式。如果提供，将从文件加载点云数据。
        - point_size (float, optional): 点的大小, 越大越清晰，默认为 0.05。
        - axis_length (float, optional): 坐标轴的长度。默认根据点云数据自动计算为点云范围的一半。
        - canvas_dimensions (tuple, optional): 渲染画布的尺寸 (宽度, 高度)，默认为 (400, 300)。
        - point_color (str, optional): 点的颜色，使用 HTML 颜色表示，默认为绿色 '#00ff00'。
        - max_points (int, optional): 最大渲染点数。若提供，且点云数据点数超过此值，将进行随机采样。若不提供，渲染全部点云数据。
        - show_axes (bool, optional): 是否显示坐标轴，默认为 True。
        - show_light (bool, optional): 是否启用光照，默认为 True。

        返回:
        - None: 函数会直接在 Jupyter Notebook 中渲染点云，不返回值。

        异常:
        - ValueError: 如果未提供 `points_array` 或 `file_path`，抛出此异常。
        - TypeError: 如果 `points_array` 不是 numpy 数组，或 `canvas_dimensions` 格式不正确，抛出此异常。
        - ValueError: 如果 `points_array` 是空的，或形状不为 (n, 3)，抛出此异常。

        示例:
        >>> render_point_cloud_with_axes(file_path="example.ply", point_size=0.1, axis_length=2.0, canvas_dimensions=(600, 400))
        >>> points_array = np.random.rand(100, 3)  # 生成 100 个随机点
        >>> render_point_cloud_with_axes(points_array=points_array, point_size=0.1, axis_length=2.0, canvas_dimensions=(600, 400))
        """
        

        # 如果提供了 file_path，则从文件加载点云数据
        if file_path:
            point_cloud_data = PointCloudUtils.load_point_cloud(file_path)
            points_array = point_cloud_data["points"]  # 仅提取点数据进行渲染
            colors_array = point_cloud_data.get("colors", None)  # 尝试提取颜色数据
            normals_array = point_cloud_data.get("normals", None)  # 尝试提取法向量数据
            # intensity_array = point_cloud_data.get("intensity", None)  # 尝试提取强度数据
            # faces_array = point_cloud_data.get("faces", None)  # 尝试提取强度数据
        elif points_array is None:
            raise ValueError("必须提供 points_array 或 file_path 之一。")

        # 验证 points_array 是否为 numpy 数组
        if not isinstance(points_array, np.ndarray):
            raise TypeError("points_array 应为 numpy 数组")
        if points_array.size == 0:
            raise ValueError("points_array 为空")
        if points_array.shape[1] != 3:
            raise ValueError("points_array 的形状应为 (n, 3)")
        if not (isinstance(canvas_dimensions, tuple) and len(canvas_dimensions) == 2 
                and all(isinstance(dim, int) for dim in canvas_dimensions)):
            raise TypeError("canvas_dimensions 应为包含两个整数的 tuple")

        # 数据采样（仅当 max_points 被指定时）
        if max_points is not None and len(points_array) > max_points:
            indices = np.random.choice(len(points_array), max_points, replace=False)
            points_array = points_array[indices]

        # 如果 axis_length 未指定，则根据点云范围自动计算
        if axis_length is None:
            axis_length = np.linalg.norm(np.ptp(points_array, axis=0)) * 0.5

        canvas_width, canvas_height = canvas_dimensions

        # 创建点云参数
        attributes = {
            'position': p3.BufferAttribute(points_array, normalized=False),
        }

        if colors_array is not None:
            attributes['color'] = p3.BufferAttribute(colors_array, normalized=True)

        if normals_array is not None:
            attributes['normal'] = p3.BufferAttribute(normals_array, normalized=True)

        
        # 创建点云的几何和材质
        geometry = p3.BufferGeometry(attributes=attributes)

        material = p3.PointsMaterial(size=point_size, vertexColors='VertexColors')

        point_cloud = p3.Points(geometry=geometry, material=material)

        scene_children = [point_cloud]

        # 如果指定显示坐标轴，则添加坐标轴
        if show_axes:
            axis_data = {
                'positions': [
                    [0, 0, 0], [axis_length, 0, 0],  # X轴
                    [0, 0, 0], [0, axis_length, 0],  # Y轴
                    [0, 0, 0], [0, 0, axis_length]   # Z轴
                ],
                'colors': [
                    [1, 0, 0], [1, 0, 0],  # X轴为红色
                    [0, 1, 0], [0, 1, 0],  # Y轴为绿色
                    [0, 0, 1], [0, 0, 1]   # Z轴为蓝色
                ]
            }

            axis_geometry = p3.BufferGeometry(
                attributes={
                    'position': p3.BufferAttribute(np.array(axis_data['positions'], dtype=np.float32), normalized=False),
                    'color': p3.BufferAttribute(np.array(axis_data['colors'], dtype=np.float32), normalized=False)
                }
            )

            axis_material = p3.LineBasicMaterial(vertexColors='VertexColors')
            scene_children.append(p3.LineSegments(geometry=axis_geometry, material=axis_material))

        # 如果指定显示光照，则添加光照
        if show_light:
            scene_children.append(p3.AmbientLight(color='#ffffff'))

        # 创建场景并渲染
        scene = p3.Scene(children=scene_children)
        camera = p3.PerspectiveCamera(position=[0, 0, 3], fov=75, aspect=canvas_width/canvas_height)
        renderer = p3.Renderer(camera=camera, scene=scene, controls=[p3.OrbitControls(controlling=camera)],
                            width=canvas_width, height=canvas_height)

        display(renderer)

    # 示例代码
    # render_point_cloud_with_axes(file_path="path/to/your/file.off", point_size=0.1, axis_length=2.0, canvas_dimensions=(400, 300))
    # render_point_cloud_with_axes(points_array=np.random.rand(100, 3), point_size=0.1, axis_length=2.0, canvas_dimensions=(600, 400))
