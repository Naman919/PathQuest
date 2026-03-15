import pygame
from config import WHITE, FONT

class Button:
    def __init__(self, x, y, width, height, text, color=(70,70,70)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text, self.color = text, color
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        txt_surf = FONT.render(self.text, True, WHITE)
        win.blit(txt_surf, txt_surf.get_rect(center=self.rect.center))
    def is_clicked(self, pos): return self.rect.collidepoint(pos)
