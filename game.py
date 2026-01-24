import pygame
import sys
from config import DEBUG


class Game:
    def __init__(self, all_team_troops, all_team_names):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Mini Militia Bot Arena")

        self.screen = pygame.display.set_mode((1200, 700))
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.all_team_troops = all_team_troops
        self.all_team_names = all_team_names

        self.game_counter = 0
        self.winner = None

        if DEBUG:
            for i, name in enumerate(self.all_team_names):
                print(f"[Game] Loaded Team {i+1}: {name}")

        # TODO: initialize players, weapons, map, physics, etc.
        self._init_players()

    def _init_players(self):
        self.players = []

        for team_idx, troops in enumerate(self.all_team_troops):
            for troop in troops:
                # Placeholder player objects
                self.players.append({
                    "team": team_idx,
                    "troop": troop,
                    "x": 100 + 100 * team_idx,
                    "y": 100
                })

        if DEBUG:
            print(f"[Game] Initialized {len(self.players)} players")

    def update(self):
        # TODO: physics, AI calls, combat resolution
        pass

    def draw(self):
        self.screen.fill((25, 25, 25))

        # Placeholder rendering
        for p in self.players:
            color = (200, 50 + 40*p["team"], 50)
            pygame.draw.circle(self.screen, color, (p["x"], p["y"]), 10)

        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update()
            self.draw()

            self.clock.tick(self.fps)
            self.game_counter += 1
