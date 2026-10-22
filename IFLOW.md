# 身份证图片构造器 (idcard_generator)

## 项目概述

这是一个用于生成身份证图片的Python应用程序，提供图形用户界面(GUI)来输入个人信息并生成黑白和彩色身份证图片。该项目仅用于研究目的，使用时需遵守当地法律法规。

### 主要功能
- 填入个人信息生成身份证图片
- 支持黑白和彩色两种输出格式
- 自动抠图功能（仅支持纯色背景）
- 随机生成身份信息（姓名、出生日期、身份证号）
- 自动调整头像大小
- 生成图片时显示处理进度弹窗
- 智能地址生成：从配置文件中随机选择江苏省内地址
- 统一签发机关：设置为"江苏省徐州市鼓楼分局"
- 精确有效期限：严格20年有效期，确保起始和结束日期月日一致，结束日期在2030年后
- 标准身份证号码：
  - 前六位限制为徐州市各区县代码
  - 倒数第二位性别标识：奇数为男，偶数为女
  - 出生年份限制：1980年及之后

### 技术栈
- **语言**: Python
- **GUI框架**: Tkinter
- **图像处理**: OpenCV、Pillow (PIL)
- **数值计算**: NumPy
- **打包工具**: PyInstaller

## 项目结构

```
idcard_generator--master/
├── main.py                 # 主程序入口
├── main.spec              # PyInstaller打包配置文件
├── setup.py               # Python包安装配置
├── README.md              # 项目说明文档
├── .gitignore             # Git忽略文件配置
├── asserts/               # 资源文件夹
│   ├── empty.png          # 空白图片模板
│   ├── ico.ico            # Windows图标文件
│   ├── ico.icns           # macOS图标文件
│   └── fonts/             # 字体文件夹
│       ├── fzhei.ttf      # 方正黑体字体
│       ├── hei.ttf        # 黑体字体
│       └── ocrb10bt.ttf   # OCR-B字体
├── docs/                  # 文档文件夹
│   └── images/            # 图片文档
│       ├── example_01.png # Windows运行效果图
│       ├── example_macos.png # macOS运行效果图
│       └── result_color.png # 生成结果示例
└── idcard_generator/      # 主要代码包
    ├── __init__.py
    ├── id_card_gui.py     # GUI界面实现
    ├── id_card_utils.py   # 身份证号码生成工具
    ├── loading_alert.py   # 加载提示窗口
    ├── name_utils.py      # 姓名生成工具
    ├── address_utils.py   # 地址生成工具
    ├── address_config.json # 地址配置文件
    └── utils.py           # 通用工具函数
```

## 安装与运行

### 环境要求
- Python 3.x
- numpy==1.20.3
- pillow==8.3.1
- opencv-python==4.5.2.54

### 源码安装
```bash
pip install idcard_generator -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
python main.py
```

### 直接运行
```bash
python main.py
```

## 打包程序

### 安装PyInstaller
```bash
pip install pyinstaller
```

### Windows打包
```bash
# 窗口模式
pyinstaller -i asserts/ico.ico --windowed --clean --noconfirm --onefile --add-data "asserts;asserts" main.py

# 控制台模式（显示日志）
pyinstaller -i asserts/ico.ico -c --clean --noconfirm --onefile --add-data "asserts;asserts" main.py
```

### macOS打包
```bash
# 方法一：使用venv模式
pyinstaller -i asserts/ico.icns --windowed --clean --noconfirm --onefile --add-data ./asserts:./asserts --paths /path/to/venv/lib/python3.7/site-packages main.py

# 方法二：使用spec文件
pyinstaller main.spec
```

## 开发指南

### 核心模块说明

1. **id_card_gui.py**: 主GUI界面实现，包含用户交互逻辑和图片生成流程
2. **id_card_utils.py**: 身份证号码生成和校验工具，包含徐州市区县代码和性别验证逻辑
3. **name_utils.py**: 中文姓名生成工具
4. **address_utils.py**: 地址生成工具，从配置文件中随机选择江苏省内地址
5. **address_config.json**: 地址配置文件，包含江苏省各地地址列表
6. **utils.py**: 通用工具函数，包括路径处理、文本长度计算等
7. **loading_alert.py**: 加载进度提示窗口

### 身份证生成标准
项目遵循中国居民身份证的标准规范：
- 正面：国徽、"中华人民共和国居民身份证"标题、签发机关、有效期限等
- 背面：姓名、性别、民族、出生年月日、住址、公民身份号码等
- 字体：使用方正黑体简体、OCR-B 10 BT和华文细黑等

### 身份证号码规则
- 前六位：徐州市各区县行政区划代码（320302-320382）
- 7-14位：出生年月日（YYYYMMDD）
- 15-16位：顺序码
- 17位：性别码（奇数为男，偶数为女）
- 18位：校验码
- 出生年份限制：1980年及之后

### 有效期限规则
- 严格20年有效期
- 起始和结束日期月日一致（如2021.02.25-2041.02.25）
- 结束日期确保在2030年之后

### 开发注意事项
- 项目包含敏感的身份证生成功能，仅用于研究目的
- 图像处理部分使用OpenCV进行抠图和图像合成
- GUI使用Tkinter实现，确保跨平台兼容性
- 资源文件路径处理考虑了打包后的运行环境

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 GPL-3.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 免责声明

本项目仅用于研究目的，使用者需遵守当地法律法规，因使用本项目产生的任何法律后果由使用者自行承担。

## 联系方式

作者: airobot
邮箱: airobot@airobot.link