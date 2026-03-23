def run(state,memory):

    if not memory:
        memory = {
            "roam_dir": 1,
            "roam_ticks": 240,
            "evade_dir": 1,
            "evade_ticks": 0,
            "strafe_dir": 1,
            "strafe_ticks": 0,
            "grenade_tick": 0,
            "dodge_tick": 0,
            "target_id": -1,
            "target_health": -1.0,
            "no_damage_ticks": 0,
            "target_x": 0.0,
            "target_y": 0.0,
            "stable_ticks": 0,
            "last_x": 0.0,
            "last_y": 0.0,
            "stuck_ticks": 0,
            "nade_escape_ticks": 0,
            "nade_escape_dir": 1,
            "fly_tick": 0,
        }
    enemies = state.enemy_positions()
    markers = state.player_markers()
    ammo_cur, _ = state.my_ammo()
    grenades = state.my_grenades()
    health = state.my_health()
    fuel = state.my_fuel()
    current_aim = state.my_aim_angle()
    my_x, my_y = state.my_position()  
    radius=state._sensor_radius()
    stats=state.get_weapon_stats()  



    if enemies:
        bakra=min(enemies,key=lambda e:e["distance"])
        bakra_id=int(bakra["id"])
        ex=float(bakra["x"])
        ey=float(bakra["y"])
        bakra_health=float(bakra["health"])
        dist=float(bakra["distance"])
        dx = ex - my_x
        dy = ey - my_y
        angle = math.atan2(dy, dx)
        # if angle>0 and angle<math.pi/2:
        #     aim_right()
        # elif angle>math.pi/2 and angle<math.pi:
        #     aim_left()
        # elif angle<0 and angle>-math.pi/2:
        #     aim_right()
        # else:
        #     aim_left()            
        aim_error = angle - current_aim
        if aim_error > math.pi:
            aim_error -= 2.0 * math.pi
        elif aim_error < -math.pi:
            aim_error += 2.0 * math.pi

        # Single aim command per frame. AIM_ROTATION_SPEED = 0.12 rad/frame now,
        # so a 180° flip takes ~26 frames instead of ~78.
        if aim_error > 0.01:
            aim_right()   # clockwise: increases angle
        elif aim_error < -0.01:
            aim_left()    # counter-clockwise: decreases angle

        shoot() 
        if ammo_cur==0:
            reload()
    return memory    