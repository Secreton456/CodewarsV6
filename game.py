import os
import math
import pygame
import numpy as np
import time

from client import Network
from scripts.guns.guns import Gun, GUN_DATA


class PlayerClient:
    def __init__(self, W=800, H=600):
        pygame.init()

        # TEMP display (will resize after map info)
        self.screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
        pygame.display.set_caption("PyTanks")

        self.font = pygame.font.SysFont(None, 24)

        # ---- LOAD GUN DATA (NO SPRITES YET) ----
        self.guns = [Gun(**data) for data in GUN_DATA]

        self.get_player_name()
        self.join_server()

        # ---- RESIZE DISPLAY BASED ON MAP ----
        map_w = self.grid_w * self.grid_size
        map_h = self.grid_h * self.grid_size
        self.screen = pygame.display.set_mode((map_w, map_h), pygame.RESIZABLE)

        # ---- LOAD SPRITES AFTER DISPLAY ----
        self.load_sprites()

        self.running = True
        self.run_game()
        self.quit_game()

    # ------------------------------------
    # INITIALIZATION
    # ------------------------------------
    def get_player_name(self):
        self.name = ""
        while not (0 < len(self.name) < 20):
            self.name = input("Please enter your name: ")

    def join_server(self):
        print("Connecting to server...")
        self.server = Network()
        self.ID = self.server.connect(self.name)

        (
            self.collision_map,
            self.grid_w,
            self.grid_h,
            self.grid_size
        ) = self.server.get_collision_map()

        print("Connected as player", self.ID)

    def load_sprites(self):
        # Placeholder player body
        self.player_img = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.player_img, (100, 150, 255), (12, 12), 7)

        self.gun_sprites = {}
        for i, data in enumerate(GUN_DATA):
            path = os.path.join(
                "scripts", "guns", "gunsprites", data["sprite"]
            )
            self.gun_sprites[i] = pygame.image.load(path).convert_alpha()

    # ------------------------------------
    # DRAWING HELPERS
    # ------------------------------------
    def draw_player_with_gun(self, x, y, angle, gun_id, is_local):
        # body
        body_rect = self.player_img.get_rect(center=(x, y))
        self.screen.blit(self.player_img, body_rect)

        gun_img = self.gun_sprites.get(gun_id)
        gun_img= pygame.transform.smoothscale(gun_img,(20,10))
        if gun_img is None:
            return

        offset = 15
        gx = x + math.cos(angle) * offset
        gy = y + math.sin(angle) * offset

        rotated = pygame.transform.rotate(
            gun_img, -math.degrees(angle)
        )
        gun_rect = rotated.get_rect(center=(gx, gy))
        self.screen.blit(rotated, gun_rect)

        # local player indicator
        if is_local:
            pygame.draw.circle(self.screen, (0, 0, 255), (int(x), int(y)), 7, )

    # ------------------------------------
    # GAME LOOP
    # ------------------------------------
    def run_game(self):
        clock = pygame.time.Clock()
        guns = [Gun(**data) for data in GUN_DATA]
        while self.running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keyboard_input = np.zeros(8, dtype=bool)
            keys = pygame.key.get_pressed()

            keyboard_input[0] = keys[pygame.K_w]
            keyboard_input[1] = keys[pygame.K_a]
            keyboard_input[2] = keys[pygame.K_d]
            keyboard_input[3] = keys[pygame.K_UP]
            keyboard_input[4] = keys[pygame.K_DOWN]
            keyboard_input[5] = keys[pygame.K_LEFT]
            keyboard_input[6] = keys[pygame.K_RIGHT]
            keyboard_input[7] = keys[pygame.K_SPACE]

            if keys[pygame.K_ESCAPE]:
                self.running = False

            game_world = self.server.send(keyboard_input)
            self.render(game_world)

    # ------------------------------------
    # RENDER
    # ------------------------------------
    def render(self, game_world):
        guns = [Gun(**data) for data in GUN_DATA]
        self.screen.fill((0, 0, 0))

        # 1️⃣ MAP
        for gy in range(self.grid_h):
            for gx in range(self.grid_w):
                if self.collision_map[gy, gx] == 0:
                    pygame.draw.rect(
                        self.screen,
                        (70, 70, 70),
                        (
                            gx * self.grid_size,
                            gy * self.grid_size,
                            self.grid_size,
                            self.grid_size,
                        ),
                    )

        # 2️⃣ PLAYERS + GUNS
        for i in range(8):
            if game_world[i, 0] == 0:
                continue

            gun_id = int(game_world[i, 10])
            self.draw_player_with_gun(
                game_world[i, 1],
                game_world[i, 2],
                game_world[i, 3],
                gun_id,
                is_local=(i == self.ID),
            )

        # 3️⃣ BULLETS
        for i in range(8, 48):
            if game_world[i, 0] == 1:
                pygame.draw.circle(
                    self.screen,
                    (255, 255, 255),
                    (int(game_world[i, 1]), int(game_world[i, 2])),
                    2,
                )

        # 4️⃣ UI
        if game_world[self.ID, 0] == 1:
            fuel = game_world[self.ID, 6]
            health = game_world[self.ID, 7]
            score = int(game_world[self.ID, 8])

            pygame.draw.rect(self.screen, (0, 255, 255), (10, 10, fuel * 2, 15))
            pygame.draw.rect(self.screen, (255, 0, 0), (10, 30, health, 15))

            score_surf = self.font.render(f"Score: {score}", True, (255, 255, 255))
            self.screen.blit(score_surf, (self.screen.get_width() // 2 - 40, 10))

        pygame.display.flip()

    # ------------------------------------
    def quit_game(self):
        self.server.disconnect()
        pygame.quit()


if __name__ == "__main__":
    PlayerClient()
