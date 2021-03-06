# Simple Data Maker
## 简单数据生成器
----------------

一个用于OI/ACM题目的简单数据生成器

### 用法
将程序文件、配置文件`config.json`和标准程序（或其源代码）放入同一个文件夹下，按照需要修改配置文件`config.json`，运行程序文件，即可生成输入输出数据。
由于`config.json`支持了schema，理论上使用支持的编辑器（如Visual Studio Code）打开`config.json`就可以使用代码补全，将鼠标悬停在关键字上方即可看到提示。

#### 配置文件
配置文件中的`test_range`和`config`是必须属性，前者为含有两个整数的列表，后者为包含若干个data类型的列表。
data类型的定义如下：
- data类型可以是数字或字符串
- data类型可以是包含data类型的列表
- data类型可以是一个对象，它的data属性是一个data类型

数据生成器将会对于`config`中的每一个data类型生成数据，并使用换行符 '\n' 分隔开。
data类型的生成规则如下：
- 若data类型是数字，则直接输出数字
- 若data类型是字符串，分三种情况：
  - 若不包含英文逗号，将以该字符串为字符集随机生成一个字符
  - 若只包含一个英文逗号，将以逗号分隔的数字为区间生成随机整数
  - 若包含两个英文逗号，将以逗号分隔的前两个数字为区间，第三个数字为间隔，生成随机浮点数
- 若data类型是列表，将对于其中每一个data类型生成数据，并使用空格 ' ' 分隔开。
- 若data类型是一个对象，则检查它的属性：
  - repeat: 将data属性重复生成这么多次，默认为1
  - sep: 重复生成的data属性之间用它隔开，默认为' '
  - end: 生成数据最后插入的字符，默认为''
  - distinct: 是否允许生成重复的数据
  - 特别地，若repeat为1且data属性为列表，将在生成列表时使用sep分隔。

#### 示例
以下是配置文件的一个例子：
```js
{
    "$schema": "http://49.233.176.49/project_DataMaker/schema.json",
    "test_range": [1, 10], //生成测试点的区间，用闭区间表示
    "title": "", //题目标题，将用于数据点文件的命名
    "std": "std", //标程文件名
    "std_compile": "g++ std.cpp -o std", //标程的编译命令(如果需要)
    "path": "./data", //生成的数据文件存放目录，默认为./data
    "zip": true, //是否将产生的文件打包
    "config": [
        10, //第一行，输出一个10
        ["10,20", "20,50,0.001"], //第二行，输出两个随机数，第一个数是10~20的整数，第二个是20~50且精度为0.001的浮点数
        { //第三行，输出10个随机整数，每个数字互不相同，且在区间[1,10]中
            "repeat": 10, //表示生成data重复10次，中间插入空格
            "distinct": true, //表示生成的数据互不相同
            "data": "1,10"
        },
        { //第4~6行，输出10个随机整数，每个数字互不相同，且在区间[1,10]中
            "repeat": 3, //生成data重复3次
            "sep": "\n", //中间插入换行
            "data": {
                "repeat": 5, //每行生成data重复5次
                "sep": "   ", //中间插入三个空格
                "data": "ABCD" //每次在"ABCD"中随机选择一个字符
            }
        }
    ]
}
```
**注意：使用时不要在`config.json`中写注释，否则程序会闪退！**

生成的数据样例`1.in`如下：
```
10
14 20.835
3 2 8 7 5 4 10 6 9 1 
B   C   B   D   C   
D   D   C   C   A   
B   B   B   D   D
```
