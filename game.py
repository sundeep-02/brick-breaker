import pygame
import random
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

SCR_WIDTH = 835
SCR_HEIGHT = 550
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
ROWS = 1
COLUMNS = 2
BG_COLOUR = (30, 30, 40)
PADDLE_COLOR = (154, 223, 252)

pygame.init()
pygame.display.set_caption("Brick Breaker")
screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
clock = pygame.time.Clock()

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.vel = 6
        self.move = False

    def update(self, brick_group):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > self.vel:
            self.move = True
            self.x -= self.vel

        if keys[pygame.K_RIGHT] and self.x < SCR_WIDTH - self.width - self.vel:
            self.move = True
            self.x += self.vel

        if len(brick_group.sprites()) == 0:
            keys = []
            self.move = False
            self.x = SCR_WIDTH//2
            self.y = SCR_HEIGHT-20

        self.rect.center = (self.x, self.y)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, picture):
        super().__init__()
        self.image = pygame.image.load(picture)
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.x_vel = random.choice((5, -5))
        self.y_vel = -5

    def update(self, paddle, brick_group):
        if paddle.move: 
            self.x += self.x_vel
            self.y += self.y_vel

        if self.rect.left <= 0:
            self.x_vel = 5

        if self.rect.right >= SCR_WIDTH:
            self.x_vel = -5

        if self.rect.top <= 0:
            self.y_vel = 5

        if self.rect.bottom >= SCR_HEIGHT:
            self.reset_ball(paddle)

        if self.rect.colliderect(paddle.rect):
            self.y_vel = -5 

        collided_list = pygame.sprite.spritecollide(ball, brick_group, True)
        if len(collided_list):
            self.y_vel *= -1

        if len(brick_group.sprites()) == 0:
            self.reset_ball(paddle)
            brick_group = createBricks(brick_group)

        self.rect.center = (self.x, self.y)

    def reset_ball(self, paddle):
        self.x = paddle.x + PADDLE_WIDTH//2
        self.y = paddle.y - 20
        self.x_vel = random.choice((5, -5))
        self.y_vel = -5
    
def createBricks(brick_group):
    for i in range(ROWS):
        for j in range(COLUMNS):
            r, g, b = random.randrange(50, 256), random.randrange(50, 256), random.randrange(50, 256)
            brick = Brick(j*BRICK_WIDTH+20, i*BRICK_HEIGHT+20, BRICK_WIDTH-5, BRICK_HEIGHT-5, (r, g, b))
            brick_group.add(brick)
    return brick_group

brick_group = pygame.sprite.Group()
brick_group = createBricks(brick_group)
paddle_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()

paddle = Paddle(SCR_WIDTH//2, SCR_HEIGHT-20, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_COLOR)
paddle_group.add(paddle)

ball = Ball(SCR_WIDTH//2, SCR_HEIGHT-40, "ball.png")
ball_group.add(ball)

run = True
while run:
    screen.fill(BG_COLOUR)
    brick_group.draw(screen)
    paddle_group.draw(screen)
    paddle_group.update(brick_group)
    ball_group.draw(screen)
    ball_group.update(paddle, brick_group)

    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()