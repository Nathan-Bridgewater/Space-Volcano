"""
2D gravity based simulation of volcanic activity on one of Jupiter's
moons. Visualisation plots the particle paths of different molecules
ejected by the volcano.
"""
import sys
import math
import random
import pygame as pg

pg.init()  # initialse pygame

# define colour table
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LT_GREY = (180, 180, 180)
GREY = (120, 120, 120)
DK_GREY = (80, 80, 80)


class Particle(pg.sprite.Sprite):
    """Build ejecta particles for volcano simulation."""

    # Define constants and dictionary containing colour tuples
    gases_colours = {'SO2': LT_GREY, 'CO2': GREY, 'H2S': DK_GREY, 'H2O': WHITE}
    VENT_LOCATION_XY = (320, 300)
    IO_SURFACE_Y = 308
    GRAVITY = 0.5  # pixels per frame; added to dy each game loop
    VELOCITY_SO2 = 8  # pixels per frame

    # scalar (SO2 atomic weight/particle atomic weight) used for velocity
    vel_scalar = {'SO2': 1, 'CO2': 1.45, 'H2S': 1.9, 'H2O': 3.6}

    def __init__(self, screen, background):
        super().__init__()

        # define class attributes
        self.screen = screen
        self.background = background
        self.image = pg.Surface((4, 4))
        self.rect = self.image.get_rect()

        # randomly choose a gas for each particle
        self.gas = random.choice(list(Particle.gases_colours.keys()))
        self.colour = Particle.gases_colours[self.gas]

        # scale particles velocity
        self.vel = Particle.VELOCITY_SO2 * Particle.vel_scalar[self.gas]

        # define starting position and calculate its vector
        self.x, self.y = Particle.VENT_LOCATION_XY
        self.vector()

    def vector(self):
        """Calculate particle vector at launch."""

        # choose an angle at random and calculate vector in x and y directions
        orientation = random.uniform(60, 120)  # 90 is vertical
        radians = math.radians(orientation)
        self.dx = self.vel * math.cos(radians)
        self.dy = -self.vel * math.sin(radians)

    def update(self):
        """Apply gravity, draw a path, and handle boundary conditions"""

        # include effect of gravity by adding to change in y
        self.dy += Particle.GRAVITY
        # draw a line between the old and new position
        pg.draw.line(self.background, self.colour, (self.x, self.y),
                     (self.x + self.dx, self.y + self.dy))

        self.x += self.dx
        self.y += self.dy

        # remove particle if it leaves the screen or passes the set y position
        if self.x < 0 or self.x > self.screen.get_width():
            self.kill()

        if self.y < 0 or self.y > Particle.IO_SURFACE_Y:
            self.kill()


def main():
    """Set up and run game screen and loop."""
    # create pygame surface and load the image file
    screen = pg.display.set_mode((639, 360))
    pg.display.set_caption('IO Volcano Simulator')
    background = pg.image.load('tvashtar_plume.gif')

    # set up colour coded legend
    legend_font = pg.font.SysFont('None', 24)
    water_label = legend_font.render('--- H20', True, WHITE, BLACK)
    h2s_label = legend_font.render('--- H2S', True, DK_GREY, BLACK)
    co2_label = legend_font.render('--- CO2', True, GREY, BLACK)
    so2_label = legend_font.render('--- SO2/S2', True, LT_GREY, BLACK)

    # create sprite gorup to manage all the particles
    particles = pg.sprite.Group()
    clock = pg.time.Clock()

    while True:
        clock.tick(25)  # frame rate
        particles.add(Particle(screen, background))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # end game if user closes window
                pg.quit()
                sys.exit()

        # draw labels and background image
        screen.blit(background, (0, 0))
        screen.blit(water_label, (40, 20))
        screen.blit(h2s_label, (40, 40))
        screen.blit(co2_label, (40, 60))
        screen.blit(so2_label, (40, 80))

        # update and draw particles
        particles.update()
        particles.draw(screen)
        pg.display.flip()


if __name__ == '__main__':
    main()
