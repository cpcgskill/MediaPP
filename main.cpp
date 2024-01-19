// main.cpp
// Purpose: 一个简单的C++程序，用于启动python解释器
// Author: 苍之幻灵
// Date: 2024/1/19 23:58

#include <iostream>

int main() {
    std::cout << "Open Python Interpreter" << std::endl;
    // 运行当前目录下的python的python解释器， 并且为了让外部脚本能够设置启动的文件，需要预先设置模板字符串
    return system(".\\python.exe {{{{script}}}}");
}
