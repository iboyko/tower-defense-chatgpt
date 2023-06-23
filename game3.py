import pygame
import random
import math

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
        self.level = 1

        # Load font
        self.font = pygame.font.Font(None, 30)

    def draw(self):
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        gold_text = self.font.render(f"Gold: {self.gold}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        win.blit(lives_text, (10, 10))
        win.blit(gold_text, (10, 40))
        win.blit(level_text, (10, 70))

# Enemy class
class Enemy:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.vel = 2
        self.max_health = 10
        self.reset()

    def move(self):
        self.x += self.vel

    def draw(self):
        pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height))
        health_bar_width = self.width * (self.health / self.max_health)
        pygame.draw.rect(win, GREEN, (self.x, self.y - 10, health_bar_width, 5))

    def reached_end(self):
        return self.x >= WIDTH

    def reset(self):
        self.x = 0
        self.y = HEIGHT // 2
        self.health = self.max_health

# Bullet class
class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.radius = 5
        self.color = WHITE
        self.speed = 5
        self.target_x = target_x
        self.target_y = target_y
        self.dx = self.target_x - self.x
        self.dy = self.target_y - self.y
        self.distance = math.sqrt(self.dx ** 2 + self.dy ** 2)
        self.vx = (self.dx / self.distance) * self.speed
        self.vy = (self.dy / self.distance) * self.speed
        self.damage = 1

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

# Tower class
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.range = 150
        self.cooldown = 60  # 1 second cooldown at 60 frames per second
        self.can_shoot = True

    def draw(self):
        pygame.draw.rect(win, GREEN, (self.x, self.y, self.width, self.height))

    def shoot(self, enemy):
        if self.can_shoot and self.is_within_range(enemy):
            bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, enemy.x, enemy.y)
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
enemies = []
towers = []
bullets = []

# Game loop
running = True
clock = pygame.time.Clock()

def start_new_level():
    for i in range(player.level):
        enemy = Enemy()
        enemies.append(enemy)

def check_collisions():
    for bullet in bullets:
        enemy_killed = False  # Track if an enemy has been killed
        for enemy in enemies:
            if collision_detection(bullet, enemy):
                enemy.health -= bullet.damage
                bullets.remove(bullet)
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    enemy_killed = True  # Set the flag to indicate an enemy has been killed
                    if not enemies:
                        player.level += 1  # Increment level when all enemies are eliminated
                        start_new_level()
                break
        if enemy_killed:
            player.gold += 50  # Give the player 50 gold when an enemy is killed

def collision_detection(bullet, enemy):
    distance = math.sqrt((bullet.x - enemy.x) ** 2 + (bullet.y - enemy.y) ** 2)
    return distance <= bullet.radius + enemy.width

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

    # Move enemies if the player has remaining lives
    if player.lives > 0:
        for enemy in enemies:
            enemy.move()
            if enemy.reached_end():
                player.lives -= 1
                enemies.remove(enemy)

        # Add new enemy when necessary
        if not enemies:
            start_new_level()

    # Update towers
    for tower in towers:
        tower.update_cooldown()
        for enemy in enemies:
            tower.shoot(enemy)

    # Move bullets
    for bullet in bullets:
        bullet.move()

    # Check collisions
    check_collisions()

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
