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
    # ----------------------------TO ADD THIS INTO ATTACK MODE LATER ON ------------------------------- #
    if player_markers:
        target = player_markers[0]

        for enemy in player_markers:
            id = int(enemy["id"])
            theta = float(enemy["angle"])
            distance = int(enemy["distance"])

            # RIGHT NOW IT CHOOSES A TARGET IN VIEW PLUS MAX TARGET ID ---> TO CHANGE IN THE NEXT COMMIT
            if distance < state.distance_to_obstacle(theta):
                target = enemy
            else:
                continue

        # Debug Mode
        if DEBUG_MODE:
            for enemy in player_markers:
                print(f'id:{enemy["id"]}, angle: {enemy["angle"]}, distance: {enemy["distance"]}')

        id = int(target["id"])
        theta = float(target["angle"])
        distance = int(target["distance"])

        # BASIC MOVEMENT AND AIMING
        if (theta < math.pi / 2 and theta > 0) or (theta > -math.pi / 2 and theta < 0):
            move_right()
            aim_right()
        else:
            move_left()
            aim_left()

        if theta > 0:
            jetpack()
            aim_up()
        else:
            aim_down()

        if distance < state.distance_to_obstacle(theta):
            shoot()
    # -------------------------------------------------------------------------------------------------- #

    newmemory = ""
    return newmemory
