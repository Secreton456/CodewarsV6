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
        min_distance = int(target["distance"])
        for enemy in player_markers:
            id = int(enemy["id"])
            theta = float(enemy["angle"])
            distance = int(enemy["distance"])
            
            # RIGHT NOW IT CHOOSES A TARGET IN VIEW PLUS MAX TARGET ID ---> TO CHANGE IN THE NEXT COMMIT
            if distance < state.distance_to_obstacle(theta) and distance<=min_distance:
                target = enemy
                min_distance = distance
            else:
                continue


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
        if attack_mode:
            if theta<math.pi/2 and theta> -math.pi/2:
                move_right()
            else:
                move_left()

            if theta < 0:
                jetpack()
            
            # Adjust aiming
            if aim_error > 0.01:
                aim_right()   
            elif aim_error < -0.01:
                aim_left() 
        
        # For defense mode go away from the attacker but still shoot
        elif not attack_mode:
            if theta<math.pi/2 and theta> -math.pi/2:
                move_left()
            else:
                move_right()
            
            if theta > 0:
                jetpack()

            # Adjust aiming
            if aim_error > 0.01:
                aim_right()   
            elif aim_error < -0.01:
                aim_left() 
        

    # -------------------------------------------------------------------------------------------------- #
        if my_ammo == 0:
            switch_weapon()


    newmemory = ""
    return newmemory
