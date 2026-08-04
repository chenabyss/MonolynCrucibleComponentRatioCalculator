# 冶炼厂阵列最优配比计算器

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个用于 **Rimworld** 模组 **"冶炼厂阵列"** 的组件配置优化工具，基于作者从游戏中人工提取并验证的数学模型，自动枚举所有可能的组件组合（冷却/超频/分担/散热），在给定产品参数和批量件数下，找出使 **总生产时间（含必要冷却）最短** 的最优配比。
<img width="600" height="580" alt="image" src="https://github.com/user-attachments/assets/ff85756c-7f0d-4bad-9ec6-9fe456db79a2" />

---

## ✨ 特性

- 🎯 **精确模型**：数学模型的各项参数为作者从游戏中人工提取，并经过实测验证，与游戏行为一致。
- ⚡ **批量优化**：支持任意件数，自动插入最优冷却策略（冷却到恰好容纳下一件），确保生产安全。
- 🖥️ **图形界面**：基于 `tkinter`，开箱即用，无需安装额外库。
- ⌨️ **命令行支持**：适合脚本集成或批量处理（`optimizer_cli.py`）。
- 🚀 **快速计算**：枚举 60 个槽位所有组合耗时 < 1 秒。
- 📦 **预编译版本**：Windows 可执行文件可直接下载运行，无需 Python 环境。

---

## 📥 下载与安装

