import pygame
import random
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

SCR_WIDTH = 835
SCR_HEIGHT = 550
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
PADDLE_HEIGHT = 10
ROWS = 8
COLUMNS = 10
NO_OF_LIVES = 3
BG_COLOUR = (30, 30, 40)
PADDLE_COLOR = (154, 223, 252)

pygame.init()
pygame.display.set_caption("Brick Breaker")
screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 15)

def introScreen():
    font_ = pygame.font.SysFont('Berlin Sans FB', 100)
    r, g, b = random.randrange(150, 256), random.randrange(150, 256), random.randrange(150, 256)
    while pygame.time.get_ticks() < 6000:
        if pygame.time.get_ticks() % 500 <= 50:
            r, g, b = random.randrange(50, 256), random.randrange(150, 256), random.randrange(50, 256)
        text_1 = font_.render("Brick", True, (r, g, b))
        text_2 = font_.render("Breaker", True, (r, g ,b))
        textRect_1 = text_1.get_rect()
        textRect_2 = text_2.get_rect()
        textRect_1.center = ((SCR_WIDTH//2)-50, (SCR_HEIGHT//2)-50)
        textRect_2.center = ((SCR_WIDTH//2)+10, (SCR_HEIGHT//2)+50)
        screen.fill(BG_COLOUR)
        screen.blit(text_1, textRect_1)
        screen.blit(text_2, textRect_2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        clock.tick(60)
        pygame.display.update()

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.powerup = random.randrange(0, 6)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.vel = 7
        self.move = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > self.width//2 + self.vel:
            self.move = True
            self.x -= self.vel

        if keys[pygame.K_RIGHT] and self.x < SCR_WIDTH - self.width//2 - self.vel:
            self.move = True
            self.x += self.vel

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
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
        self.life = NO_OF_LIVES
        self.collision_threshold = 6
        self.collide = True

    def update(self, paddle):
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
            self.life -= 1
            self.reset_ball(paddle)

        if self.rect.colliderect(paddle.rect):
            self.y_vel = -5

        self.rect.center = (self.x, self.y)

    def reset_ball(self, paddle):
        self.x = paddle.x
        self.y = paddle.y - 20
        self.x_vel = random.choice((5, -5))
        self.y_vel = -5

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        r, g, b = random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)
        self.image = font.render("PowerUp", True, (r, g, b))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.vel = 1
        self.type = random.randrange(0, 4)

    def update(self):
        r, g, b = random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)
        self.image = font.render("PowerUp", True, (r, g, b))
        self.y += self.vel
        if self.y > SCR_HEIGHT + 20:
            self.kill()
        self.rect.center = (self.x, self.y)
        
def createBricks(brick_group, paddle, ball):
    for i in range(ROWS):
        for j in range(COLUMNS):
            r, g, b = random.randrange(50, 256), random.randrange(50, 256), random.randrange(50, 256)
            brick = Brick(j*BRICK_WIDTH+20, i*BRICK_HEIGHT+20, BRICK_WIDTH-5, BRICK_HEIGHT-5, (r, g, b))
            brick_group.add(brick)

    paddle.move = False
    paddle.x = SCR_WIDTH//2
    paddle.y = SCR_HEIGHT-20
    ball.life = NO_OF_LIVES
    return brick_group

def gameManager(screen, ball, paddle, brick_group, power_group):
    brick_group.draw(screen)
    paddle_group.draw(screen)
    paddle_group.update()
    ball_group.draw(screen)
    ball_group.update(paddle)
    power_group.draw(screen)
    power_group.update()

    lives = font.render(f"Lives: {ball.life}", True, (255, 255, 255))
    screen.blit(lives, (10, SCR_HEIGHT - 30))

    if len(brick_group.sprites()) == 0 or ball.life == 0:
        power_group.empty()
        brick_group = createBricks(brick_group, paddle, ball)
        ball.reset_ball(paddle)
        paddle.width = 100
        paddle.vel = 7
        ball.x_vel = 5 if ball.x_vel > 0 else -5
        ball.y_vel = 5 if ball.y_vel > 0 else -5
        ball.collide = True

    brick_collided_list = pygame.sprite.spritecollide(ball, brick_group, True)
    if len(brick_collided_list):
        for brick in brick_collided_list:
            if ball.collide == True:
                if abs(ball.rect.bottom - brick.rect.top) < ball.collision_threshold and ball.y_vel > 0:
                    ball.y_vel *= -1
                if abs(ball.rect.top - brick.rect.bottom) < ball.collision_threshold and ball.y_vel < 0:
                    ball.y_vel *= -1
                if abs(ball.rect.right - brick.rect.left) < ball.collision_threshold and ball.y_vel > 0:
                    ball.x_vel *= -1
                if abs(ball.rect.left - brick.rect.right) < ball.collision_threshold and ball.y_vel < 0:
                    ball.x_vel *= -1

            if brick.powerup == 1:
                powerup = Powerup(brick.rect.centerx, brick.rect.centery)
                power_group.add(powerup)

    power_collided_list = pygame.sprite.spritecollide(paddle, power_group, True)
    if len(power_collided_list):
        if power_collided_list[0].type == 0:
            paddle.width = 200
            paddle.vel = 7
            ball.x_vel = 5 if ball.x_vel > 0 else -5
            ball.y_vel = 5 if ball.y_vel > 0 else -5
            ball.collide = True

        elif power_collided_list[0].type == 1:
            paddle.width = 100
            paddle.vel = 10
            ball.x_vel = 5 if ball.x_vel > 0 else -5
            ball.y_vel = 5 if ball.y_vel > 0 else -5
            ball.collide = True
            
        elif power_collided_list[0].type == 2:
            paddle.width = 100
            paddle.vel = 7
            ball.x_vel = 2 if ball.x_vel > 0 else -2
            ball.y_vel = 2 if ball.y_vel > 0 else -2
            ball.collide = True

        elif power_collided_list[0].type == 3:
            paddle.width = 100
            paddle.vel = 7
            ball.x_vel = 5 if ball.x_vel > 0 else -5
            ball.y_vel = 5 if ball.y_vel > 0 else -5
            ball.collide = False

        elif power_collided_list[0].type == 4:
            ball.life += 1
    
brick_group = pygame.sprite.Group()
paddle_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
power_group = pygame.sprite.Group()

paddle = Paddle(SCR_WIDTH//2, SCR_HEIGHT-20, 100, PADDLE_HEIGHT, PADDLE_COLOR)
paddle_group.add(paddle)

ball = Ball(SCR_WIDTH//2, SCR_HEIGHT-40, "ball.png")
ball_group.add(ball)

brick_group = createBricks(brick_group, paddle, ball)

run = True
while run:
    introScreen()
    screen.fill(BG_COLOUR)
    gameManager(screen, ball, paddle, brick_group, power_group)
    pygame.display.update()
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()