import global_val
import pygame

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(global_val.ground_size)
        pygame.draw.rect(self.image, global_val.ground_color, pygame.Rect(0, 0, 340, 700))
        pygame.draw.rect(self.image, global_val.side_color, pygame.Rect(0, 0, 20, 700))
        pygame.draw.rect(self.image, global_val.side_color, pygame.Rect(320, 0, 20, 700))
        pygame.draw.rect(self.image, global_val.side_color, pygame.Rect(0, 0, 340, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = (30, 90)

class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(global_val.score_size)

        self.draw_all(0, 0)

    def draw_all(self, p1, p2):
        self.image.fill(global_val.background_color)
        #lines
        pygame.draw.rect(self.image, (66, 60, 40), pygame.Rect(5, 70, 390, 4))
        pygame.draw.rect(self.image, (66, 60, 40), pygame.Rect(196, 35, 4, 35))
        pygame.draw.rect(self.image, (66, 60, 40), pygame.Rect(110, 35, 180, 4))
        pygame.draw.rect(self.image, (66, 60, 40), pygame.Rect(110, 5, 4, 30))
        pygame.draw.rect(self.image, (66, 60, 40), pygame.Rect(286, 5, 4, 30))

        #text
        font = pygame.font.SysFont('consolas',  24, bold=True)
        text = font.render("BOĆANJE", 1, (66, 60, 40))
        textR = text.get_rect()
        textR.center = (200, 20)
        self.image.blit(text, textR)

        #points
        font = pygame.font.SysFont('consolas', 44, bold=True)
        text_p1 = font.render(str(p1), 1, (66, 60, 40))
        text_p2 = font.render(str(p2), 1, (66, 60, 40))
        textR_p1 = text_p1.get_rect()
        textR_p2 = text_p2.get_rect()
        textR_p1.center = (55, 40)
        textR_p2.center = (345, 40)
        self.image.blit(text_p1, textR_p1)
        self.image.blit(text_p2, textR_p2)

        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
    
