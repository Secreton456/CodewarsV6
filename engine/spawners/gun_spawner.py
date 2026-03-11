import numpy as np
import time
import json
import os
import sys
import random

# Add project root to path so root-level modules are importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from engine.weapons.weapons import get_weapon
from config import (GUN_SPAWN_INTERVAL, GUN_PICKUP_RADIUS, 
                    GUN_SPAWN_POINTS, DEFAULT_STARTING_WEAPON, DEFAULT_SECONDARY_WEAPON,
                    GUN_SPAWN_APPEAR_CHANCE, GUN_SPAWN_ACTIVE_LIFETIME)

class GunSpawner:
    """Manages gun spawning at predefined locations on the map"""
    
    def __init__(self):
        self.spawn_points = GUN_SPAWN_POINTS  # Load from config
        self.active_spawns = []  # List of currently spawned guns
        self.spawn_cooldowns = []  # Cooldown timers for each spawn point
        self.active_lifetimes = []  # Active time trackers for despawn logic
        self.SPAWN_INTERVAL = GUN_SPAWN_INTERVAL
        self.PICKUP_RADIUS = GUN_PICKUP_RADIUS
        self.SPAWN_APPEAR_CHANCE = GUN_SPAWN_APPEAR_CHANCE
        self.ACTIVE_LIFETIME = GUN_SPAWN_ACTIVE_LIFETIME
        
    def initialize_map(self, map_name):
        """Initialize spawns for a specific map (load from file or fallback to config)"""
        # Try to load spawn data from map file first
        spawns_filepath = os.path.join("maps", f"{map_name}_spawns.json")
        
        spawn_data = None
        
        if os.path.exists(spawns_filepath):
            try:
                with open(spawns_filepath, 'r') as f:
                    spawn_data = json.load(f)
                print(f"[GUN_SPAWNER] Loaded {len(spawn_data)} spawn points from {spawns_filepath}")
            except Exception as e:
                print(f"[GUN_SPAWNER] Error loading spawn file: {e}")
                spawn_data = None
        
        # Fallback to config if file doesn't exist or failed to load
        if spawn_data is None:
            if map_name not in self.spawn_points:
                print(f"[GUN_SPAWNER] No spawn points defined for map: {map_name}")
                self.active_spawns = []
                self.spawn_cooldowns = []
                return
            spawn_data = self.spawn_points[map_name]
            print(f"[GUN_SPAWNER] Using config spawn points for {map_name}")
        
        # Initialize active spawns: [x, y, weapon_id, is_active(1=yes, 0=no)]
        self.active_spawns = []
        for x, y, weapon_id in spawn_data:
            # Do not spawn all guns at once: each point rolls appearance chance.
            is_active = 1 if random.random() < self.SPAWN_APPEAR_CHANCE else 0
            self.active_spawns.append([x, y, weapon_id, is_active])

        # Active points start immediately; inactive points retry after interval.
        self.spawn_cooldowns = [0.0 if s[3] == 1 else self.SPAWN_INTERVAL for s in self.active_spawns]
        self.active_lifetimes = [0.0] * len(self.active_spawns)
        
        print(f"[GUN_SPAWNER] Initialized {len(self.active_spawns)} spawn points for {map_name}")
        
    def update(self, delta_time):
        """Update gun spawn lifecycle (chance-based spawn + auto-despawn)."""
        for i in range(len(self.spawn_cooldowns)):
            is_active = self.active_spawns[i][3] == 1

            if is_active:
                self.active_lifetimes[i] += delta_time
                if self.active_lifetimes[i] >= self.ACTIVE_LIFETIME:
                    # Despawn if not picked up for too long.
                    self.active_spawns[i][3] = 0
                    self.active_lifetimes[i] = 0.0
                    self.spawn_cooldowns[i] = self.SPAWN_INTERVAL
                continue

            if self.spawn_cooldowns[i] > 0:
                self.spawn_cooldowns[i] -= delta_time

            if self.spawn_cooldowns[i] <= 0:
                if random.random() < self.SPAWN_APPEAR_CHANCE:
                    self.active_spawns[i][3] = 1
                    self.active_lifetimes[i] = 0.0
                    self.spawn_cooldowns[i] = 0.0
                else:
                    # Failed spawn roll; retry later.
                    self.spawn_cooldowns[i] = self.SPAWN_INTERVAL
                    
    def get_nearby_gun(self, player_x, player_y):
        """Return index of nearby gun spawn if player is close"""
        for i, spawn in enumerate(self.active_spawns):
            x, y, weapon_id, is_active = spawn

            if is_active == 1:
                dist = np.sqrt((player_x - x)**2 + (player_y - y)**2)

                if dist <= self.PICKUP_RADIUS:
                    return i   # return spawn index

        return None
    
    def pickup_gun(self, spawn_index):
        """Activate pickup for a spawn"""
        x, y, weapon_id, is_active = self.active_spawns[spawn_index]

        if is_active == 1:
            self.active_spawns[spawn_index][3] = 0
            self.spawn_cooldowns[spawn_index] = self.SPAWN_INTERVAL
            self.active_lifetimes[spawn_index] = 0.0
            return weapon_id

        return None
        
    def get_active_spawns(self):
        """Return list of active gun spawns for rendering"""
        # Returns: [(x, y, weapon_id), ...]
        active = []
        for spawn in self.active_spawns:
            x, y, weapon_id, is_active = spawn
            if is_active == 1:
                active.append((x, y, weapon_id))
        return active
        
    def get_spawn_data_for_client(self):
        """Get spawn data in format suitable for network transmission"""
        # Format: array of [x, y, weapon_id, is_active]
        return np.array(self.active_spawns, dtype=np.float32)


