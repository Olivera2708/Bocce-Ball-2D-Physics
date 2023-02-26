import numpy as np
import pygame
import global_val
import math
from nans_lib_2 import rk4N

class Ball():
    def __init__(self, player, radius):
        self.position = np.zeros(2, dtype=float)
        self.velocity = np.zeros(2, dtype=float)
        self.player = player
        self.angle = np.array([0, 0])
        self.radius = radius
        self.rk_x = None
        self.rk_y = None
        self.num = 0

    def apply_force(self, vel):
        #podesimo brzinu lopte na osnovu prosledjene
        self.velocity = vel
        dv = lambda *args: -1/150 * args[2]
        vx = np.array([self.position[0], self.velocity[0]])
        self.rk_x = rk4N(0, 100, 1, vx, dv)

        vy = np.array([self.position[1], self.velocity[1]])
        self.rk_y = rk4N(0, 100, 1, vy, dv)

        self.num = 0
        self.update()
    
    def set_velocity(self, new_vel):
        self.velocity = np.array(new_vel, dtype=float)

    def move_to(self, new_pos):
        self.position = np.array(new_pos, dtype=float)

    def update(self):
        if (self.num == 100):
            self.apply_force(self.velocity)

        self.position = np.array([self.rk_x[0][self.num], self.rk_y[0][self.num]])
        self.velocity = np.array([self.rk_x[1][-1][self.num], self.rk_y[1][-1][self.num]])
        self.num += 1

        if np.hypot(*self.velocity) < 0.08: #ako je brzina mala kazemo da je 0
            self.velocity = np.zeros(2)


class BallSprite(pygame.sprite.Sprite):
    def __init__(self, igrac, radius):
        if (igrac == 1):
            self.color = global_val.red_color
        elif (igrac == 2):
            self.color = global_val.blue_color
        else:
            self.color = global_val.white_color

        self.ball = Ball(igrac, radius)
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((self.ball.radius * 2, self.ball.radius * 2))
        self.image.set_alpha(255)
        #lines
        pygame.draw.circle(self.image, self.color, (self.ball.radius, self.ball.radius), self.ball.radius)

        self.rect = self.image.get_rect()
        self.rect.center = self.ball.position

    def update(self, *args):
        if np.hypot(*self.ball.velocity) != 0:
            self.ball.update()
        self.rect.center = self.ball.position.tolist()

    def move_to(self, pos):
        self.ball.move_to(pos)
        self.rect.center = self.ball.position.tolist()