def run(state, memory):

    r = random.random()

    # Random movement
    if r < 0.25:
        move_left()
    elif r < 0.5:
        move_right()

    # Random aiming
    r2 = random.random()
    if r2 < 0.25:
        aim_left()
    elif r2 < 0.5:
        aim_right()
    elif r2 < 0.75:
        aim_up()
    else:
        aim_down()

    # Random shooting
    if random.random() < 0.4:
        shoot()

    if random.random() < 0.05:
        reload()

    if random.random() < 0.02:
        switch_weapon()

    if random.random() < 0.1:
        jetpack()

    return memory

