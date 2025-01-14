import pygame
import random
score = 0
# Initialize Pygame and Joystick
pygame.init()
pygame.joystick.init()

add_player = 0

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Zombie Apocalypse')

# Load and scale background
background = pygame.image.load('images/background.webp')
background = pygame.transform.scale(background, (800, 600))

# Load and scale player sprite
player = pygame.image.load('images/soldier.png')
player_diff = pygame.transform.scale(player, (100, 100))

# Load and scale zombie sprite
zombie = pygame.image.load('images/zombie.png')
zombie_diff = pygame.transform.scale(zombie, (100, 100))

# Load and scale bullet sprite
bullet = pygame.image.load('images/bullet.png')
bullet = pygame.transform.scale(bullet, (20, 20))

# Player initial position
px, py = 360, 400

# Bullet initial position and state
bx, by = px, py
b_state = 'ready'  # "ready" means bullet is ready to fire, "fire" means it's moving

# Zombies initial positions
zombie_positions = [
    [random.randint(0, 600), random.randint(0, 100)],
    [random.randint(0, 600), random.randint(0, 100)],
    [random.randint(0, 600), random.randint(0, 100)],
]

# Initialize joystick list
joysticks = []

# Functions to draw player, zombies, and bullet
def draw_player():
    screen.blit(player_diff, (px, py))

def draw_zombies(zombies):
    for zx, zy in zombies:
        screen.blit(zombie_diff, (zx, zy))
def draw_zombies1(zombies):
    for zx, zy in zombies:
        screen.blit(zombie_diff, (zx, zy))

def fire_bullet(bx, by):
    screen.blit(bullet, (bx, by))

# Main game loop
running = True
while running:
    # Move zombies
    if score < 10:
         draw_zombies1(zombie_positions)

    for pos in zombie_positions:
        pos[0] += 0.5  # Move zombie to the right
        if pos[0] >= 800:  # Reset zombie position when it reaches the edge
            pos[0] = 0
            pos[1] += 50

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joy.init()
            joysticks.append(joy)
            print(f"Joystick {joy.get_name()} added.")
            add_player += 1

    # Handle joystick input
    for joystick in joysticks:
        if joystick.get_button(13):  # Button 13 pressed
            px -= 1  # Move player left
        if joystick.get_button(14):  # Button 14 pressed
            px += 1  # Move player right
        if joystick.get_button(7):  # Button 7 pressed
            py += 1  # Move player down
        if joystick.get_button(8):  # Button 8 pressed
            py -= 1  # Move player up
        if joystick.get_button(0):  # Button 0 fires the bullet
            if b_state == 'ready':
                b_state = 'fire'
                bx = px + 40  # Center the bullet with the player
                by = py

    # Bullet movement
    if b_state == 'fire':
        fire_bullet(bx, by)
        by -= 1 # Move the bullet up
    if by <= 0:
        b_state = 'ready'  # Reset bullet when it goes off-screen

    # Create rectangles for collision detection
    player_rect = pygame.Rect(px, py, 100, 100)  # Player rectangle
    zombie_rects = [pygame.Rect(zx, zy, 100, 100) for zx, zy in zombie_positions]  # Zombie rectangles
    bullet_rect = pygame.Rect(bx, by, 20, 20)  # Bullet rectangle

    # Check for collisions
    for i, zombie_rect in enumerate(zombie_rects):
        if player_rect.colliderect(zombie_rect):
            px, py = 360, 400  # Reset player position on collision
        if b_state == 'fire' and bullet_rect.colliderect(zombie_rect):
            b_state = 'ready'  # Reset bullet
            by = py
            score += 1
            zombie_positions[i] = [random.randint(0, 600), random.randint(0, 100)]  # Respawn zombie

    # Render the screen
    screen.blit(background, (0, 0))  # Draw background
    draw_player()  # Draw player
    draw_zombies(zombie_positions)  # Draw zombies
    if b_state == 'fire':
        fire_bullet(bx, by)  # Draw bullet if it's fired
    pygame.display.update()

pygame.quit()

