# scripts/simple_bot.py

def run(state, memory):

    x, y = state.my_position()
    enemies = state.enemy_positions()

    if enemies:
        target = enemies[0]
        if isinstance(target, dict):
            ex, ey = target["x"], target["y"]
        else:
            ex, ey = target[0], target[1]

        if ex < x:
            move_left()
            aim_left()
        else:
            move_right()
            aim_right()

        shoot()

    return memory

