#include <iostream>
#include <vector>
#include <algorithm> // 加载算法库

// 定义一个表示矩形的类
class Rectangle {
private:
    double length; // 矩形的长度
    double width;  // 矩形的宽度

public:
    // 构造函数，初始化矩形的长度和宽度
    Rectangle(double len, double wid) : length(len), width(wid) {}

    // 成员函数，计算矩形的面积
    double area() const {
        return length * width;
    }

    // 成员函数，计算矩形的周长
    double perimeter() const {
        return 2 * (length + width);
    }

    // 成员函数，显示矩形的长度和宽度
    void display() const {
        std::cout << "Length: " << length << ", Width: " << width << std::endl;
    }
};

// 定义一个函数，计算并返回向量中所有元素的总和
int sumVector(const std::vector<int>& numbers) {
    int sum = 0;
    for (int num : numbers) {
        sum += num; // 累加每个元素的值
    }
    return sum;
}

int main() {
    // 创建并操作矩形对象
    Rectangle rect(5.0, 3.0);
    rect.display();
    std::cout << "Area: " << rect.area() << std::endl;
    std::cout << "Perimeter: " << rect.perimeter() << std::endl;

    // 创建一个整数向量并初始化
    std::vector<int> numbers = {5, 3, 1, 4, 2};

    std::cout << "Before sorting: ";
    for (int num : numbers) {
        std::cout << num << " "; // 输出排序前的向量元素
    }
    std::cout << std::endl;

    // 使用std::sort函数对向量进行排序
    std::sort(numbers.begin(), numbers.end());

    std::cout << "After sorting: ";
    for (int num : numbers) {
        std::cout << num << " "; // 输出排序后的向量元素
    }
    std::cout << std::endl;

    // 调用sumVector函数计算向量元素的总和
    int totalSum = sumVector(numbers);
    std::cout << "Sum of vector elements: " << totalSum << std::endl;

    return 0; // 程序成功结束
}
