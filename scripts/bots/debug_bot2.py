# scripts/debug_bot2.py

def run(state, memory):

    t = now()

    # Memory format: "last_scan_time|frame_counter"
    if memory == "":
        last_scan = 0.0
        frame_counter = 0
    else:
        try:
            parts = memory.split("|")
            last_scan = float(parts[0])
            frame_counter = int(parts[1])
        except:
            last_scan = 0.0
            frame_counter = 0

    # ---- 1/4 speed movement ----
    if frame_counter % 4 == 0:
        move_right()

    frame_counter += 1

    # ---- Scan once per second ----
    if t - last_scan >= 1.0:

        print("\n=== LIDAR SCAN ===")

        RAYS = 36
        MAX_DIST = 300.0
        GRID_SIZE = 21
        CENTER = GRID_SIZE // 2

        grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        grid[CENTER][CENTER] = "P"

        for i in range(RAYS):
            theta = (2 * pi() / RAYS) * i
            d = state.distance_to_obstacle(theta)

            if d > MAX_DIST:
                d = MAX_DIST

            norm = d / MAX_DIST

            x = CENTER + int(cos(theta) * norm * (CENTER - 1))
            y = CENTER + int(sin(theta) * norm * (CENTER - 1))

            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                grid[y][x] = "#"

        for row in grid:
            print("".join(row))

        board = state.leaderboard()
        print("\nLeaderboard:")
        for entry in board:
            print(f"  #{entry['rank']} Player {entry['id']} - K:{entry['kills']} D:{entry['deaths']} K-D:{entry['kd_delta']}")

        print("\nTime remaining:", round(state.time_remaining(), 1), "seconds")

        print("==================")

        last_scan = t

    new_memory = f"{last_scan}|{frame_counter}"
    return new_memory[:100]

