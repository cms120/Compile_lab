# 测试的使用说明
## 关于文件结构的说明
`build`是包含makefile的目录，在这个目录下包括了makefile和可执行程序

<!-- `test`是包含测试用例的目录，在这个目录下包括了测试用例的文件，之后可以在此目录下添加测试用例 -->

`runtime`是包含了antlr4的目录，在这个目录下包括了antlr4的文件，```无需改动```

`src`是包含源码的目录，在这个目录下包括了源码的文件，之后可以在此目录下添加头文件的定义文件

`include`是包含头文件的目录，在这个目录下包括了自定义的文件，之后可以在此目录下添加自定义的头文件

<!-- `lib`是包含了库文件的目录，在这个目录下包括了googletest的代码，可以直接使用，```无需改动``` -->


<!-- ## 关于文件运行的顺序
1. 启动docker镜像，

    docker  images && docker run -it -v /path/to/local/dir:/path/to/remote/dir my-container my-image bash

2. 进入远程目录，

    cd /path/to/remote/dir

3. cmake编译生成makefile： 
    
    mkdir  build && cd build && cmake ..

4. 编译生成可执行程序并运行测试： 
    
    make -j10 && ./runUnitTests

5. 运行主函数程序： 

    ./project1

make -j4 代表启动四个线程运行，如果没有这个参数，默认是一个线程运行，线程数量可以通过nproc命令获取(docker  内运行，我之前在docker中运行过make -j8，所以这里也可以使用，大家可以根据自己的机器配置来设置)

[参考使用](https://blog.csdn.net/guotianqing/article/details/104055221) -->

## 关于可执行文件的生成
1. 启动docker镜像，

    docker  images && docker run -it -v /path/to/local/dir:/path/to/remote/dir my-container my-image bash

2. 进入远程目录，并删除存在的build文件夹

    cd /path/to/remote/dir

3. 运行脚本文件,生成可执行程序

    sh script/generate.sh

4. 运行主程序，生成文件 （输入文件在input中，output在output中，自己命名）
    
    sh script/runmain.sh (intputfile.sy) (outputfile.ll)
