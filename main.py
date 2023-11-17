import pygame, sys
import os
from pygame.locals import *

# Constants for colors and screen size
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
pygame.font.init()
# Set up the Pygame window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Menu")

# Pygame font initialization
FONT = pygame.font.SysFont('Sora', 50)

def draw_menu():
    win.fill(BLACK)
    
    # Draw menu options and create rectangles
    title_text = FONT.render("Space Shooter Menu", True, WHITE)
    start_text = FONT.render("Start Game", True, WHITE)
    instructions_text = FONT.render("Instructions", True, WHITE)
    settings_text = FONT.render("Settings", True, WHITE)
    quit_text = FONT.render("Quit", True, WHITE)
    
    # Position menu options
    title_rect = title_text.get_rect(center=(WIDTH//2, 100))
    start_rect = start_text.get_rect(center=(WIDTH//2, 200))
    instructions_rect = instructions_text.get_rect(center=(WIDTH//2, 300))
    settings_rect = settings_text.get_rect(center=(WIDTH//2, 400))
    quit_rect = quit_text.get_rect(center=(WIDTH//2, 500))
    
    # Display menu options
    win.blit(title_text, title_rect)
    win.blit(start_text, start_rect)
    win.blit(instructions_text, instructions_rect)
    win.blit(settings_text, settings_rect)
    win.blit(quit_text, quit_rect)

    pygame.display.update()
    
    # Return the rectangles for menu options
    return start_rect, instructions_rect, settings_rect, quit_rect



WIDTH, HEIGHT = 1400,800
WIN = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Space_Shooter")

WHITE=(255,255,255)
BLACK=(0,0,0)
BORDER = pygame.Rect(WIDTH//2-8,0,16,HEIGHT)

HEALTH_FONT = pygame.font.SysFont('Sora',50)
WIN_FONT = pygame.font.SysFont('Sora',150)

BLUE_HIT = pygame.USEREVENT +1
RED_HIT = pygame.USEREVENT +2

FPS=120
VEL=8
BULLET_VEL = 15
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 100,100
JOYSTICK_SPACE_WIDTH = 700
JOYSTICK_SPACE_HEIGHT = 700
BLUE_SPACESHIP = pygame.image.load(os.path.join('Assets','spaceship_blue.png'))
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

RED_SPACESHIP = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space 4.png')),(WIDTH, HEIGHT))


def draw_window(red, blue, red_bullets, blue_bullets,red_health, blue_health):

    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER )

    red_health_text = HEALTH_FONT.render("HP: "+str(red_health), 1, WHITE)
    blue_health_text = HEALTH_FONT.render("HP: "+str(blue_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width()-10,10))
    WIN.blit(blue_health_text,(10,10))

    WIN.blit(BLUE_SPACESHIP, (blue.x, blue.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
         pygame.draw.rect(WIN,(255,0,0),bullet)
    for bullet in blue_bullets:
         pygame.draw.rect(WIN,(0,0,255),bullet)

    pygame.display.update()

def blue_movement(keys_pressed, blue):
        if keys_pressed[pygame.K_a] and blue.x - VEL>0: #left
            blue.x -= VEL
        if keys_pressed[pygame.K_d] and blue.x + VEL<592: #right
            blue.x += VEL
        if keys_pressed[pygame.K_w] and blue.y - VEL>0: #up
            blue.y -= VEL
        if keys_pressed[pygame.K_s] and blue.y +VEL<700: #down
            blue.y += VEL

def red_movement(keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and red.x -VEL>BORDER.x + BORDER.width: #left
            red.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #right
            red.x += VEL
        if keys_pressed[pygame.K_UP] and red.y - VEL>0: #up
            red.y -= VEL
        if keys_pressed[pygame.K_DOWN] and red.y +VEL<700: #down
            red.y += VEL

def joystick_red_movement(red):
    # Get joystick axes
    left_right_axis = pygame.joystick.Joystick(0).get_axis(0)  # X-axis
    up_down_axis = pygame.joystick.Joystick(0).get_axis(1)  # Y-axis

    # Modify red spaceship's movement based on joystick inputs
    if abs(left_right_axis) > 0.1:
        if left_right_axis < -0.1 and red.x - VEL > BORDER.x + BORDER.width:  # left
            red.x -= VEL
        elif left_right_axis > 0.1 and red.x + VEL + red.width < BORDER.x + BORDER.width + JOYSTICK_SPACE_WIDTH:  # right
            red.x += VEL

    if abs(up_down_axis) > 0.1:
        if up_down_axis < -0.1 and red.y - VEL > BORDER.y:  # up
            red.y -= VEL
        elif up_down_axis > 0.1 and red.y + VEL < BORDER.y + JOYSTICK_SPACE_HEIGHT:  # down
            red.y += VEL

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
print(joysticks)

def handle_bullets(blue_bullets, red_bullets, blue, red):
     for bullet in blue_bullets:
          bullet.x += BULLET_VEL
          if red.colliderect(bullet):
               pygame.event.post(pygame.event.Event(RED_HIT))
               blue_bullets.remove(bullet)
          elif bullet.x > WIDTH:
               blue_bullets.remove(bullet)

     for bullet in red_bullets:
          bullet.x -= BULLET_VEL
          if blue.colliderect(bullet):
               pygame.event.post(pygame.event.Event(BLUE_HIT))
               red_bullets.remove(bullet)
          elif bullet.x <0:
               red_bullets.remove(bullet)

def draw_winner(text):
     draw_text = WIN_FONT.render(text, 1, WHITE)
     WIN.blit(draw_text, (WIDTH/2- draw_text.get_width()/2,HEIGHT/2 - draw_text.get_height()/2))
     pygame.display.update()
     pygame.time.delay(5000)



def main():

    red = pygame.Rect(1150, 350, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    blue = pygame.Rect(150, 350, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    blue_bullets=[]
    red_bullets=[]

    red_health=8
    blue_health=8

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
          
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                
            #joystick_red_movement(red)



            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE and len(blue_bullets) < MAX_BULLETS:
                      bullet = pygame.Rect(blue.x + blue.width, blue.y + blue.height//2 - 2,10,5)
                      blue_bullets.append(bullet)
                      
                 if event.key == pygame.K_RCTRL and len(red_bullets)<MAX_BULLETS:
                      bullet = pygame.Rect(red.x, red.y + red.height//2 - 2,10,5)
                      red_bullets.append(bullet)

            if event.type == pygame.JOYBUTTONDOWN:
                 if event.button == 0:  # Replace 0 with the correct button index for 'A'
                     if len(red_bullets) < MAX_BULLETS:
                         bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                         red_bullets.append(bullet)

            if event.type == RED_HIT:
                 red_health -=1
            
            if event.type == BLUE_HIT:
                 blue_health -=1

        win_text=''
        if red_health<=0:
             win_text = "BLUE WINS!"
             
        if blue_health<=0:
             win_text = "RED WINS!"
             
        
        if win_text != '':
             draw_winner(win_text)
             break
             
        keys_pressed = pygame.key.get_pressed()
        blue_movement(keys_pressed, blue)
        red_movement(keys_pressed, red)

        handle_bullets(blue_bullets, red_bullets, blue, red)
        
        draw_window(red,blue, red_bullets, blue_bullets, red_health, blue_health)
       

 
def main_menu():
    running = True
    while running:
        start_rect, instructions_rect, settings_rect, quit_rect = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    print("Start Game Selected")
                    main()
                elif instructions_rect.collidepoint(mouse_pos):
                    print("Instructions Selected")
                    # Add code to display instructions
                elif settings_rect.collidepoint(mouse_pos):
                    print("Settings Selected")
                    # Add code to adjust game settings
                elif quit_rect.collidepoint(mouse_pos):
                    print("Quit Selected")
                    pygame.quit()
                    sys.exit()
if __name__ == "__main__":
    main_menu()
