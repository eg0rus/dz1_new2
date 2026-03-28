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

projectile_pos = None
projectile_target = None
projectile_speed = 600
projectile_radius = 5
projectile_active = False

while running:
    screen.blit(background_img, (0, 0))

    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        player.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if not projectile_active:
                projectile_pos = player.pos.copy()
                projectile_target = pygame.Vector2(event.pos)
                projectile_active = True

    player.update(dt, mouse_pos, keys)

    if projectile_pos is not None:
        direction = (projectile_target - projectile_pos).normalize()
        projectile_pos += direction * projectile_speed * dt

        if (projectile_pos.distance_to(projectile_target) < 10 or
                projectile_pos.x < -100 or projectile_pos.x > SCREEN_WIDTH + 100 or
                projectile_pos.y < -100 or projectile_pos.y > SCREEN_HEIGHT + 100):
            projectile_pos = None
            projectile_active = False

    player.draw(screen)

    if projectile_pos is not None:
        pygame.draw.circle(screen, "red", (int(projectile_pos.x), int(projectile_pos.y)), projectile_radius)

    pygame.display.flip()

    dt = clock.tick(FPS) / 1000

pygame.quit()