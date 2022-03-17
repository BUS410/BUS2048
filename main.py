import pygame


class Game:
    fps = 60
    screen_width = 500
    screen_height = 500

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.SCALED)
        self.running = True
        self.clock = pygame.time.Clock()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.window.fill((0, 0, 0))
        pygame.display.flip()

    def run(self):
        while self.running:
            self.update()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    Game().run()
