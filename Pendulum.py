import pygame
import pygame.gfxdraw
from math import sin, cos, pi


class Pendulum:
    def __init__(self, mass, theta, radius, color, length, offset):
        self.mass = mass
        self.theta = theta
        self.radius = radius
        self.color = color
        self.length = length
        self.offset = offset
        self.a = 0
        self.v = 0
        self.lines = []

        self.position = pygame.Vector2(
            self.length * sin(self.theta) + self.offset.x,
            self.length * cos(self.theta) + self.offset.y,
        )

    def draw(self, screen):
        if len(self.lines) > 1:
            pygame.draw.aalines(
                screen,
                (190, 190, 190),
                False,
                self.lines,
            )

        # Draw the antialiased line
        pygame.draw.line(screen, (30, 30, 30), self.offset, self.position, 2)

        # Draw the antialiased circle
        pygame.gfxdraw.aacircle(
            screen, int(self.position.x), int(self.position.y), self.radius, self.color
        )
        pygame.gfxdraw.filled_circle(
            screen, int(self.position.x), int(self.position.y), self.radius, self.color
        )
