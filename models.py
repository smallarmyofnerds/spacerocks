import pygame
from pygame import surface

from pygame.math import Vector2
from pygame.transform import rotozoom

from spacegame_utils import get_random_velocity, load_sound, load_sprite, wrap_position





UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Jukebox():
    def __init__(self):
        self.songs = ['Battle 1.wav', 'Battle 1.wav', 'Battle 1.wav']
        self.current_song = 0

    def play(self):
        pygame.mixer.music.load(f"assets/sounds/{self.songs[self.current_song]}")
        pygame.mixer.music.play(-1)
        
    def skip(self):
        self.current_song = (self.current_song + 1) % len(self.songs)
        self.play()
        

class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.15
    BULLET_SPEED = 4
    SHIELD = 2

    def __init__(self, position, sprite, moving_sprite, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        self.direction = Vector2(UP)
        self.sprite = pygame.transform.scale(sprite, (50, 70))
        self.moving_sprite = pygame.transform.scale(moving_sprite, (50, 70))
        self.is_moving = False
        self.engine = load_sound("engine")
        super().__init__(position, self.sprite, Vector2(0))
    
    def rotate(self, clockwise = True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)
    
    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION
    
    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.create_bullet_callback(bullet)
        self.create_bullet_callback(bullet)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

    def set_moving(self, is_moving):
        self.is_moving = is_moving
        if self.is_moving:
            self.engine.play()
        else:
            self.engine.stop()
    
    def explode(self, surface):
        self.ship_explosion = load_sprite("shipexplosion")
        self.re_ship_explosion = pygame.transform.scale(self.ship_explosion, (80, 80))
        surface.blit(self.re_ship_explosion, self.position)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        if self.is_moving:
            rotated_surface = rotozoom(self.moving_sprite, angle, 1.0)
        else:
            rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)


class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size = 3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {
            3: 1,
            2: 0.5,
            1: 0.25,
        }
        asteroid = load_sprite("asteroid")
        re_asteroid = pygame.transform.scale(asteroid, (130, 130))
        scale = size_to_scale[size]
        sprite = rotozoom(re_asteroid, 0, scale)
        super().__init__(position, sprite, get_random_velocity(1, 3))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(self.position, self.create_asteroid_callback, self.size - 1)
                self.create_asteroid_callback(asteroid)

class Bullet(GameObject):
    def __init__(self, position, velocity):
        bullet = load_sprite("bullet")
        re_bullet = pygame.transform.scale(bullet, (40, 40))
        super().__init__(position, re_bullet, velocity)
    
    def move(self, surface):
        self.position = self.position+ self.velocity