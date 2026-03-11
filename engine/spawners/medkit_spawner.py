import numpy as np
import time
import json
import os
import sys
import random

# Add project root to path so root-level modules are importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config import (MEDKIT_SPAWN_INTERVAL, MEDKIT_PICKUP_RADIUS, 
                    MEDKIT_SPAWN_POINTS, MEDKIT_SPAWN_APPEAR_CHANCE,
                    MEDKIT_SPAWN_ACTIVE_LIFETIME)

class MedkitSpawner:
    """Manages medkit spawning at predefined locations on the map"""
    
    def __init__(self):
        self.spawn_points = MEDKIT_SPAWN_POINTS  # Load from config
        self.active_spawns = []  # List of currently spawned medkits
        self.spawn_cooldowns = []  # Cooldown timers for each spawn point
        self.active_lifetimes = []  # Active time trackers for despawn logic
        self.SPAWN_INTERVAL = MEDKIT_SPAWN_INTERVAL
        self.PICKUP_RADIUS = MEDKIT_PICKUP_RADIUS
        self.SPAWN_APPEAR_CHANCE = MEDKIT_SPAWN_APPEAR_CHANCE
        self.ACTIVE_LIFETIME = MEDKIT_SPAWN_ACTIVE_LIFETIME
        self.collision_map = None
        self.grid_size = None
        self.grid_w = None
        self.grid_h = None
        
    def set_collision_map(self, collision_map, grid_size, grid_w, grid_h):
        """Set collision map for spawn validation"""
        self.collision_map = collision_map
        self.grid_size = grid_size
        self.grid_w = grid_w
        self.grid_h = grid_h
        
    def is_valid_spawn_location(self, x, y, radius=10):
        """Check if a position is valid for spawning (not inside obstacles)"""
        if self.collision_map is None:
            return True  # If no collision map, assume valid
            
        # Check all grid cells that the circle overlaps
        min_grid_x = max(0, int((x - radius) / self.grid_size))
        max_grid_x = min(self.grid_w - 1, int((x + radius) / self.grid_size))
        min_grid_y = max(0, int((y - radius) / self.grid_size))
        max_grid_y = min(self.grid_h - 1, int((y + radius) / self.grid_size))
        
        for gy in range(min_grid_y, max_grid_y + 1):
            for gx in range(min_grid_x, max_grid_x + 1):
                if self.collision_map[gy, gx] == 0:  # obstacle
                    # Check if circle intersects this grid cell
                    cell_x = gx * self.grid_size
                    cell_y = gy * self.grid_size
                    # Find closest point in rectangle to circle center
                    closest_x = max(cell_x, min(x, cell_x + self.grid_size))
                    closest_y = max(cell_y, min(y, cell_y + self.grid_size))
                    # Check distance
                    dist = np.sqrt((x - closest_x)**2 + (y - closest_y)**2)
                    if dist < radius:
                        return False
        return True
        
    def initialize_map(self, map_name):
        """Initialize medkit spawns for a specific map"""
        # Try to load spawn data from map file first
        spawns_filepath = os.path.join("maps", f"{map_name}_medkit_spawns.json")
        
        spawn_data = None
        
        if os.path.exists(spawns_filepath):
            try:
                with open(spawns_filepath, 'r') as f:
                    spawn_data = json.load(f)
                print(f"[MEDKIT_SPAWNER] Loaded {len(spawn_data)} medkit spawn points from {spawns_filepath}")
            except Exception as e:
                print(f"[MEDKIT_SPAWNER] Error loading spawn file: {e}")
                spawn_data = None
        
        # Fallback to config if file doesn't exist or failed to load
        if spawn_data is None:
            if map_name not in self.spawn_points:
                print(f"[MEDKIT_SPAWNER] No spawn points defined for map: {map_name}")
                self.active_spawns = []
                self.spawn_cooldowns = []
                return
            spawn_data = self.spawn_points[map_name]
            print(f"[MEDKIT_SPAWNER] Using config spawn points for {map_name}")
        
        # Initialize active spawns: [x, y, is_active(1=yes, 0=no)]
        # Note: Validation is skipped (matching gun_spawner). Ensure spawn points are placed in valid walkable areas via config.
        self.active_spawns = []
        for x, y in spawn_data:
            # Do not spawn all medkits at once: each point rolls appearance chance.
            is_active = 1 if random.random() < self.SPAWN_APPEAR_CHANCE else 0
            self.active_spawns.append([x, y, is_active])

        # Active points start immediately; inactive points retry after interval.
        self.spawn_cooldowns = [0.0 if s[2] == 1 else self.SPAWN_INTERVAL for s in self.active_spawns]
        self.active_lifetimes = [0.0] * len(self.active_spawns)
        
        print(f"[MEDKIT_SPAWNER] Initialized {len(self.active_spawns)} medkit spawn points for {map_name}")
        
    def update(self, delta_time):
        """Update medkit spawn lifecycle (chance-based spawn + auto-despawn)."""
        for i in range(len(self.spawn_cooldowns)):
            is_active = self.active_spawns[i][2] == 1

            if is_active:
                self.active_lifetimes[i] += delta_time
                if self.active_lifetimes[i] >= self.ACTIVE_LIFETIME:
                    # Despawn if not picked up for too long.
                    self.active_spawns[i][2] = 0
                    self.active_lifetimes[i] = 0.0
                    self.spawn_cooldowns[i] = self.SPAWN_INTERVAL
                continue

            if self.spawn_cooldowns[i] > 0:
                self.spawn_cooldowns[i] -= delta_time

            if self.spawn_cooldowns[i] <= 0:
                if random.random() < self.SPAWN_APPEAR_CHANCE:
                    self.active_spawns[i][2] = 1
                    self.active_lifetimes[i] = 0.0
                    self.spawn_cooldowns[i] = 0.0
                else:
                    # Failed spawn roll; retry later.
                    self.spawn_cooldowns[i] = self.SPAWN_INTERVAL
                    
    def check_pickup(self, player_x, player_y):
        """Check if player is near any medkit spawn and return True if pickup possible"""
        for i, spawn in enumerate(self.active_spawns):
            x, y, is_active = spawn
            
            if is_active == 1:
                # Calculate distance to player
                dist = np.sqrt((player_x - x)**2 + (player_y - y)**2)
                
                if dist <= self.PICKUP_RADIUS:
                    # Player picked up the medkit
                    self.active_spawns[i][2] = 0  # Deactivate spawn
                    self.spawn_cooldowns[i] = self.SPAWN_INTERVAL  # Start cooldown
                    self.active_lifetimes[i] = 0.0
                    return True
                    
        return False  # No medkit picked up
        
    def get_active_spawns(self):
        """Return list of active medkit spawns for rendering"""
        # Returns: [(x, y), ...]
        active = []
        for spawn in self.active_spawns:
            x, y, is_active = spawn
            if is_active == 1:
                active.append((x, y))
        return active
        
    def get_spawn_data_for_client(self):
        """Get spawn data in format suitable for network transmission"""
        # Format: array of [x, y, is_active]
        return np.array(self.active_spawns, dtype=np.float32)
