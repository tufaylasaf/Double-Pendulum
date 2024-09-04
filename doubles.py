import pygame
import sys
from Pendulum import Pendulum
from math import pi, sin, cos
import pygame.gfxdraw
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
width, height = 450, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Double Pendulum")

clock = pygame.time.Clock()
fps = 60
g = 9.81
dt = 0.125

center = pygame.Vector2(width // 2, height // 3)

# pendA = Pendulum(12, 3.3836375204668463, 10, (127, 0, 255), 100, center)
# pendB = Pendulum(12, 4.37177945122265, 10, (127, 0, 255), 100, pendA.position)

pendA = Pendulum(12, 4.222060976865711, 10, (127, 0, 255), 100, center)
pendB = Pendulum(12, 0.4940709653779023, 10, (127, 0, 255), 100, pendA.position)


def motion(y):
    a1, a2, v1, v2 = y
    m1 = pendA.mass
    m2 = pendB.mass
    l1 = pendA.length
    l2 = pendB.length

    num1 = -g * (2 * m1 + m2) * sin(a1)
    num2 = -m2 * g * sin(a1 - 2 * a2)
    num3 = -2 * sin(a1 - a2) * m2
    num4 = v2 * v2 * l2 + v1 * v1 * l1 * cos(a1 - a2)
    den = l1 * (2 * m1 + m2 - m2 * cos(2 * a1 - 2 * a2))
    a = (num1 + num2 + num3 * num4) / den

    num1 = 2 * sin(a1 - a2)
    num2 = v1 * v1 * l1 * (m1 + m2)
    num3 = g * (m1 + m2) * cos(a1)
    num4 = v2 * v2 * l2 * m2 * cos(a1 - a2)
    den = l2 * (2 * m1 + m2 - m2 * cos(2 * a1 - 2 * a2))
    b = (num1 * (num2 + num3 + num4)) / den

    return np.array([v1, v2, a, b])


def rk4(y, dt):
    k1 = motion(y)
    k2 = motion(y + 0.5 * k1 * dt)
    k3 = motion(y + 0.5 * k2 * dt)
    k4 = motion(y + k3 * dt)

    return dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6


initial = np.array([pendA.theta, pendB.theta, 0, 0])
simulation_running = False  # Variable to track simulation state

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulation_running = not simulation_running  # Toggle simulation state

    if simulation_running:
        initial = initial + rk4(initial, dt)

    pendA.position = (
        pygame.Vector2(pendA.length * sin(initial[0]), pendA.length * cos(initial[0]))
        + pendA.offset
    )

    pendB.offset = pendA.position

    pendB.position = (
        pygame.Vector2(pendB.length * sin(initial[1]), pendB.length * cos(initial[1]))
        + pendB.offset
    )

    pendB.lines.append(pendB.position)

    pygame.display.flip()

    screen.fill((255, 255, 255))

    pendB.draw(screen)
    pendA.draw(screen)

    pygame.gfxdraw.aacircle(screen, int(center.x), int(center.y), 6, (30, 30, 30))
    pygame.gfxdraw.filled_circle(screen, int(center.x), int(center.y), 6, (30, 30, 30))

    clock.tick(fps)

# Clean up and quit
pygame.quit()
sys.exit()
