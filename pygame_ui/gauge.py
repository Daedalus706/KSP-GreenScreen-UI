import pygame
import math
from pygame_ui.util import *


class Gauge:
    if not pygame.font.get_init():
        pygame.font.init()
    font = pygame.font.SysFont("Trebuchet MS", 28, False)

    def __init__(self, pos:tuple, value_range:tuple, name:str, unit:str) -> None:
        """
        :param pos: Position of the gauge on the darget surface when calling the draw() function
        :param value_range: A tupel (min, max) that defines tha range in which the gauge expects the values
        :param name: The name that will be displayed below the gauge, For example "Throttle" or "Fuel"
        :param unit: The unit that will be displayed behind the value. For example "m/s" or "%" 
        """
        # Set values
        self._pos = pos
        self._range = value_range
        self._name = name
        self._unit = unit

        # Init surfaces
        self._surf = pygame.Surface((200, 200), pygame.SRCALPHA)
        self._surf.fill((0, 0, 0, 0))

        self._background = pygame.Surface((200, 200), pygame.SRCALPHA)
        self._background.fill((0, 0, 0, 0))

        # Magic number party
        pygame.draw.circle(self._background, (255, 255, 255, 255), (100, 100), 95, 10)
        p1 = rotate_vector(0, -100, -120/180*math.pi)
        p2 = rotate_vector(0, -100, 120/180*math.pi)
        pygame.draw.polygon(self._background, (0, 0, 0, 0), ((100, 100), (p1[0]+100, p1[1]+100), (0, 200), (200, 200), (p2[0]+100, p2[1]+100)))
        self._font_surf = Gauge.font.render(name, False, (255, 255, 255, 255))
        self._background.blit(self._font_surf, (100-self._font_surf.get_width()//2, 145))
        v1 = (-p1[0]/norm(p1[0], p1[1]), -p1[1]/norm(p1[0], p1[1]))
        v2 = (-v1[0], v1[1])
        pygame.draw.polygon(self._background, (255, 255, 255, 255), ((100-(v1[0]*90-v1[1]*3), 110-(v1[1]*90+v1[0]*3)), (100-(v1[0]*90+v1[1]*3), 110-(v1[1]*90-v1[0]*3)), (100-(v1[0]*55+v1[1]*3), 109-(v1[1]*55-v1[0]*3)), (100-(v1[0]*55-v1[1]*3), 110-(v1[1]*55+v1[0]*3))))
        pygame.draw.polygon(self._background, (255, 255, 255, 255), ((100-(v2[0]*90-v2[1]*3), 110-(v2[1]*90+v2[0]*3)), (100-(v2[0]*90+v2[1]*3), 110-(v2[1]*90-v2[0]*3)), (100-(v2[0]*55+v2[1]*3), 110-(v2[1]*55-v2[0]*3)), (100-(v2[0]*55-v2[1]*3), 109-(v2[1]*55+v2[0]*3))))

        self._scale_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
        self._scale_surf.fill((0, 0, 0, 0))
        pygame.draw.circle(self._scale_surf, (255, 255, 255, 255), (100, 100), 80, 20)
        pygame.draw.polygon(self._scale_surf, (0, 0, 0, 0), ((100, 100), (p1[0]+100, p1[1]+100), (0, 200), (200, 200), (p2[0]+100, p2[1]+100)))

        self.update_surf(self._range[0])

    def draw(self, surf:pygame.Surface):
        """
        Draw the gauge to the surface
        """
        surf.blit(self._surf, self._pos)

    def update_surf(self, value:float):
        """
        Set the new value of the gauge. Values above or below the gauge's range will be displayed as a number but clipped for the display arc.
        """
        # Clear surface
        self._surf.fill((0, 0, 0, 0))
        self._surf.blit(self._scale_surf, (0, 0))

        # Render text
        decimal = len(f"{int(self._range[1])}")
        text_surf = Gauge.font.render(f"{value:{decimal}.0f}{self._unit}", False, (255, 255, 255, 255))

        # Clip values
        if value < self._range[0]:
            value = self._range[0]
        elif value > self._range[1]:
            value = self._range[1]

        # Draw the arc 
        amount = (value-self._range[0])/(self._range[1]-self._range[0])
        angle = (1-amount) * 240
        p = rotate_vector(0, -100, 120/180*math.pi)
        p = rotate_vector(p[0], p[1], -angle/180*math.pi)
        if 0 <= (amount) < .33:
            pygame.draw.polygon(self._surf, (0, 0, 0, 0), ((100, 100), (p[0]+100, p[1]+100), (0, 0), (200, 0), (200, 200), (100, 200)))
        elif .33 <= (amount) < .80:
            pygame.draw.polygon(self._surf, (0, 0, 0, 0), ((100, 100), (p[0]+100, p[1]+100), (200, 0), (200, 200), (100, 200)))
        else:
            pygame.draw.polygon(self._surf, (0, 0, 0, 0), ((100, 100), (p[0]+100, p[1]+100), (200, 200), (100, 200)))

        self._surf.blit(self._background, (0, 0))
        self._surf.blit(text_surf, (100-text_surf.get_width()/2, 100-text_surf.get_height()//2))
