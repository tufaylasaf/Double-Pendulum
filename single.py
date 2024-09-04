import pygame
import sys
from Pendulum import Pendulum
from math import sin, cos, pi

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Double Pendulum")

clock = pygame.time.Clock()
fps = 60
g = 0.25

center = pygame.Vector2(width // 2, height // 3)


pend = Pendulum(100, pi / 3, 14, (127, 0, 255), 125, center)

pendulums = []

for i in range(0, 8):
    pend = Pendulum(100, pi / 2, 10, (127, 0, 255), 25 + (i * 22), center)
    pendulums.append(pend)


def simulate(pendulum):
    pendulum.a = (-g * sin(pendulum.theta)) / pendulum.length

    pendulum.v += pendulum.a
    pendulum.theta += pendulum.v

    pendulum.position = pygame.Vector2(
        pendulum.length * sin(pendulum.theta) + pendulum.offset.x,
        pendulum.length * cos(pendulum.theta) + pendulum.offset.y,
    )


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for pend in pendulums:
        simulate(pend)

    screen.fill((255, 255, 255))

    for pend in pendulums:
        pend.draw(screen)
    # pend.draw(screen)
    pygame.gfxdraw.aacircle(screen, int(center.x), int(center.y), 3, (30, 30, 30))
    pygame.gfxdraw.filled_circle(screen, int(center.x), int(center.y), 3, (30, 30, 30))

    pygame.display.flip()

    clock.tick(fps)

# Clean up and quit
pygame.quit()
sys.exit()