class PlayerInventory:
    """Manages a player's gun inventory (2 guns max)"""
    
    def __init__(self, starting_weapon_id=None, secondary_weapon_id=None):
        if starting_weapon_id is None:
            starting_weapon_id = DEFAULT_STARTING_WEAPON
        if secondary_weapon_id is None:
            secondary_weapon_id = DEFAULT_SECONDARY_WEAPON
        self.guns = [None, None]  # Two gun slots
        self.current_slot = 0  # Currently active gun (0 or 1)
        
        # Start with default loadout
        self.guns[0] = get_weapon(starting_weapon_id)
        if secondary_weapon_id is not None:
            self.guns[1] = get_weapon(secondary_weapon_id)
        
    def pickup_gun(self, weapon_id):
        """Pickup a new gun by replacing the currently active gun."""
        new_gun = get_weapon(weapon_id)

        current_gun = self.guns[self.current_slot]
        dropped_id = current_gun.gun_id if current_gun is not None else None
        self.guns[self.current_slot] = new_gun
        return dropped_id
            
    def switch_gun(self):
        """Switch to the other gun slot"""
        if self.guns[1] is not None:
            self.current_slot = 1 - self.current_slot  # Toggle between 0 and 1
            
    def get_current_gun(self):
        """Get the currently active gun"""
        return self.guns[self.current_slot]
        
    def has_second_gun(self):
        """Check if player has a second gun"""
        return self.guns[1] is not None
        
    def get_gun_ids(self):
        """Get weapon IDs of both guns for syncing"""
        ids = [-1, -1]  # -1 means no gun
        if self.guns[0] is not None:
            ids[0] = self.guns[0].gun_id
        if self.guns[1] is not None:
            ids[1] = self.guns[1].gun_id
        return ids
        
    def get_ammo_data(self):
        """Get ammo data for both guns"""
        # Returns: [(current_ammo, total_ammo), (current_ammo, total_ammo)]
        ammo_data = [(0, 0), (0, 0)]
        for i in range(2):
            if self.guns[i] is not None:
                ammo_data[i] = (self.guns[i].current_ammo, self.guns[i].total_ammo)
        return ammo_data
