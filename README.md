# 冶炼厂阵列最优配比计算器

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个用于Rimworld **“冶炼厂阵列”** 的组件配置优化工具，基于数学模型，自动枚举所有可能的组件组合（冷却/超频/分担/散热），在给定产品参数和批量件数下，找出使总生产时间最短的最优配比。

## ✨ 特性

- 🎯 **精确模型**：冷却速度采用总体乘法，并经向下取整和下限2处理，与游戏实测完全一致。
- ⚡ **批量优化**：支持任意件数，自动插入最优冷却策略（冷却到恰好容纳下一件）。
- 🖥️ **图形界面**：基于 `tkinter`，开箱即用，无需安装额外库。
- ⌨️ **命令行支持**：适合脚本集成或批量处理。
- 🚀 **快速计算**：枚举 60 个槽位所有组合耗时 < 1 秒。

## 📥 下载与安装

### 方式一：直接使用预编译的 Windows 可执行文件 (推荐)
- 前往 [Releases](https://github.com/你的用户名/仓库名/releases) 页面下载 `optimizer_gui.exe`。
- 双击运行即可，无需安装 Python。

### 方式二：从源码运行（需要 Python 3.6+）
```bash
git clone https://github.com/你的用户名/仓库名.git
cd 仓库名
python optimizer_gui.py          # 启动图形界面
# 或
python optimizer_cli.py -r 50 -p 69.1 -N 10   # 命令行使用
