# PyVis 📊

> 一个基于Python的物理现象可视化Web应用 🚀

## ✨ 功能特点

- 📈 利萨如图形模拟
  - 可调节X、Y频率和相位差
  - 动态/静态显示切换
  - 实时显示频率比和周期
  - 带投影视图显示

- 🌊 驻波模拟
  - 可视化驻波形成过程
  - 显示波节点和波腹点
  - 支持显示前行波和反射波分量
  - 可调节波速和暂停/播放

- 🔄 波的叠加演示
  - 双波叠加效果展示
  - 可调节各波的振幅和频率
  - 实时计算最大振幅和拍频
  - 支持分别显示/隐藏各波形

- 🔭 夫琅禾费矩形孔衍射（当前版本性能较差，后续会优化）
  - 实时计算衍射光强分布
  - 可调节光波长(380-780nm)
  - 可调节矩形孔尺寸和屏距
  - 显示第一级暗纹位置
  - 高精度热图显示
  - 基于夫琅禾费衍射公式

## 🛠️ 技术栈

- 🐍 Python + Flask - 后端框架
- 📊 Plotly.js - 数据可视化
- 🎨 Bootstrap 5 - 前端界面
- 📱 响应式设计 - 支持各种设备
- 🧮 NumPy - 科学计算

## 📦 安装要求

确保你的系统已安装 Python 3.8 或更高版本。

```bash
# 安装依赖
pip install -r requirements.txt
```

## 🚀 快速开始

1. 克隆仓库
```bash
git clone https://github.com/yourusername/PyVis.git
cd PyVis
```

2. 配置Python环境（选择一种方式）

方式一：使用 conda 环境（推荐）
```bash
# 创建并激活conda环境
conda create -n pyvis python=3.8
conda activate pyvis
```

方式二：使用 venv 虚拟环境
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行应用
```bash
python app.py
```

5. 在浏览器中访问 `http://localhost:5001`

## 🔬 物理原理

### 夫琅禾费衍射
- 基于夫琅禾费衍射公式：I(θx,θy) = I₀·sinc²(πa·sinθx/λ)·sinc²(πb·sinθy/λ)
- 其中：
  - I₀ 为中心光强
  - a,b 为矩形孔的宽度和高度
  - λ 为光的波长
  - θx,θy 为衍射角
- 第一级暗纹位置：x = λL/a, y = λL/b
  - L 为屏距
  - 可用于验证实验结果

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 有问题请直接提Issue
