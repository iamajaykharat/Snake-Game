# Game Development in python by pygame.
# initialize first
import random
import os
import pygame

pygame.mixer.init()
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)

# Creating Game Window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background image
bgimg = pygame.image.load("bg.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

bgimg1 = pygame.image.load("home.jpg")
bgimg1 = pygame.transform.scale(bgimg1, (screen_width, screen_height)).convert_alpha()

pygame.display.set_caption("--------Play Snake With Ajay--------")
icon = pygame.image.load("icn1.png")
pygame.display.set_icon(icon)
pygame.display.update()

# Creating Clock
clock = pygame.time.Clock()
# Score on Screen/Window
font = pygame.font.SysFont(None, 40)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, (x, y))


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, (x, y, snake_size, snake_size))


# Home screen
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((200, 200, 255))
        gameWindow.blit(bgimg1, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back.mp3')
                    pygame.mixer.music.play(-1)
                    gameloop()
        pygame.display.update()
        clock.tick(30)


# Game Loop and Event Handling
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 110
    snake_y = 110
    snake_size = 20
    velocity_x = 0
    velocity_y = 0
    init_velocity = 7
    fps = 30
    score = 0
    snk_list = []
    snk_length = 1
    # Food generating here
    food_x = random.randint(110, screen_width - 110)
    food_y = random.randint(100, screen_height - 100)

    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    while not exit_game:

        # GameOver code2
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            bgimg2 = pygame.image.load("go.jpg")
            bgimg2 = pygame.transform.scale(bgimg2, (screen_width, screen_height)).convert_alpha()
            gameWindow.blit(bgimg2, (0, 0))
            text_screen("FINAL SCORE : " + str(score), white, 350, 450)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                # Moving of snake in all sides
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_q:
                        score += 20

            snake_x += velocity_x
            snake_y += velocity_y

            # Food Eating Process
            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score += 10
                food_x = random.randint(110, screen_width - 110)
                food_y = random.randint(100, screen_height - 100)
                snk_length += 5
                if score > int(highscore):
                    highscore = score

            # Snake Making and Window
            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))

            text_screen("SCORE: " + str(score) + "  HIGHSCORE: " + str(highscore), (255, 200, 200), 5, 5)
            pygame.draw.rect(gameWindow, red, (food_x, food_y, snake_size, snake_size))

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            # GameOver code1
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            if snake_x < 90 or snake_x > screen_width - 90 or snake_y < 60 or snake_y > screen_height - 60:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            plot_snake(gameWindow, white, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
