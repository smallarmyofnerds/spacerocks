import random
import time
from pygame import Color
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound

def load_sprite(name, with_alpha = True):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)


    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height())
    )


def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)


def load_sound(name):
    path = f"assets/sounds/{name}.wav"
    return Sound(path)


def print_text(surface, text, font, color = Color("tomato")):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2
    
    surface.blit(text_surface, rect)

def print_timer(surface, start_time, end_time, font, color = Color("tomato")):
    if end_time is None:
        score = int((time.time() - start_time) * 1000)
    else:
        score = int((end_time - start_time) * 1000)
    text_surface = font.render(str(score), True, color)
    rect = text_surface.get_rect()
    rect.center = 400, 100

    surface.blit(text_surface, rect)