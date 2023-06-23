import pygame
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")

# Player class
class Player:
    def __init__(self):
        self.lives = 5
        self.gold = 100

        # Load font
        self.font = pygame.font.Font(None, 30)

    def draw(self):
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        gold_text = self.font.render(f"Gold: {self.gold}", True, WHITE)
        win.blit(lives_text, (10, 10))
        win.blit(gold_text, (10, 40))

# Enemy class
class Enemy:
    def __init__(self):
        self.x = 0
        self.y = HEIGHT // 2
        self.width = 20
        self.height = 20
        self.vel = 2
        self.health = 10

    def move(self):
        self.x += self.vel

    def draw(self):
        pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height))

    def reached_end(self):
        return self.x >= WIDTH

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.color = WHITE
        self.vel = 5

    def move(self):
        self.x += self.vel

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

# Tower class
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.range = 150
        self.damage = 1
        self.cooldown = 60  # 1 second cooldown at 60 frames per second
        self.can_shoot = True

    def draw(self):
        pygame.draw.rect(win, GREEN, (self.x, self.y, self.width, self.height))

    def shoot(self, enemy):
        if self.can_shoot and self.is_within_range(enemy):
            bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2)
            bullets.append(bullet)
            self.can_shoot = False

    def is_within_range(self, enemy):
        distance = ((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) ** 0.5
        return distance <= self.range

    def update_cooldown(self):
        if not self.can_shoot:
            self.cooldown -= 1
            if self.cooldown <= 0:
                self.can_shoot = True
                self.cooldown = 60  # Reset the cooldown

# Create objects
player = Player()
enemies = [Enemy()]
towers = []
bullets = []

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # Frame rate

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and player.gold >= 10:
            mouse_pos = pygame.mouse.get_pos()
            tower = Tower(mouse_pos[0], mouse_pos[1])
            towers.append(tower)
            player.gold -= 10

    # Move enemies
    for enemy in enemies:
        enemy.move()

    # Update towers
    for tower in towers:
        tower.update_cooldown()
        for enemy in enemies:
            tower.shoot(enemy)

    # Move bullets
    for bullet in bullets:
        bullet.move()

    # Remove bullets that are off-screen
    bullets = [bullet for bullet in bullets if bullet.x <= WIDTH]

    # Draw the game window
    win.fill((0, 0, 0))  # Clear the screen

    # Draw enemies
    for enemy in enemies:
        enemy.draw()

    # Draw towers
    for tower in towers:
        tower.draw()

    # Draw bullets
    for bullet in bullets:
        bullet.draw()

    # Draw player stats
    player.draw()

    # Update the game window
    pygame.display.update()

pygame.quit()
