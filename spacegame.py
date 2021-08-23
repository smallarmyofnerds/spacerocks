from os import wait
import pygame
from pygame import Rect, surface
import time
from pygame import draw

from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP

from models import Asteroid, Jukebox, Spaceship
from spacegame_utils import get_random_position, load_sound, load_sprite, print_text, print_timer

class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250
    def __init__(self, size = (1800 , 1000)):
        self._init_pygame()
        self.size = size
        self.screen = pygame.display.set_mode(size)
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.timer_font = pygame.font.Font(None, 30)
        self.timer = pygame.time.get_ticks()
        self.jukebox = Jukebox()
        
        
        self.new_game()
    
    def new_game(self):
        self.message = ""
        self.asteroids = []
        self.bullets = []
        self.start_game_time = time.time()
        self.end_game_time = None
        self.spaceship = Spaceship((400, 300), load_sprite("spaceship"), load_sprite("spaceshipmoving"), self.bullets.append)
        self.new_rocks()

    def new_rocks(self):
        for _ in range(12):
            while True:
                position = get_random_position(self.screen)
                if (position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))


    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects

    def main_loop(self):
        self.jukebox.play()
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()

            elif (self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.spaceship.shoot()

            if self.message:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print("pressed mouse button")
                    print(pos)
                    print(self.replay_rect)
                    if self.replay_rect.collidepoint(pos):
                        self.new_game()


        is_key_pressed = pygame.key.get_pressed()
        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
                self.spaceship.set_moving(True)
            else:
                self.spaceship.set_moving(False)

   


    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
        
        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship) and self.spaceship.SHIELD == 0:
                    self.spaceship.explode(self.screen)
                    self.spaceship = None
                    self.asteroids.remove(asteroid)
                    asteroid.split()
                    ship_explosion = load_sound("shipexplosion")
                    ship_explosion.play()
                    self.message = "You Lost!"
                    self.end_game_time = time.time()
                    break
                elif asteroid.collides_with(self.spaceship) and self.spaceship.SHIELD > 0:
                    self.spaceship.SHIELD -= 1
                    self.asteroids.remove(asteroid)
                    asteroid.split()
                    ship_explosion = load_sound("shipexplosion")
                    ship_explosion.play()

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    rock_explosion = load_sound("rockexplosion")
                    rock_explosion.play()
                    self.spaceship.SHIELD += 1
                    break
        
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.asteroids and self.spaceship:
            # self.message = "You Won!"
            self.new_rocks()
        

    def _draw(self):
        re_background = pygame.transform.scale(self.background, self.size)
        self.screen.blit(re_background, (0, 0))
        

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        print_timer(self.screen, self.start_game_time, self.end_game_time, self.timer_font)
        if self.message:
            print_text(self.screen, self.message, self.font)
            replaybtn = load_sprite("replaybtn")
            re_replaybtn = pygame.transform.scale(replaybtn, (100, 100))
            self.re_replaybtn = re_replaybtn
            pygame.Surface.blit(self.screen, re_replaybtn, (850, 700))
            self.replay_rect = Rect(850, 700, 100, 100)
            # draw button
        pygame.display.flip()
        self.clock.tick(60)
        


