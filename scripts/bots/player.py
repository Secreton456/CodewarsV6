def run(state, memory):
    # Gets the time at every call
    t = int(time.time())

    # Attack_mode Boolean
    attack_mode = True

    # Debug mode -----> SET IT TO FALSE WHEN SUBMITTING
    DEBUG_MODE = True

    # Fetches the bot data
    x, y = state.my_position()
    health = state.my_health()
    fuel = state.my_fuel()
    enemy_positions = state.enemy_positions()
    all_players = state.all_players()
    player_markers = state.player_markers()
    gun_spawns = state.gun_spawns()
    medkit_spawns = state.medkit_spawns()
    active_grenades = state.active_grenades()
    saw_bullets_in_view = state.saw_bullets_in_view()
    my_gun = state.my_gun()
    my_ammo = state.my_ammo()
    my_aim_angle = state.my_aim_angle()
    MIN_FIGHT_DISTANCE = 300
    MAX_FIGHT_DISTANCE = 600


    # Initialise memory
    # Right now memory stores only the fuel mode
    if memory == "":
        newmemory = "1"
        FUEL_MODE = 1
    # Storing Memory string as an array
    else:
        try:
            parts = memory.split("|")
            FUEL_MODE = int(parts[0])
        except:
            FUEL_MODE = 1
    # Run away from nearby live grenades with higher priority than normal strafing.
    nades = state.active_grenades()
    nearest_nade = None
    nearest_nade_dist = 1e9
    for g in nades:
        nx = float(g["x"])
        ny = float(g["y"])
        d = math.sqrt((nx - my_x) * (nx - my_x) + (ny - my_y) * (ny - my_y))
        if d < nearest_nade_dist:
            nearest_nade_dist = d
            nearest_nade = g

    if nearest_nade is not None and nearest_nade_dist < GRENADE_ESCAPE_DIST:
        gx = float(nearest_nade["x"])
        memory["nade_escape_dir"] = -1 if my_x < gx else 1
        memory["nade_escape_ticks"] = 18
    elif memory["nade_escape_ticks"] > 0:
        memory["nade_escape_ticks"] -= 1

    escaping_nade = memory["nade_escape_ticks"] > 0

    #FUEL CONSUMPTION MODE 1--->MEMORY
    #FUEL RECHARGING MODE  0--->MEMORY
    # If the fuel goes to zero the fuel recharges till goes upto 50 which is half the fuel
    if FUEL_MODE:
        if fuel<=1:
            newmemory="0"
        else:
            newmemory="1"
    else:
        if fuel<=50:
            newmemory="0"
        else:
            newmemory="1"


    # Go defensive once health is less that 40% of total
    if health<=80:
        attack_mode = False


    # Targeting the closest enemy in view
    if player_markers:
        target = player_markers[0]
        ENEMIES_IN_VIEW =False
        min_distance = int(target["distance"])
        for enemy in player_markers:
            id = int(enemy["id"])
            theta = float(enemy["angle"])
            distance = int(enemy["distance"])
            
            if distance < state.distance_to_obstacle(theta) and distance<=min_distance:
                target = enemy
                min_distance = distance
                ENEMIES_IN_VIEW = True

        id = int(target["id"])
        theta = float(target["angle"])
        distance = int(target["distance"])


        # Debug Mode
        if DEBUG_MODE:
            print(f"id:{id},theta:{theta},distance:{distance}")

        # Better Movement and Aiming
        dx = distance*math.cos(theta)
        dy = distance*math.sin(theta)

        # Normalise aim_error to [-pi,pi]
        aim_error = theta - my_aim_angle
        if aim_error > math.pi:
            aim_error -= 2.0 * math.pi
        elif aim_error < -math.pi:
            aim_error += 2.0 * math.pi


        # If enemies are in view move towards the in case of attack mode else move away
        if attack_mode and ENEMIES_IN_VIEW:
            if theta<math.pi/2 and theta> -math.pi/2:
                move_right()
            else:
                move_left()

            if theta < 0:
                if FUEL_MODE:
                    jetpack()
            
            # Adjust aiming
            if aim_error > 0.01:
                aim_right()
                if distance<MAX_FIGHT_DISTANCE and distance<state.distance_to_obstacle(theta):
                    shoot()
            elif aim_error < -0.01:
                aim_left()
                if  distance<MAX_FIGHT_DISTANCE and distance<state.distance_to_obstacle(theta):
                    shoot() 
        
        # For defense mode go away from the attacker but still shoot
        if (not attack_mode) and ENEMIES_IN_VIEW:
            if theta<math.pi/2 and theta> -math.pi/2:
                move_left()
            else:
                move_right()
            
            if theta > 0:
                if FUEL_MODE:
                    jetpack()

            # Adjust aiming
            if aim_error > 0.01:
                aim_right()
                if  distance<MAX_FIGHT_DISTANCE and distance<state.distance_to_obstacle(theta):
                    shoot()   
            elif aim_error < -0.01:
                aim_left()
                if  distance<MAX_FIGHT_DISTANCE and distance<state.distance_to_obstacle(theta):
                    shoot() 
        
        #SELF-EXPLANATORY ---> If no enemies are in view we choose the closest enemy as the target
        if not ENEMIES_IN_VIEW:
            for enemy in player_markers:
                id = int(enemy["id"])
                theta = float(enemy["angle"])
                distance = int(enemy["distance"])
            
                if distance<=min_distance:
                    target = enemy
                    min_distance = distance

            # IF THERE ARE NO ENEMIES IN VIEW MOVE ALONG THE MOST SPACIOUS DIRECTION
            move_angle = 0
            spatial_distance = state.distance_to_obstacle(0)
            for RAYCASTSTEP in range(0,35):
                RAYCASTANGLE = (2*math.pi/36)*RAYCASTSTEP
                if RAYCASTANGLE >math.pi:
                    RAYCASTANGLE-=2*math.pi
                if spatial_distance < state.distance_to_obstacle(RAYCASTANGLE):
                    spatial_distance = state.distance_to_obstacle(RAYCASTANGLE)
                    move_angle = RAYCASTANGLE

            if move_angle<math.pi/2 and move_angle> -math.pi/2:
                move_right()
            else:
                move_left()
            if theta<0:  
                if FUEL_MODE:                  
                    jetpack()

            if DEBUG_MODE:
                print(f"spatial_distance:{spatial_distance},move_angle:{move_angle},ENEMIES_IN_VIEW:{ENEMIES_IN_VIEW}")



        if my_ammo == 0:
            switch_weapon()

        # Throw grenade when target position is stable long enough (tolerance-based).
        if (
            not escaping_nade
            and (not blocked)
            and distance < 320.0
            and (memory["stable_ticks"] >= STABLE_TICKS_TO_THROW or memory["no_damage_ticks"] >= 10)
            and memory["grenade_tick"] <= 0
        ):
            if grenades["gas"] > 0:
                if grenades["selected_type"] != 3:
                    change_grenade_type()
                else:
                    throw_grenade()
                    memory["grenade_tick"] = GRENADE_COOLDOWN_TICKS
                    did_attack = True
            elif grenades["frag"] > 0:
                if grenades["selected_type"] != 1:
                    change_grenade_type()
                else:
                    throw_grenade()
                    memory["grenade_tick"] = GRENADE_COOLDOWN_TICKS
                    did_attack = True


    return newmemory
