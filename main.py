import random

import numpy as np
import pygame


class Cell(pygame.sprite.Sprite):

    def __init__(self, x, y, size, font: pygame.font.Font):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.image = pygame.surface.Surface((size, size))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.border_size = self.rect.width // 25
        self.value = 0

    def update(self):
        self.image.fill((128, 255, 128))
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, *self.rect.size), self.border_size)
        if self.value:
            text = self.font.render(str(self.value), True, (255, 255, 255))
            self.image.blit(text, (self.rect.width / 2 - text.get_width() / 2,
                                   self.rect.height / 2 - text.get_height() / 2))


class Field(pygame.sprite.Group):

    def __init__(self, width, height, size, font: pygame.font.Font):
        pygame.sprite.Group.__init__(self)
        self.width, self.height = width, height
        self.size = size
        self.cell_size = width / size
        self.matrix = np.array(
            [np.array(
                [Cell(x * self.cell_size, y * self.cell_size, self.cell_size, font) for x in range(size)]
            ) for y in range(size)]
        )
        self.add_new_number()
        self.add_new_number()
        for line in self.matrix:
            for cell in line:
                cell.update()
                self.add(cell)

    def add_new_number(self):
        while True:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.matrix[y][x].value == 0:
                self.matrix[y][x].value = 2
                return

    def move_to_up(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.matrix[y][x].value == 0:
                    continue
                for i in range(0, y):
                    if self.matrix[i][x].value == 0:
                        self.matrix[i][x].value = self.matrix[y][x].value
                        self.matrix[y][x].value = 0
                    elif self.matrix[y][x].value == self.matrix[i][x].value:
                        self.matrix[i][x].value = self.matrix[y][x].value * 2
                        self.matrix[y][x].value = 0
                    else:
                        continue
                    break

    def move_to_bottom(self):
        for y in range(self.size-1, -1, -1):
            for x in range(self.size):
                if self.matrix[y][x].value == 0:
                    continue
                for i in range(self.size-1, y, -1):
                    if self.matrix[i][x].value == 0:
                        self.matrix[i][x].value = self.matrix[y][x].value
                        self.matrix[y][x].value = 0
                    elif self.matrix[y][x].value == self.matrix[i][x].value:
                        self.matrix[i][x].value = self.matrix[y][x].value * 2
                        self.matrix[y][x].value = 0
                    else:
                        continue
                    break

    def move_to_left(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.matrix[y][x].value == 0:
                    continue
                for i in range(0, x):
                    if self.matrix[y][i].value == 0:
                        self.matrix[y][i].value = self.matrix[y][x].value
                        self.matrix[y][x].value = 0
                    elif self.matrix[y][x].value == self.matrix[y][i].value:
                        self.matrix[y][i].value = self.matrix[y][x].value * 2
                        self.matrix[y][x].value = 0
                    else:
                        continue
                    break

    def move_to_right(self):
        for y in range(self.size):
            for x in range(self.size-1, -1, -1):
                if self.matrix[y][x].value == 0:
                    continue
                for i in range(self.size-1, x, -1):
                    if self.matrix[y][i].value == 0:
                        self.matrix[y][i].value = self.matrix[y][x].value
                        self.matrix[y][x].value = 0
                    elif self.matrix[y][x].value == self.matrix[y][i].value:
                        self.matrix[y][i].value = self.matrix[y][x].value * 2
                        self.matrix[y][x].value = 0
                    else:
                        continue
                    break


class Game:
    fps = 60
    screen_width = 500
    screen_height = 500

    def __init__(self, size):
        pygame.init()
        pygame.display.set_caption('BUS2048')
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.running = True
        self.clock = pygame.time.Clock()
        font = pygame.font.SysFont('consolas', int(self.screen_height / size / 2), True)
        self.field = Field(self.screen_width, self.screen_height, size, font)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.field.move_to_up()
                elif event.key == pygame.K_DOWN:
                    self.field.move_to_bottom()
                elif event.key == pygame.K_LEFT:
                    self.field.move_to_left()
                elif event.key == pygame.K_RIGHT:
                    self.field.move_to_right()
                else:
                    continue
                self.field.add_new_number()
                self.field.update()


        self.window.fill((255, 255, 255))
        self.field.draw(self.window)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.update()
            self.clock.tick(self.fps)
        pygame.quit()


if __name__ == '__main__':
    Game(4).run()
