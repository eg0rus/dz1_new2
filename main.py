import pygame
pygame.init()

FPS = 60
SCREEN_WIDTH = 725
SCREEN_HEIGHT = 725

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background_img = pygame.image.load("images\\background.jpg")

clock = pygame.time.Clock()


class Player:
    def __init__(self, x, y, speed=300):
        self.pos = pygame.Vector2(x, y)
        self.speed = speed
        self.radius = 40

    def update(self, dt, keys):
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            move.y -= 1
        if keys[pygame.K_s]:
            move.y += 1
        if keys[pygame.K_a]:
            move.x -= 1
        if keys[pygame.K_d]:
            move.x += 1

        if move.length() > 0:
            move = move.normalize()
            self.pos += move * self.speed * dt

    def draw(self, screen):
        pygame.draw.circle(screen, "pink", (int(self.pos.x), int(self.pos.y)), self.radius)


running = True
dt = 0

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

while running:
    screen.blit(background_img, (0, 0))

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(dt, keys)
    player.draw(screen)

    pygame.display.flip()

    dt = clock.tick(FPS) / 1000

pygame.quit()