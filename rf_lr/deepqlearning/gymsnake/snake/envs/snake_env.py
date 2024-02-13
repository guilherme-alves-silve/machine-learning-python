import sys
import time
import random
import pygame
import numpy as np
import gym

from pygame.surfarray import array3d
from pygame.display
from gym import error, spaces, utils
from gym.utils import seeding


BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)


class SnakeEnv(gym.Env):

	metadata = {"render.modes": ["human"]}
    
    def __init__(self):
    	# [0, 1, 2, 3]
    	self.action_space = space.Discrete(4)
        self.width = 200
        self.height = 200
        self.window = pygame.display.set_mode((width, height))
        self.reset()
        self.STEP_LIMIT = 1000
        self.sleep = 0
        
    def reset(self):
        self.window.fill(BLACK)
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.food_pos = self.spawn_food()
        self.food_spawn = True
        
        self.direction = "RIGHT"
        self.action = self.direction
        
        self.score = 0
        self.steps = 0
        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0, 1)
        # observation
        return img
        
    @staticmethod
    def change_direction(action, direction):
        if action == 0 and direction != "DOWN":
            direction = "UP"
        if action == 1 and direction != "UP":
            direction = "DOWN"
        if action == 2 and direction != "RIGHT":
            direction = "LEFT"
        if action == 3 and direction != "LEFT":
            direction = "RIGHT"
        return direction
    
    @staticmethod
    def move(direction, snake_pos):
        if direction == "UP":
            snake_pos[1] -= 10
        elif direction == "DOWN":
            snake_pos[1] += 10
        elif direction == "LEFT":
            snake_pos[0] -= 10
        elif direction == "RIGHT":
            snake_pos[0] += 10
        return snake_pos
        
    def spawn_food(self):
        x = random.randrange(1, self.width//10)*10
        y = random.randrange(1, self.height//10)*10
        food = [x, y]
        if food in self.snake_body:
            return self.spawn_food()
        return food
    
    def eat(self):
        return self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]
    
    def step(self, action):
    	score_holder = self.score
    	reward = 0
    	self.direction = SnakeEnv.change_direction(action, self.direction)
    	self.snake_pos = SnakeEnv.move(self.direction, self.snake_pos)
    	self.snake_pos.insert(0, list(self.snake_pos))
    	# reward handler
    	reward = self.food_handler()

    	self.update_game_state()

    	reward, done = self.game_over(reward)

    	# get observations
    	obs = self.get_image_array_from_game()

    	info = {"score": self.score}
    	self.steps += 1
    	time.sleep(self.sleep)

        return obs, reward, done, info

    def game_over(self, reward):

        # Touch box
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.width-10:
            return -1, True
        elif self.snake_pos[1] < 0 or self.snake_pos[1] > self.height-10:
            return -1, True
            
        # Touch own body
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
	            return -1, True

	    if self.steps >= self.STEP_LIMIT:
	    	return 0, True

        return reward, False

    def food_handler(self):
    	if self.eat():
    		self.score += 1
    		reward = 1
    		self.food_spawn = False
    	else:
    		self.snake_body.pop()
    		reward = 0

    	if not self.food_spawn:
    		self.food_pos = self.spawn_food()
    	self.food_spawn = True

    	return reward

    def get_image_array_from_game(self):
        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0, 1)
        # observation
        return img

    def update_game_state(self):
	    # Drawing the snake
	    self.window.fill(BLACK)
	    for pos in self.snake_body:
	        pygame.draw.rect(self.window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
	    
	    # Drawing of food
	    pygame.draw.rect(self.window, WHITE, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))

	def render(self, mode="human"):
		if mode == "human":
			display.update()

	def close(self):
		pass
