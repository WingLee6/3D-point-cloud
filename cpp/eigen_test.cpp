#include <iostream>
#include <Eigen/Dense> // 包含Eigen库

int main() {
    // 定义两个2x2矩阵
    Eigen::Matrix2d matA;
    Eigen::Matrix2d matB;

    // 初始化矩阵
    matA << 1, 2,
            3, 4;
    matB << 5, 6,
            7, 8;

    // 计算矩阵之和
    Eigen::Matrix2d matC = matA + matB;

    // 输出结果
    std::cout << "Matrix A:\n" << matA << std::endl;
    std::cout << "Matrix B:\n" << matB << std::endl;
    std::cout << "Sum of A and B:\n" << matC << std::endl;

    return 0;
}
