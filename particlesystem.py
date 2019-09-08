import pygame
import random
from enum import Enum

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game")

carryOn = True
 
clock = pygame.time.Clock()

def lerp(a, b, t):
    return(a + (b - a) * t)
def colorLerp(c1, c2, t):
    return((c1[0] + (c2[0] - c1[0]) * t, 
            c1[1] + (c2[1] - c1[1]) * t,
            c1[2] + (c2[2] - c1[2]) * t))

class Particle:
    def __init__(self, pos, color, opacity, size, speedX, speedY, lifespan):
        self.pos = pos
        self.color = color
        self.opacity = opacity
        self.size = size
        self.speedX = speedX
        self.speedY = speedY
        self.lifespan = lifespan
        self.deathClock = 0
    def render(self):
        pygame.draw.circle(screen, self.color, [int(self.pos[0]), int(self.pos[1])], int(self.size))

class OriginType(Enum):
    Point = 0
    Box = 1

class ParticleSystem:
    def __init__(self, origin, frequence, atATime, color, lifespan, xspread, gravity, randomLife, size, origintype, originSize):
        self.origin = origin
        self.particles = []
        self.frequence = frequence
        self.color = color
        self.lifespan = lifespan
        self.xspread = xspread
        self.gravity = gravity
        self.randomLife = randomLife
        self.size = size
        self.origintype = origintype
        self.originSize = originSize
        self.atATime = atATime
        self.timer = 0
    def update(self):
        self.timer += 1;
        if (self.timer >= self.frequence):
            self.timer = 0;
            for k in range(self.atATime):
                randx = random.random()
                self.particles.append(Particle(self.origin[:] if self.origintype == OriginType.Point else [self.origin[0] + self.originSize[0] * randx, self.origin[1] + self.originSize[1] * random.random()], 
                                               self.color[:],
                                               1, 
                                               self.size, 
                                               (random.random()*self.xspread-(self.xspread/2)) if self.origintype == OriginType.Point else (random.random() * self.xspread * (randx*2 - 1)), 
                                               0, 
                                               self.lifespan + (random.random()*self.lifespan*self.randomLife)-(self.lifespan/2)))
        
        for i in range(len(self.particles)):
            self.particles[i].deathClock += 1
        self.particles = [part for part in self.particles if part.deathClock < part.lifespan]
            
        for i in range(len(self.particles)):
            particleTime = self.particles[i].deathClock/self.particles[i].lifespan
            if isinstance(self.size, list):
                self.particles[i].size = lerp(self.size[0], self.size[1], particleTime)
            if isinstance(self.color, list):
                self.particles[i].color = colorLerp(self.color[0], self.color[1], particleTime)
            self.particles[i].speedY += self.gravity;
            self.particles[i].pos[0] += self.particles[i].speedX
            self.particles[i].pos[1] += self.particles[i].speedY
    def render(self):
        for part in self.particles:
            part.render()

partsys = ParticleSystem([350, 250], 1, 2, [(255, 255, 0), (255, 0, 0)], 70, 1, -0.15, 0.2, [6, 0], OriginType.Box, [15, 15])
smoke = ParticleSystem([358, 250], 1, 2, [(60, 60, 60), (0, 0, 0)], 150, 2, -0.15, 0.2, [10, 0], OriginType.Point, [15, 15])

while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False

    # --- Game logic should go here
    partsys.update()
    smoke.update()
    # --- Drawing code should go here
    screen.fill(BLACK)
    smoke.render()
    partsys.render()

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    
    # --- Limit to 60 frames per second
    clock.tick(60)

#Once we have exited the main program loop we can stop the game engine:
pygame.quit()