### 方式一：直接使用预编译的 Windows 可执行文件（推荐）
- 前往本仓库的 [Releases](https://github.com/chenabyss/MonolynCrucibleComponentRatioCalculator/releases) 页面下载 `optimizer_gui.exe`。
- 双击运行即可，无需安装 Python。

### 方式二：从源码运行（需要 Python 3.6+）
```bash
git clone https://github.com/chenabyss/MonolynCrucibleComponentRatioCalculator.git
cd MonolynCrucibleComponentRatioCalculator
python optimizer_gui.py          # 启动图形界面
# 或
python optimizer_cli.py -r 50 -p 69.1 -N 10   # 命令行使用
```

---

## 📖 使用方法

### 图形界面（GUI）
1. 从下拉菜单选择预设产品（或手动输入 `r` 和 `p`）。
2. 输入生产件数 `N`，组件总数上限（默认60）和安全裕度（建议 `1.0`）。
3. 点击 **"计算最优配置"**，结果将显示在下方的文本框中。

**参数说明**：
- **散热量 r**：产品每小时产生的热量（热量/小时）。
- **基础加工时间 p**：无超频时的加工时间（小时）。
- **生产件数 N**：需要连续生产的件数。
- **组件总数上限**：可用的组件总数量（默认 60）。
- **安全裕度 margin**：为避免临界爆炸而保留的热量余量（建议 `1.0`，已通过测试验证）。

### 命令行（CLI）
```bash
python optimizer_cli.py -r <散热量> -p <加工时间> -N <件数> [--slots 上限] [--margin 裕度]
```
示例：
```bash
python optimizer_cli.py -r 50 -p 69.1 -N 10 --slots 60 --margin 1.0
```

---

## 📐 数学模型

### 基础参数
| 参数 | 符号 | 取值 |
|------|------|------|
| 基础冷却速度（无组件） | `base` | 5（热量/小时） |
| 冷却组件加成 | `+8c` | 每个冷却组件提供 +8 散热速率，受效率影响 |
| 超频组件效果 | `o` | 每个：工序速度 +25%（即 `1+0.25o`），冷却效率 -10%（因子 `1-0.10o`） |
| 分担组件效果 | `s` | 每个：热容量上限 +25（即 `100+25s`） |
| 散热组件效果 | `h` | 每个：冷却效率 +7%（因子 `1+0.07h`） |

### 冷却速度公式（含取整和下限）

```math
raw = (5 + 8c) \times (1 - 0.10\, o + 0.07\, h)
```

```math
c_{\text{cool}} = \max\left(2,\; \lfloor raw \rfloor \right)
```

其中 `floor` 为向下取整，下限 2 表示冷却速度最小为 2（即使计算值为负或小于 2，也显示为 2）。

### 单件生产

- 实际加工时间：

  ```math
  t_{\text{prod}} = \frac{p}{1 + 0.25\, o}
  ```

- 单件净产热：

  ```math
  \Delta H = (r - c_{\text{cool}}) \cdot t_{\text{prod}}
  ```

- 热容量上限：

  ```math
  C_{\max} = 100 + 25\, s
  ```

- **可行条件**（带裕度）：

  ```math
  \Delta H \le C_{\max} - \text{margin}
  ```

建议 `margin = 1.0` 以避免离散误差导致的爆炸。

### 批量生产（N件，离散模拟）

1. 初始化当前热量 `heat = 0`，总时间 `total_time = 0`。
2. 对每一件产品：

若 $heat+\Delta H>C_{\max}$，则先冷却：

$$
\mathrm{cool\_time} = \frac{heat+\Delta H-C_{\max}}{c_{\mathrm{cool}}}
$$

$$total\_{time} += t_{\mathrm{cool}}$$，并将 `heat` 设为 $C_{\max}-\Delta H$（冷却到恰好能容纳下一件）。
然后生产：

$$
total\_{time} \leftarrow total\_{time}+t_{\mathrm{prod}}
$$

$$
heat \leftarrow heat+\Delta H
$$

3. 返回 `total_time`。

> **验证数据**：对"神圣机械心脏"（`r=50, p=69.1`）生产 10 件，最优配置为 `c=1, o=53, s=6, h=0`，总时间约 49.8 小时，实测安全。

---

## 🛠️ 开发者指南

### 打包为独立 EXE（Windows）
使用 PyInstaller：
```bash
pip install pyinstaller
pyinstaller --onefile --console optimizer_gui.py   # 带控制台（调试用）
# 或
pyinstaller --onefile --windowed optimizer_gui.py  # 无控制台（发布用）
```
生成的 `dist/optimizer_gui.exe` 即可分发。

> **注意**：若 `--windowed` 版本双击无反应，请改用 `--console` 版本，或参考 [常见问题](#常见问题) 解决 Tcl/Tk 依赖问题。

### 修改组件常数
在 `optimizer_core.py` 中调整以下变量即可适配游戏更新：
```python
BASE_COOL = 5          # 基础冷却速度
COOL_ADD = 8           # 每个冷却组件加成
SPEED_O = 0.25         # 超频速度加成
EFFICIENCY_O = -0.10   # 超频效率影响
EFFICIENCY_H = 0.07    # 散热效率影响
```

---

## 📁 文件结构

```
.
├── optimizer_core.py       # 核心计算逻辑（无界面）
├── optimizer_gui.py        # 图形界面程序
├── optimizer_cli.py        # 命令行界面
├── LICENSE                 # MIT 许可证
├── README.md               # 本文档
└── .gitignore              # Git 忽略规则
```

---

## 🤝 贡献

欢迎提出 Issue 或 Pull Request。请确保代码符合 PEP8 风格，并对核心函数编写简单测试。

---

## ❓ 常见问题

**Q: 双击 `optimizer_gui.exe` 没有反应怎么办？**  
A: 可能是 Tcl/Tk 依赖未正确打包。请尝试：
- 在命令行中运行 `optimizer_gui.exe` 查看错误信息。
- 改用 `--console` 版本重新打包，或从 Releases 下载带控制台的版本。
- 若报错缺少 `tcl86t.dll`，可将 Python 安装目录下的 `tcl` 和 `tk` 文件夹复制到 exe 同级目录。

**Q: 如何添加新的预设产品？**  
A: 在 `optimizer_gui.py` 中的 `PRESETS` 字典中添加条目即可。

---

## 📄 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

---

## 📬 联系方式

如有问题，请通过 [GitHub Issues](https://github.com/chenabyss/MonolynCrucibleComponentRatioCalculator/issues) 反馈。
