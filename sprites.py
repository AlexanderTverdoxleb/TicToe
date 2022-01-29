import pygame
from main import load_image


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class GameObject(Sprite):
    game_obj_width = 100
    game_obj_height = 100

    def __init__(self, pos_x, pos_y, sprite_group, game_obj_type):
        super().__init__(sprite_group)
        images = {
            'o': load_image('textures/circle.png'),
            'x': load_image('textures/crest.png')
        }
        self.image = images[game_obj_type]
        self.rect = self.image.get_rect().move(
            self.game_obj_width + pos_x,
            self.game_obj_height + pos_y
        )
