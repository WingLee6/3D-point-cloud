#include <pcl/io/ply_io.h>  // 用于读取PLY文件
#include <pcl/point_types.h>  // 用于定义点类型
#include <pcl/visualization/pcl_visualizer.h>  // 用于可视化点云

int main(int argc, char** argv) {
    // 创建一个点云对象指针，用于存储读取的点云数据
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);

    // 读取PLY文件并将数据加载到点云对象中
    if (pcl::io::loadPLYFile<pcl::PointXYZ>("artifact4.ply", *cloud) == -1) {
        PCL_ERROR("Couldn't read file artifact4.ply \n");
        return -1;
    }
    std::cout << "Loaded " << cloud->width * cloud->height << " data points from PLY file." << std::endl;

    // 创建一个PCLVisualizer对象，用于可视化点云
    pcl::visualization::PCLVisualizer::Ptr viewer(new pcl::visualization::PCLVisualizer("3D Viewer"));
    viewer->setBackgroundColor(0, 0, 0);  // 设置背景颜色为黑色
    viewer->addPointCloud<pcl::PointXYZ>(cloud, "sample cloud");  // 添加点云到可视化窗口
    viewer->setPointCloudRenderingProperties(pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 1, "sample cloud");  // 设置点云渲染属性
    viewer->addCoordinateSystem(1.0);  // 添加坐标系
    viewer->initCameraParameters();  // 初始化摄像机参数

    // 保持窗口打开，直到用户关闭
    while (!viewer->wasStopped()) {
        viewer->spinOnce(100);
    }

    return 0;
}
