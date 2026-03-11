def run(state, memory):

    # print once per second
    t = int(time.time())

    if memory != str(t):

        print("\n====== DEBUG BOT ======")

        x, y = state.my_position()
        print("Position:", (round(x,2), round(y,2)))

        angle = state.my_aim_angle()
        print("Angle:", angle)

        print("Health:", state.my_health())
        print("Fuel:", state.my_fuel())
        print("Score:", state.my_score())

        print("Gun:", state.my_gun())
        print("Ammo:", state.my_ammo())

        enemies = state.enemy_positions()
        print("Enemies:", enemies)

        bullets = state.bullet_positions()
        print("Bullets:", bullets)
        saw_bullets = saw_info(state)

        print("SAW bullets:", saw_bullets)

        grenades = state.active_grenades()
        print("Grenades:", grenades)

        gas_clouds = state.gas_clouds()
        print("Gas clouds:", gas_clouds)

        guns = state.gun_spawns()
        print("Nearby guns:", guns)

        medkits = state.medkit_spawns()
        print("Nearby medkits:", medkits)

        grenades = state.my_grenades()
        print("My grenades:", grenades)

        board = state.leaderboard()
        print("\nLeaderboard:")
        for entry in board:
            print(f"  #{entry['rank']} Player {entry['id']} - K:{entry['kills']} D:{entry['deaths']} K-D:{entry['kd_delta']}")

        print("\nTime remaining:", round(state.time_remaining(), 1), "seconds")

        print("\nLocal map:")

        radius = 6
        m = state.local_map(radius)

        for row in m:
            line = ""
            for cell in row:
                if cell == 0:
                    line += "#"
                else:
                    line += "."
            print(line)

        print("=======================\n")

        memory = str(t)

    move_right()

    if random.random() < 0.02:
        shoot()

    return memory

