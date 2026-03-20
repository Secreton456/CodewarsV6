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
    if health <= 120:
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
            
            # RIGHT NOW IT CHOOSES A TARGET IN VIEW PLUS MAX TARGET ID ---> TO CHANGE IN THE NEXT COMMIT
            if distance < state.distance_to_obstacle(theta) and distance<=min_distance:
                target = enemy
                min_distance = distance
                ENEMIES_IN_VIEW = True

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
                RAYCASTANGLE = 10*RAYCASTSTEP/math.pi
                if RAYCASTANGLE >math.pi:
                    RAYCASTANGLE-=2*math.pi
                if spatial_distance > state.distance_to_obstacle(RAYCASTANGLE):
                    spatial_distance = state.distance_to_obstacle(RAYCASTANGLE)
                    move_angle = RAYCASTANGLE

            if move_angle<math.pi/2 and move_angle> -math.pi/2:
                move_right()
            else:
                move_left()
            if theta<0:                    
                jetpack()

            if DEBUG_MODE:
                print(f"spatial_distance:{spatial_distance},move_angle:{move_angle}")


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

        #----------------------- Check if enemy in range and attack --------------------------------
        if attack_mode and ENEMIES_IN_VIEW:
            if theta<math.pi/2 and theta> -math.pi/2:
                move_right()
            else:
                move_left()

            if theta < 0:
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
        elif (not attack_mode) and ENEMIES_IN_VIEW:
            if theta<math.pi/2 and theta> -math.pi/2:
                move_left()
            else:
                move_right()
            
            if theta > 0:
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
        

    # -------------------------------------------------------------------------------------------------- #
        if my_ammo == 0:
            switch_weapon()


    newmemory = ""
    return newmemory
