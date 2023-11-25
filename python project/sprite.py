import pygame
from customizze import *

class Tile:
    def __init__(self, x, y, letter = "", colour = None):
        self.x, self.y = x, y
        self.letter = letter
        self.colour = colour
        self.width, self.height = TILESIZE, TILESIZE
        self.font_size = int(60*(TILESIZE/100))
        self.create_font()
  
    def create_font(self):
        font = pygame.font. SysFont("Consolas", self.font_size)
        self.render_lettter = font.render(self.letter, True, white)
        self.font_width, self.font_height = font.size(self.letter)

    def draw(self, screen):
        if self.colour is None:
            pygame.draw.rect(screen, white, (self.x, self.y, self.width, self.height), 2)
        else:
            pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        if self.letter != "":
            self.font_x = self.x + (self.width/2) - (self.font_width/2)
            self.font_y = self.y + (self.height/2) - (self.font_height/2)
            letter = pygame.transform.scale(self.render_lettter, (self.font_width, self.font_height))
            screen.blit(letter, (self.font_x, self.font_y))

class UIElement:
    def __init__(self, x, y, text, colour, font_size = 20):
        self.x, self.y = x, y
        self.text = text
        self.colour = colour
        self.font_size = font_size
        self.alpha = 0
        self.create_font()

    def create_font(self):
        font = pygame.font.SysFont("Arcadia", self.font_size)
        self.original_surface = font.render(self.text, True, self.colour)
        self.text_surface = self.original_surface.copy()
        # this surface is used to adjust the alpha of the text_surface
        self.alpha_surface = pygame.Surface(self.text_surface.get_size(), pygame.SRCALPHA)

    def draw(self, screen):
        self.text_surface = self.original_surface.copy()
        self.alpha_surface.fill((255, 255, 255, self.alpha))
        self.text_surface.blit(self.alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(self.text_surface, (self.x, self.y))

    def fade_out(self):
        self.alpha = max(self.alpha - 10, 0)
        self.text_surface = self.original_surface.copy()
        self.alpha_surface.fill((255, 255, 255, self.alpha))
        self.text_surface.blit(self.alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def fade_in(self):
        self.alpha = min(self.alpha + 10, 255)
        self.text_surface = self.original_surface.copy()
        self.alpha_surface.fill((255, 255, 255, self.alpha))
        self.text_surface.blit(self.alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)