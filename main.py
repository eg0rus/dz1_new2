import pygame
import math

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
        self.target_pos = self.pos.copy()
        self.dragging = False
        self.drag_offset = pygame.Vector2(0, 0)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_pos = pygame.Vector2(event.pos)
            if self.pos.distance_to(click_pos) <= self.radius:
                self.dragging = True
                self.drag_offset = self.pos - click_pos
            else:
                self.target_pos = click_pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

    def update(self, dt, mouse_pos, keys):
        if self.dragging:
            self.pos = mouse_pos + self.drag_offset
            self.target_pos = self.pos.copy()
        else:
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
                self.target_pos = self.pos.copy()
            else:
                if self.pos.distance_to(self.target_pos) > 5:
                    if self.pos.distance_to(self.target_pos) > self.speed * dt:
                        direction = (self.target_pos - self.pos).normalize()
                        self.pos += direction * self.speed * dt
                    else:
                        self.pos = self.target_pos

    def draw(self, screen):
        pygame.draw.circle(screen, "pink", (int(self.pos.x), int(self.pos.y)), self.radius)

        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        if self.pos.distance_to(mouse_pos) < self.radius:
            pygame.draw.circle(screen, "red", (int(self.pos.x), int(self.pos.y)), self.radius + 2, 3)


running = True
dt = 0

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

while running:
    screen.blit(background_img, (0, 0))

    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        player.handle_event(event)

    player.update(dt, mouse_pos, keys)
    player.draw(screen)

    pygame.display.flip()

    dt = clock.tick(FPS) / 1000

pygame.quit()