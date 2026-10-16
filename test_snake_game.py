"""snake_game 核心逻辑单元测试（不涉及 GUI 渲染）。

运行方式：
    .\\.venv\\Scripts\\python.exe -m pytest test_snake_game.py -v
"""

import snake_game as g


def make_state(snake, direction=g.RIGHT, food=(0, 0), score=0, game_over=False):
    """构造一份可控的游戏状态。"""
    return {
        "snake": list(snake),
        "direction": direction,
        "pending_direction": direction,
        "food": food,
        "score": score,
        "game_over": game_over,
    }


# ---------- reset_game ----------

def test_reset_game_initial_state():
    state = g.reset_game()
    assert len(state["snake"]) == 3
    assert state["direction"] == g.RIGHT
    assert state["pending_direction"] == g.RIGHT
    assert state["score"] == 0
    assert state["game_over"] is False
    # 蛇身坐标都在网格内，且食物不在蛇身上
    for x, y in state["snake"]:
        assert 0 <= x < g.GRID_WIDTH
        assert 0 <= y < g.GRID_HEIGHT
    assert state["food"] not in state["snake"]


# ---------- random_food ----------

def test_random_food_never_on_snake():
    snake = [(5, 5), (4, 5), (3, 5)]
    for _ in range(200):
        food = g.random_food(snake)
        assert food not in snake
        assert 0 <= food[0] < g.GRID_WIDTH
        assert 0 <= food[1] < g.GRID_HEIGHT


def test_random_food_only_one_empty_cell():
    # 蛇占满全屏仅留 (7, 8)，食物必然生成在该格
    only_empty = (7, 8)
    snake = [
        (x, y)
        for x in range(g.GRID_WIDTH)
        for y in range(g.GRID_HEIGHT)
        if (x, y) != only_empty
    ]
    assert g.random_food(snake) == only_empty


# ---------- step：移动与进食 ----------

def test_step_moves_forward_without_growth():
    state = make_state(snake=[(5, 5), (4, 5), (3, 5)], direction=g.RIGHT, food=(10, 10))
    g.step(state)
    assert state["snake"] == [(6, 5), (5, 5), (4, 5)]  # 长度不变，整体前移
    assert state["score"] == 0
    assert state["game_over"] is False


def test_step_eat_food_grows_and_scores():
    state = make_state(snake=[(5, 5), (4, 5), (3, 5)], direction=g.RIGHT, food=(6, 5))
    g.step(state)
    assert len(state["snake"]) == 4
    assert state["snake"][0] == (6, 5)
    assert state["score"] == 1
    # 新食物已重新生成且不在蛇身上
    assert state["food"] != (6, 5)
    assert state["food"] not in state["snake"]


def test_step_applies_pending_direction():
    state = make_state(snake=[(5, 5), (4, 5), (3, 5)], direction=g.RIGHT, food=(10, 10))
    state["pending_direction"] = g.DOWN
    g.step(state)
    assert state["direction"] == g.DOWN
    assert state["snake"][0] == (5, 6)


# ---------- step：碰撞检测 ----------

def test_step_hit_wall_ends_game():
    # 头紧贴右边界继续向右
    state = make_state(snake=[(g.GRID_WIDTH - 1, 5), (g.GRID_WIDTH - 2, 5)], direction=g.RIGHT)
    g.step(state)
    assert state["game_over"] is True


def test_step_hit_self_ends_game():
    # 头 (2,2) 向左进入身体 (1,2)
    state = make_state(snake=[(2, 2), (1, 2), (1, 1), (2, 1)], direction=g.LEFT, food=(10, 10))
    g.step(state)
    assert state["game_over"] is True


def test_step_moving_into_vacated_tail_is_safe():
    """回归测试：头追尾尖移动（本帧不吃食物，尾巴会移走）不应判撞。"""
    # 蛇围成一圈：头 (1,2)，尾尖 (2,2)；向右移动后尾尖恰好让位
    state = make_state(snake=[(1, 2), (1, 1), (2, 1), (2, 2)], direction=g.RIGHT, food=(10, 10))
    g.step(state)
    assert state["game_over"] is False
    assert state["snake"] == [(2, 2), (1, 2), (1, 1), (2, 1)]


def test_step_does_nothing_when_game_over():
    state = make_state(snake=[(5, 5), (4, 5), (3, 5)], food=(10, 10), game_over=True)
    snapshot = {k: (list(v) if k == "snake" else v) for k, v in state.items()}
    g.step(state)
    assert state["snake"] == snapshot["snake"]
    assert state["score"] == snapshot["score"]


# ---------- try_change_direction ----------

def test_try_change_direction_blocks_reverse():
    state = make_state(snake=[(5, 5), (4, 5), (3, 5)], direction=g.RIGHT)
    assert g.try_change_direction(state, g.LEFT) is False
    assert state["pending_direction"] == g.RIGHT  # 未被修改


def test_try_change_direction_allows_turn():
    state = make_state(snake=[(5, 5), (4, 5), (3, 5)], direction=g.RIGHT)
    assert g.try_change_direction(state, g.UP) is True
    assert state["pending_direction"] == g.UP


def test_turn_then_reverse_is_blocked_next_frame():
    """向右移动中先转上，下一帧再试图向左（相对新方向是掉头）应被拒绝。"""
    state = make_state(snake=[(5, 5), (4, 5), (3, 5)], direction=g.RIGHT)
    g.try_change_direction(state, g.UP)
    g.step(state)  # 此时 direction 已变为 UP
    assert g.try_change_direction(state, g.DOWN) is False
    assert state["pending_direction"] == g.UP
