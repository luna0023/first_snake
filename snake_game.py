"""贪吃蛇小游戏（pygame 版）

操作说明：
  - 方向键 / WASD：控制移动方向
  - 空格：游戏结束后重新开始
  - ESC / 关闭窗口：退出游戏
"""

import random
import sys
from pathlib import Path

import pygame

# ---------- 常量配置 ----------
CELL_SIZE = 20          # 每格像素
GRID_WIDTH = 30         # 网格列数
GRID_HEIGHT = 20        # 网格行数
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10                # 蛇移动速度（帧率）

# 颜色 (R, G, B)
COLOR_BG = (15, 15, 25)
COLOR_GRID = (30, 30, 45)
COLOR_SNAKE_HEAD = (80, 220, 100)
COLOR_SNAKE_BODY = (40, 160, 70)
COLOR_FOOD = (230, 70, 70)
COLOR_TEXT = (230, 230, 230)

# 方向向量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def random_food(snake: list[tuple[int, int]]) -> tuple[int, int]:
    """在蛇身以外的空格中随机生成食物位置。"""
    empty = [
        (x, y)
        for x in range(GRID_WIDTH)
        for y in range(GRID_HEIGHT)
        if (x, y) not in snake
    ]
    return random.choice(empty)


def draw_cell(screen: pygame.Surface, pos: tuple[int, int], color: tuple[int, int, int]) -> None:
    """按网格坐标绘制一个方块。"""
    rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, COLOR_BG, rect, 1)  # 描边，形成格子感


def reset_game() -> dict:
    """返回一份初始游戏状态。"""
    center = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
    snake = [center, (center[0] - 1, center[1]), (center[0] - 2, center[1])]
    return {
        "snake": snake,               # 蛇身：头在索引 0
        "direction": RIGHT,           # 当前移动方向
        "pending_direction": RIGHT,   # 下一帧方向（防止一帧内 180 度掉头）
        "food": random_food(snake),
        "score": 0,
        "game_over": False,
    }


def try_change_direction(state: dict, new_dir: tuple[int, int]) -> bool:
    """尝试改变移动方向，禁止 180 度掉头。返回是否生效。"""
    cur = state["direction"]
    if (new_dir[0] + cur[0], new_dir[1] + cur[1]) == (0, 0):
        return False
    state["pending_direction"] = new_dir
    return True


def step(state: dict) -> None:
    """推进一帧游戏逻辑：应用方向、移动蛇、处理碰撞与进食。"""
    if state["game_over"]:
        return

    state["direction"] = state["pending_direction"]
    head_x, head_y = state["snake"][0]
    dx, dy = state["direction"]
    new_head = (head_x + dx, head_y + dy)

    # 撞墙检测
    hit_wall = not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT)
    # 撞自身检测：若本帧吃不到食物，尾巴尖会移走，故排除尾尖
    will_eat = new_head == state["food"]
    body = state["snake"] if will_eat else state["snake"][:-1]
    hit_self = new_head in body

    if hit_wall or hit_self:
        state["game_over"] = True
        return

    state["snake"].insert(0, new_head)
    if will_eat:
        state["score"] += 1
        state["food"] = random_food(state["snake"])
    else:
        state["snake"].pop()  # 没吃到食物则去掉尾巴，保持长度


def load_font(size: int) -> pygame.font.Font:
    """加载中文字体。

    直接指定 Windows 字体文件路径，避开 pygame SysFont
    在部分 Windows 环境下扫描注册表崩溃的已知 bug。
    """
    candidates = [
        r"C:\Windows\Fonts\msyh.ttc",    # 微软雅黑
        r"C:\Windows\Fonts\simhei.ttf",  # 黑体
        r"C:\Windows\Fonts\simsun.ttc",  # 宋体
    ]
    for path in candidates:
        if Path(path).exists():
            return pygame.font.Font(path, size)
    # 找不到中文字体时退回 pygame 默认字体（中文可能显示为方块）
    return pygame.font.Font(None, size)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("贪吃蛇 Snake")
    clock = pygame.time.Clock()
    font = load_font(24)
    big_font = load_font(48)

    state = reset_game()

    # 按键到方向的映射
    key_to_dir = {
        pygame.K_UP: UP, pygame.K_w: UP,
        pygame.K_DOWN: DOWN, pygame.K_s: DOWN,
        pygame.K_LEFT: LEFT, pygame.K_a: LEFT,
        pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT,
    }

    while True:
        # ---------- 事件处理 ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if state["game_over"]:
                    if event.key == pygame.K_SPACE:
                        state = reset_game()
                elif event.key in key_to_dir:
                    try_change_direction(state, key_to_dir[event.key])

        # ---------- 逻辑更新 ----------
        step(state)

        # ---------- 绘制 ----------
        screen.fill(COLOR_BG)

        # 网格线
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, COLOR_GRID, (0, y), (WINDOW_WIDTH, y))

        # 食物
        draw_cell(screen, state["food"], COLOR_FOOD)

        # 蛇（头与身体不同颜色）
        for i, segment in enumerate(state["snake"]):
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            draw_cell(screen, segment, color)

        # 分数
        score_surf = font.render(f"得分: {state['score']}", True, COLOR_TEXT)
        screen.blit(score_surf, (10, 8))

        # 游戏结束提示
        if state["game_over"]:
            over_surf = big_font.render("游戏结束", True, COLOR_TEXT)
            tip_surf = font.render("按 空格 重新开始，ESC 退出", True, COLOR_TEXT)
            over_rect = over_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
            tip_rect = tip_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            screen.blit(over_surf, over_rect)
            screen.blit(tip_surf, tip_rect)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
