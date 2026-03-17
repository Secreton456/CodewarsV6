
def run(state,memory):
    # Gets the time at every call
    t = int(time.time())

    # Attack_mode Boolean
    attack_mode = True

    # Fetches the bot data
    x,y = state.my_position()
    health = state.my_health()
    fuel = state.my_fuel()
    enemy_positions = state.enemy_positions()
    gun_spawns = state.gun_spawns()
    medkit_spawns = state.medkit_spawns()
    active_grenades = state.active_grenades()
    saw_bullets_in_view = state.saw_bullets_in_view()

    # Initialise memory
    '''if memory == "":
        pass'''

    # Storing Memory string as an array 
    '''else:
        try:
            parts = memory.split("|")
            last_scan = float(parts[0])
        except:
            last_scan = 0.0'''
    
    # If HP goes below 60% use defensive algorithm
    if health<=120:
        attack_mode = False


    # Targeting the closest enemy in view
    target = None
    for enemy in enemy_positions:
        ex,ey = enemy
        theta = math.atan2((ey - y),(ex - x))
        if (x-ex)**2 + (y-ey)**2 < distance_to_obstacle(theta)**2:
            target = enemy
        else:
            continue
    ex,ey = target
    theta = math.atan2((ey - y),(ex - x))
    if ex<x:
        if attack_mode:
            move_left()
            aim_left()
        else:
            move_right()
    else:
        if attack_mode:
            move_right()
            aim_right()
        else:
            move_left()
    if y<ey:
        if attack_mode:
            jetpack()
    if y>ey:
        if not attack_mode:
            jetpack()
    

    newmemory = ""
    return newmemory
    