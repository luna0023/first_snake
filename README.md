# 贪吃蛇 Snake（pygame 版）

基于 Python + pygame 的经典贪吃蛇小游戏，核心逻辑与渲染分离，附带完整单元测试。

## 功能特性

- 方向键 / WASD 控制，禁止 180° 直接掉头
- 吃食物得分、蛇身变长
- 撞墙或撞自己即游戏结束，空格重新开始
- 30×20 网格地图，实时计分

## 环境要求

- Python 3.10+
- pygame 2.x

## 安装与运行

```powershell
# 1. 创建虚拟环境（首次，仅需一次）
python -m venv .venv

# 2. 安装依赖
.\.venv\Scripts\pip.exe install pygame

# 3. 运行游戏
.\.venv\Scripts\python.exe snake_game.py
```

## 运行测试

```powershell
.\.venv\Scripts\pip.exe install pytest
.\.venv\Scripts\python.exe -m pytest test_snake_game.py -v
```

预期输出：`13 passed`

## 项目结构

```
first_snake/
├── snake_game.py        # 游戏本体（核心逻辑为纯函数，可单测）
├── test_snake_game.py   # 单元测试（13 项）
├── PLAN.md              # 项目计划与决策记录
├── .gitignore
└── README.md
```

## 操作说明

| 按键 | 功能 |
|------|------|
| 方向键 / WASD | 控制移动方向 |
| 空格 | 游戏结束后重新开始 |
| ESC / 关闭窗口 | 退出游戏 |

## 可调参数

见 [snake_game.py](snake_game.py) 顶部常量：`CELL_SIZE`（格子大小）、`GRID_WIDTH / GRID_HEIGHT`（地图尺寸）、`FPS`（速度）。
