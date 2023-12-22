import pygame
import os
import sys
import


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 60
        self.maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        # self.set_view()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def start_screen(self):
        intro_text = ["КоBun"]

        fon = pygame.transform.scale(load_image('kobun.png'), (600, 600))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate(self)
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            clock.tick(50)

    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                if self.maze[row][col] == 0:
                    color = pygame.Color('black')
                else:
                    color = pygame.Color('green')
                pygame.draw.rect(screen, color, (
                    self.cell_size * col, self.cell_size * row, self.cell_size, self.cell_size))
        # self.set_view()


if __name__ == '__main__':
    pygame.init()
    w, h = 600, 600
    size = width, height = w, h
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    b = Maze(10, 10)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                b.start_screen()
        b.render(screen)
        # b.render(screen)
        pygame.display.flip()
    pygame.quit()
