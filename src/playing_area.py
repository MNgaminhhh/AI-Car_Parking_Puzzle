import pygame
import random

class PlayingArea():

    def __init__(self, game):
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.tile_size = self.settings.tile_size
        self.map_width = self.settings.map_width
        self.map_height = self.settings.map_height
        self.image = pygame.Surface((self.tile_size * self.map_width, self.tile_size * self.map_height))
        self.rect = self.image.get_rect()
        self.map = game.map
        top_left = (430, 93)
        bottom_right = (1270, 684)
        center_x = (top_left[0] + bottom_right[0]) // 2
        center_y = (top_left[1] + bottom_right[1]) // 2
        self.rect.center = (center_x, center_y)
        self.tile_rotations = [[random.choice([0, 90, 180]) for _ in range(self.map_width)] for _ in range(self.map_height)]

    def draw(self):
        self.screen.blit(self.image, self.rect)
        for i in range(self.map_height):
            for j in range(self.map_width):
                x = j * self.tile_size
                y = i * self.tile_size
                if self.map[i][j] == -1:
                    tile_image = pygame.image.load('assets/block.png')
                else:
                    tile_image = pygame.image.load('assets/map.png')

                tile_image = pygame.transform.scale(tile_image, (self.tile_size, self.tile_size))
                # Lấy góc xoay đã được lưu trữ cho tile này
                angle = self.tile_rotations[i][j]
                tile_image = pygame.transform.rotate(tile_image, angle)
                tile_rect = tile_image.get_rect(center=(x + self.tile_size // 2, y + self.tile_size // 2))
                self.image.blit(tile_image, tile_rect.topleft)
    