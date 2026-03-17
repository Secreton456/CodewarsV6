#player_markers gives the position
"""
    Helper for bots: return angle and distance to ALL active players on the map.
    No sensor-radius or quadrant restriction — full map visibility.

    Output format:
    [
        {"id": int, "angle": float, "distance": float},
        ...
    ]

    angle is radians from bot -> player using atan2(dy, dx).
    0 means right, pi/2 means down, -pi/2 means up.
"""

def run(state, memory):
    
    attack_mode = True

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
    min_fight_dist = 300

    if (attack_mode):
        #Find the nearest enemy not blocked by obstacles and aim, then shoot (if in weapon range)
        enemy = player_markers[0]
        for opp in player_markers :
            if opp["distance"] <= enemy["distance"]:
                if distance_to_obstacle(opp["angle"]) > opp["distance"]:
                    #not blocked
                    enemy = opp
                    #make it check if within shooting range
                    if enemy["distance"] < min_fight_dist:
                        #make it aim
                        
                    else:
                        #make it move to the enemy
                        pass
                    
                    #break it here
                

