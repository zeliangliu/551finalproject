import pygame
import time
import random as rd
import tkinter as tk
from tkinter import messagebox

# set the window size
window_width = 640
window_height = 480


class Snake:

    # define the four snake's moving direction
    direction_horizontal = ['left', 'right']
    direction_vertical = ['up', 'down']
    width = 20

    def __init__(self):
        # one step moving length
        self.move_distance = 10
        # food color: yellow
        self.food_color = (255, 255, 0)
        self.reset()

    def reset(self):
        #the first-time position of snake head
        self.head = [320, 240]
        self.body = []
        #initialize sanke body: length = 10
        for i in range(10):
            self.body.insert(0, [self.head[0] - i * self.width, self.head[1]])
        #initialize food
        self.generated_food = []
        # the first moving direction is right
        self.current_direction = 'right'
        # moving speed is 10
        self.speed = 10
        # generate the screen into a map
        self.map = {}
        for x in range(32):
            for y in range(24):
                self.map[(x, y)] = 0
        self.generate_food()
        self.game_status = "stop"

    # set the game screen word and color
    def words_setting(self, pygame):
        font_of_title = pygame.font.SysFont('arial', 60)
        self.welcome_words = font_of_title.render('Snake Game', True, (255, 255, 255))
        font_of_tips = pygame.font.SysFont('arial', 40)
        self.start_words = font_of_tips.render('Click Here To Start', True, (255, 0, 0))
        self.close_game_words = font_of_tips.render('ESC to exit', True, (0, 0, 255))
        self.gameover_words = font_of_tips.render('Game Over', True, (255, 0, 0))
        self.restart_words = font_of_tips.render('Click Here To Restart', True, (255, 0, 0))

    # move the snake head
    def move(self):
        if self.current_direction in self.direction_horizontal:
            if self.current_direction == self.direction_horizontal[0]:
                self.head[0] -= self.move_distance
            else:
                self.head[0] += self.move_distance
        else:
            if self.current_direction == self.direction_vertical[0]:
                self.head[1] -= self.move_distance
            else:
                self.head[1] += self.move_distance

    # check the game status
    def check_status(self):
        # check if the snake eat itself
        if self.body.count(self.head) > 1:
            return True
        # check whether the snake hit the boundary of the screen
        if self.head[0] < 0 or self.head[0] > 620 or self.head[1] < 0 or self.head[1] > 460:
            return True
        return False

    # when the snake head hit the food then generate a new food
    def generate_food(self):
        if len(self.body) // 16 > 4:
            self.speed = len(self.body) // 16
        self.calculate_taken_position()
        # find the empty position to generate new food (at random)
        empty_position = []
        for position in self.map.keys():
            if not self.map[position]:
                empty_position.append(position)

        random = rd.choice(empty_position)
        self.generated_food = [random[0] * self.width, random[1] * self.width]

    # check the snake's moving direction
    def check_direction(self, changed_direction):
        if self.current_direction in self.direction_horizontal:
            if changed_direction in self.direction_vertical:
                self.current_direction = changed_direction
        else:
            if changed_direction in self.direction_horizontal:
                self.current_direction = changed_direction

    #calculate positoin
    def calculate_taken_position(self):
        for x, y in self.body:
            self.map[(x // self.width, y // self.width)] = 1

    #run mysnake
    def run(self, pygame, screen):
        if self.game_status == "run":
            self.move()
            self.body.append(self.head[:])
            # check if the snake eat the food
            if self.head == self.generated_food:
                self.generate_food()
            else:
                self.body.pop(0)
            # draw the snake on the screen
            for x, y in self.body:
                pygame.draw.rect(screen, [255, 255, 255], [x, y, self.width, self.width], 0)
            #draw the food on the screen
            pygame.draw.rect(screen, self.food_color,
                             [self.generated_food[0], self.generated_food[1], self.width, self.width], 0)
            #generate game over window
            if self.check_status():
                self.reset()
                screen.blit(self.gameover_words, ((window_width - self.gameover_words.get_width()) / 2,
                                                  (window_height - self.gameover_words.get_height()) / 2))
                screen.blit(self.restart_words, ((window_width - self.restart_words.get_width()) / 2,
                                                 (window_height - self.gameover_words.get_height()) / 2 + 50))
                screen.blit(self.close_game_words, ((window_width - self.close_game_words.get_width()) / 2, 400))
                pygame.display.update()
                self.game_status = "finish"
        #generate game start window
        elif self.game_status == "stop":
            screen.blit(self.welcome_words, ((window_width - self.welcome_words.get_width()) / 2, 100))
            screen.blit(self.start_words, ((window_width - self.start_words.get_width()) / 2, 300))
            screen.blit(self.close_game_words, ((window_width - self.close_game_words.get_width()) / 2, 400))
        else:
            return
        pygame.display.update()
        pygame.time.Clock().tick(self.speed)


def main():
    pygame.init()
    pygame.mixer.init()
    snake = Snake()
    screen = pygame.display.set_mode((window_width, window_height), 0, 32)
    pygame.display.set_caption('Snake')
    new_direction = snake.current_direction
    snake.words_setting(pygame)
    background_image = pygame.image.load("Background.jpg")

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.K_ESCAPE:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if snake.game_status == "run":
                    pressed_direction = ""
                    if event.key == pygame.K_LEFT:
                        pressed_direction = "left"
                    elif event.key == pygame.K_RIGHT:
                        pressed_direction = "right"
                    elif event.key == pygame.K_UP:
                        pressed_direction = "up"
                    elif event.key == pygame.K_DOWN:
                        pressed_direction = "down"
                    if pressed_direction != "":
                        snake.check_direction(pressed_direction)
            elif (snake.game_status == "stop") and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if ((window_width - snake.start_words.get_width()) / 2) <= x <= (
                        ((window_width - snake.start_words.get_width()) / 2) + snake.start_words.get_width()):
                    if (310) <= y <= (310 + snake.start_words.get_height()):
                        snake.game_status = "run"
            elif (snake.game_status == "finish") and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if ((window_width - snake.restart_words.get_width()) / 2) <= x <= (
                        ((window_width - snake.restart_words.get_width()) / 2) + snake.restart_words.get_width()):
                    if ((window_height - snake.restart_words.get_height()) / 2 + 50) <= y <= (((window_height - snake.restart_words.get_height()) / 2 + 50) + snake.restart_words.get_height()):
                        snake.game_status = "run"

        screen.blit(background_image, [0, 0])
        snake.run(pygame, screen)


if __name__ == '__main__':
    main()
