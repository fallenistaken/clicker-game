import pygame
import sys
import os
import time
import pickle
from pygame.locals import *

pygame.mixer.init()
pygame.init()
pygame.font.init()
pygame.display.init()

size = width, height = 800, 600
font_size = 64
font = pygame.font.Font('assets/Poppins-ExtraLight.ttf', font_size)
font2 = pygame.font.Font('assets/Poppins-ExtraLight.ttf', 48)
font3 = pygame.font.Font('assets/Poppins-ExtraLight.ttf', 24)
cursor = pygame.image.load("assets/cursor.png")
cursor_clicked = pygame.image.load("assets/cursor_click.png")
clicksound = pygame.mixer.Sound('assets/click.mp3')
levelup = pygame.mixer.Sound('assets/100.mp3')
iconpath = "assets/icon.png"
icon = pygame.image.load(iconpath)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Clicker Game")
pygame.display.set_icon(icon)
clicks = 0
cps = 0
levels = 0
amountclicks = 1
last_click_time = time.time()
clock = pygame.time.Clock()

# Function to reset clicks, levels, and amountclicks
def reset_game():
    global clicks, levels, amountclicks
    clicks = 0
    levels = 0
    amountclicks = 1

def center_text_position(text_surface):
    text_width, text_height = text_surface.get_size()
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    return x, y

reset_button_rect = pygame.Rect(650, 500, 120, 40)
reset_button_color = (255, 0, 0)
reset_button_text = font3.render("Reset", True, (255, 255, 255))

game_data_filename = 'game_data.pkl'

# Load game data from a file if it exists
if os.path.exists(game_data_filename):
    with open(game_data_filename, 'rb') as file:
        game_data = pickle.load(file)
        clicks, levels, amountclicks = game_data

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save game data to the file before quitting
            with open(game_data_filename, 'wb') as file:
                pickle.dump([clicks, levels, amountclicks], file)
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check if the reset button is clicked
                if reset_button_rect.collidepoint(event.pos):
                    reset_game()
                else:
                    # Your existing click logic
                    if 100 <= clicks < 500:
                        clicks += 2
                    elif 500 <= clicks < 1000:
                        clicks += 3
                    elif clicks >= 1000:
                        clicks += 4
                    else:
                        clicks += 1

                    clicksound.play()  
                    current_time = time.time()
                    time_difference = current_time - last_click_time
                    if time_difference != 0:
                        cps = 1 / time_difference
                    last_click_time = current_time

    # Fill the screen with white background
    screen.fill((255, 255, 255))

    # Draw reset button after filling the screen
    pygame.draw.rect(screen, reset_button_color, reset_button_rect)
    screen.blit(reset_button_text, (660, 510))

    # Your existing code for rendering text and updating the display
    version = font3.render("v1.0", True, (0, 0, 0))
    text = font.render("Clicks: " + str(clicks), True, (0, 0, 0))
    level = font3.render("Level: " + str(levels) + "\nAmount of clicks per click: " + str(amountclicks), True, (0, 0, 0))
    text2 = font.render("", True, (0, 0, 0))
    cps_text = font3.render("CPS: {:.2f}".format(cps), True, (0, 0, 0))
    if clicks == 100:
        text = font2.render("You have reached level 1", True, (0, 0, 0)) 
        text2 = font2.render("(click to stop the sound)", True, (0, 0, 0)) 
        levels = 1
        amountclicks = 2
        levelup.play()
    elif clicks == 500:
        text = font2.render("You have reached 500 Clicks", True, (0, 0, 0))
        text2 = font2.render("(click to stop the sound)", True, (0, 0, 0)) 
        levelup.play()
    elif clicks == 1000:
        text = font2.render("You have reached 1,000 Clicks", True, (0, 0, 0))
        text2 = font2.render("(click to stop the sound)", True, (0, 0, 0))
        levelup.play()
    elif clicks == 5000:
        text = font2.render("You have reached 5,000 Clicks", True, (0, 0, 0))
        text2 = font2.render("(click to stop the sound)", True, (0, 0, 0))
        levelup.play() 
    elif clicks == 10000:
        text = font2.render("You have reached 10,000 Clicks", True, (0, 0, 0))
        text2 = font2.render("(click to stop the sound)", True, (0, 0, 0)) 
        levelup.play()
    
    x, y = center_text_position(text)
    screen.blit(text, (x, y))
    screen.blit(text2, (x, y+100))
    screen.blit(cps_text, (0, 550))
    screen.blit(level, (0, 0))
    screen.blit(version, (750, 550))
    pygame.display.flip()
