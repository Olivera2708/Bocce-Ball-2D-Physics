import pygame
import ball
import numpy as np
import sprites
import global_val

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(global_val.screen_size)
        pygame.display.set_caption("Boćanje")
        self.background = pygame.Surface(self.surface.get_size())
        self.background.fill(global_val.background_color)
        self.surface.blit(self.background, (0, 0))
        self.fps = pygame.time.Clock()
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONUP])
        self.points1 = 0
        self.points2 = 0
        self.mouse = None

    def fps(self):
        return self.fps_clock.get_fps()

    def mark_one_frame(self):
        self.fps.tick(60)

    def create_small_ball(self):
        self.small_ball = ball.BallSprite(0, global_val.small_ball_radius)
        self.small_ball.move_to(global_val.ball_center)
        self.all_sprites.add(self.small_ball)
        self.current_ball = self.small_ball
        self.used_balls.add(self.small_ball)

    def start_state(self):
        self.player = 1
        self.balls = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.OrderedUpdates()
        self.used_balls = pygame.sprite.Group()

    def draw_line(self):
        pygame.draw.line(self.surface, (19, 64, 32), global_val.ball_center, self.mouse, 3)
        # pygame.display.update()

    def reset_state(self):
        self.used_balls.empty()
        p1 = 0
        p2 = 0
        for ball in self.balls:
            if ball.ball.player == 1:
                ball.move_to((120 + p1*30, 55))
                p1 += 1
            else:
                ball.move_to((276 - p2*30, 55))
                p2 += 1
        self.small_ball.move_to(global_val.ball_center)
        self.current_ball = self.small_ball
        self.used_balls.add(self.small_ball)

    def add_points(self):
        my_dict = {}
        for ball in self.balls:
            my_dict[ball] = np.hypot(*(np.asarray(ball.ball.position) - np.asarray(self.small_ball.ball.position)))

        my_dict = dict(sorted(my_dict.items(), key=lambda  x: x[1]))
        winner = list(my_dict.keys())[0].ball.player
        winner_points = 0
        for key in my_dict.keys():
            if key.ball.player == winner:
                winner_points += 1
            else:
                break
        if (winner == 1):
            self.points1 += winner_points
        else:
            self.points2 += winner_points

        self.player = winner
        self.score.draw_all(self.points1, self.points2)

    def generate_score(self):
        self.score = sprites.Score()
        self.all_sprites.add(self.score)

    def generate_ground(self):
        self.ground = sprites.Ground()
        self.all_sprites.add(self.ground)

    def create_balls(self):
        self.create_small_ball()
        for i in range(3):
            ball_sprite = ball.BallSprite(1, global_val.ball_radius)
            ball_sprite.move_to((120 + i*30, 55))
            self.all_sprites.add(ball_sprite)
            self.balls.add(ball_sprite)
        for i in range(3):
            ball_sprite = ball.BallSprite(2, global_val.ball_radius)
            ball_sprite.move_to((276 - i*30, 55))
            self.all_sprites.add(ball_sprite)
            self.balls.add(ball_sprite)

    def start(self):
        self.start_state()
        self.generate_ground()
        self.generate_score()
        self.create_balls()

    def next_turn(self): #sve ne pomeraju
        for ball in self.used_balls:
            if (not np.array_equal(ball.ball.velocity, [0, 0])):
                return False
        return True

    def draw(self):
        self.all_sprites.clear(self.surface, self.background)
        self.all_sprites.draw(self.surface)
        if self.mouse != None:
            self.draw_line()
        self.all_sprites.update(self)
        pygame.display.flip()
        self.mark_one_frame()

    def correct_pos(self):
        mouse = pygame.mouse.get_pos()
        if (mouse[1] > 710 and mouse[1] < 790 and mouse[0] > 120 and mouse[0] < 280):
            return True, mouse
        return False, None

    def ball_move(self, mouse):
        mouse_dist = np.hypot(*(np.asarray(mouse) - np.asarray(global_val.ball_center)))
        self.current_ball.ball.angle = np.array([(200 - mouse[0])/mouse_dist, (710 - mouse[1])/mouse_dist])
        new_vel = 2 * mouse_dist * np.array([(200 - mouse[0])/mouse_dist, (710 - mouse[1])/mouse_dist])
        self.current_ball.ball.apply_force(new_vel/15)

    def detect_collision_line_circle(self):
        #0.99 je koeficijent restitucije
        for ball in self.used_balls:
            if (ball.ball.position[0] >= 345-ball.ball.radius/2):
                self.collide_line_circle(ball, np.array([-1, 0]))
            if (ball.ball.position[0] <= 55+ball.ball.radius/2):
                self.collide_line_circle(ball, np.array([1, 0]))
            if (ball.ball.position[1] <= 115+ball.ball.radius/2):
                self.collide_line_circle(ball, np.array([0, 1]))

    def detect_collision_circle_circle(self):
        possible_collisions = self.sweep_prune()
        for collision in possible_collisions:
            for i in range(len(collision)):
                for j in range(i+1, len(collision)):
                    dist = np.hypot(*(np.asarray(collision[i].ball.position) - np.asarray(collision[j].ball.position)))
                    if (dist <= collision[i].ball.radius + collision[j].ball.radius):
                        self.collide_balls(collision[i], collision[j], dist)

    def sweep_prune(self):
        sort = sorted(self.used_balls, key=lambda x: x.ball.position[1])
        possible_collisions = []
        active = [sort[0]]
        active_interval = [sort[0].ball.position[1]-sort[0].ball.radius, sort[0].ball.position[1]+sort[0].ball.radius]
        for i in sort[1:]:
            if ((active_interval[0] <= i.ball.position[1]-i.ball.radius <= active_interval[1]) or
            (active_interval[0] <= i.ball.position[1]+i.ball.radius <= active_interval[1])):
                active.append(i)
                active_interval[1] = i.ball.position[1]+i.ball.radius   
            else:
                if (len(active) != 1):
                    possible_collisions.append(active)
                active = [i]
                active_interval = [i.ball.position[1]-i.ball.radius, i.ball.position[1]+i.ball.radius]
        if (len(active) != 1):
            possible_collisions.append(active)
        return possible_collisions

    def collide_line_circle(self, ball, normal):
        dot_ball_norm = np.dot(ball.ball.velocity, normal)
        ball.ball.apply_force(ball.ball.velocity - 2 * dot_ball_norm * normal)

    def collide_balls(self, ball, ball1, dist):
        normalized = (ball.ball.position - ball1.ball.position)/dist
        tangent = np.array([-normalized[1], normalized[0]])

        dot_ball_norm = np.dot(ball.ball.velocity, normalized)
        dot_ball1_norm = np.dot(ball1.ball.velocity, normalized)

        dot_ball_tan = np.dot(ball.ball.velocity, tangent)
        dot_ball1_tan = np.dot(ball1.ball.velocity, tangent)

        #momentum - posto su mase iste onda mi ne treba prvi deo jednacine
        ball_m = dot_ball1_norm
        ball1_m = dot_ball_norm

        ball.ball.apply_force(dot_ball_tan * tangent + normalized*ball_m)
        ball1.ball.apply_force(dot_ball1_tan * tangent + normalized*ball1_m)

    def detect_collision(self):
        self.sweep_prune()
        self.detect_collision_line_circle()
        self.detect_collision_circle_circle()

    def next_ball(self):
        if (self.small_ball != self.current_ball or (self.small_ball == self.current_ball and not (np.array_equal(self.small_ball.ball.position, np.array(global_val.ball_center))))):
            for ball in self.balls:
                if ball.ball.player == self.player and ball.ball.position[1] == 55:
                    ball.move_to(global_val.ball_center)
                    self.used_balls.add(ball)
                    self.current_ball = ball
                    break
            if self.player == 1:
                self.player = 2
            else:
                self.player = 1

    def end_round(self):
        return len(self.used_balls) == 7

    def is_closed(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False