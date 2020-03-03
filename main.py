import sys
import pygame
import random
pygame.init()

#colors
black = (0, 0, 0)
white = (255, 255, 255)
red =(255, 0, 0)
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.length = 2
        self.vel_x = 20
        self.vel_y = 0
        self.body = [ [0, 0, 'right'] , [20, 0, 'right'] ]
        self.color = white
        self.height = 20
        self.width = 20
     
    def draw(self):
        for x, y, buf in self.body:
            pygame.draw.rect(win, white, (x, y, self.width, self.width))
        pygame.draw.rect(win, (0, 0, 255), (self.body[self.length - 1][0], self.body[self.length - 1][1] , self.width, self.width))
        
    def move(self, direction):
        for i in range(self.length - 1):
            self.body[i][2] = self.body[i + 1][2]
        self.body[self.length-1][2] = direction
        for i in range(self.length):
            if self.body[i][2] == 'right':
                self.body[i][0] += 20
            elif self.body[i][2] == 'left':
                self.body[i][0] -= 20
            elif self.body[i][2] == 'up':
                self.body[i][1] -= 20
            elif self.body[i][2] == 'down':
                self.body[i][1] += 20
    def add_food(self):
        x = self.body[0][0]
        y = self.body[0][1]
        di = self.body[0][2]
        if di == 'right':
            self.body.insert(0, [x - 20, y, 'right'])
        elif di == 'left':
            self.body.insert(0, [x + 20, y, 'left']) 
        elif di == 'up':
            self.body.insert(0, [x, y + 20, 'up']) 
        elif di == 'down':
            self.body.insert(0, [x, y - 20, 'down']) 
        self.length += 1

    def game_over(self):
        x = self.body[self.length - 1][0]
        y = self.body[self.length - 1][1]
        if x > 780 or x < 0 or y > 580 or y < 0:
            return True
        for i in range(self.length - 1):
            if self.body[i][0] == self.body[self.length - 1][0] and self.body[i][1] == self.body[self.length -1][1]:
                return True 
        return False

    def collide(self,food):
        x = food.x
        y = food.y 
        s_x = self.body[self.length - 1][0]
        s_y = self.body[self.length - 1][1]
        #s_x += 10
        #s_y += 10
        return pygame.Rect(s_x, s_y, 20, 20).colliderect(pygame.Rect(x, y, 20, 20))   
 
class Food:
    def __init__(self, x, y):
        self.height = 20
        self.width = 20
        self.color = red
        self.x = x
        self.y = y
    
    def draw(self):
        pygame.draw.rect(win, red , (self.x, self.y, self.width, self.width))
        
if __name__ == "__main__":
    running = True
    win = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('PySnake')
    snake = Snake()
    food_availabale = False
    food = None
    speed = 15
    while running:
        clock.tick(speed)
        win.fill(black)
        #Quit Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #Draw Food
        if not food_availabale:
            x = random.randint(1, 19)
            y = random.randint(1, 29)
            food = Food(x * 20, y * 20)
            food.draw()
            food_availabale = True
        else:
            if food != None:
                food.draw()
        if snake.collide(food):
            snake.add_food()
            food_availabale = False
            food = None
            speed += 0
        #Controls
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_LEFT] and snake.body[snake.length-1][2] != 'right':
            snake.move('left')
        elif keys[pygame.K_RIGHT] and snake.body[snake.length-1][2] != 'left':
            snake.move('right')
        elif keys[pygame.K_UP] and snake.body[snake.length-1][2] != 'down':
            snake.move('up')
        elif keys[pygame.K_DOWN] and snake.body[snake.length-1][2] != 'up':
            snake.move('down')
        snake.move(snake.body[snake.length-1][2])
        snake.draw()            
        #Coliison
        if snake.collide(food):
            snake.add_food()
            food_availabale = False
            food = None
            speed += 0
        if snake.game_over():
            running = False
        pygame.display.update()