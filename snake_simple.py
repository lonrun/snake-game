import pygame
import sys
import random

def setup_game():
        width = int(input("输入窗口宽度[默认为640]：") or 640)
        height = int(input("输入窗口高度[默认为480]：") or 480)
        snake_size = int(input("输入蛇大小[默认为20]：") or 20)
        snake_speed = int(input("输入蛇速度[默认为5]：") or 5)

        return (width, height), snake_size, snake_speed

class SnakeGame:

    def __init__(self):
        pygame.init()

        # 初始化游戏并获取屏幕尺寸、蛇大小和速度
        screen_size, snake_size, snake_speed = setup_game()

        self.screen_size = (screen_size.width, screen_size.height)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("贪食蛇")

        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)

        self.snake_size = snake_size
        self.snake_speed = snake_speed

        self.clock = pygame.time.Clock()
        self.font_style = pygame.font.SysFont(None, 50)

        self.game_loop()

    def draw_snake(self, snake_body):
        for x in snake_body:
            pygame.draw.rect(self.screen, self.BLACK, [x[0], x[1], self.snake_size, self.snake_size])

    def message(self, msg, color, pos):
        screen_text = self.font_style.render(msg, True, color)
        self.screen.blit(screen_text, pos)

    def game_loop(self):
        game_over = False

        x1 = self.screen_size[0] / 2
        y1 = self.screen_size[1] / 2
        x1_change = 0
        y1_change = 0

        snake_body = []
        length_of_snake = 1

        foodx = round(random.randrange(0, self.screen_size[0] - self.snake_size) / 20.0) * 20.0
        foody = round(random.randrange(0, self.screen_size[1] - self.snake_size) / 20.0) * 20.0

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -self.snake_size
                        y1_change = 0
                    if event.key == pygame.K_RIGHT:
                        x1_change = self.snake_size
                        y1_change = 0
                    if event.key == pygame.K_UP:
                        y1_change = -self.snake_size
                        x1_change = 0
                    if event.key == pygame.K_DOWN:
                        y1_change = self.snake_size
                        x1_change = 0

            if x1 >= self.screen_size[0] or x1 < 0 or y1 >= self.screen_size[1] or y1 < 0:
                game_over = True

            x1 += x1_change
            y1 += y1_change

            self.screen.fill(self.WHITE)
            pygame.draw.rect(self.screen, self.GREEN, [foodx, foody, self.snake_size, self.snake_size])

            snake_head = []
            snake_head.append(x1)
            snake_head.append(y1)
            snake_body.append(snake_head)
            if len(snake_body) > length_of_snake:
                del snake_body[0]

            for x in snake_body[:-1]:
                if x == snake_head:
                    game_over = True

            self.draw_snake(snake_body)
            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, self.screen_size[0] - self.snake_size) / 20.0) * 20.0
                foody = round(random.randrange(0, self.screen_size[1] - self.snake_size) / 20.0) * 20.0
                length_of_snake += 1

            self.clock.tick(self.snake_speed)

        self.message("游戏结束", self.BLACK, [self.screen_size[0] / 6, self.screen_size[1] / 3])
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()


if __name__ == "__main__":
    SnakeGame()
