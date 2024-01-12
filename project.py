import pygame
import os
import sys
from random import choice

FPS = 60
RES = WIDTH, HEIGHT = 723, 723
TILE = 40
cols, rows = WIDTH // TILE, HEIGHT // TILE
color = (102, 0, 0)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["КоBun"]
    fon = pygame.transform.scale(load_image('кобан2D.png'), (WIDTH, HEIGHT))
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
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = 4

    def draw(self, sc):
        x, y = self.x * TILE, self.y * TILE

        if self.walls['top']:
            pygame.draw.line(sc, color, (x, y), (x + TILE, y), self.thickness)
        if self.walls['right']:
            pygame.draw.line(sc, color, (x + TILE, y), (x + TILE, y + TILE), self.thickness)
        if self.walls['bottom']:
            pygame.draw.line(sc, color, (x + TILE, y + TILE), (x, y + TILE), self.thickness)
        if self.walls['left']:
            pygame.draw.line(sc, color, (x, y + TILE), (x, y), self.thickness)

    def get_rects(self):
        rects = []
        x, y = self.x * TILE, self.y * TILE
        if self.walls['top']:
            rects.append(pygame.Rect((x, y), (TILE, self.thickness)))
        if self.walls['right']:
            rects.append(pygame.Rect((x + TILE, y), (self.thickness, TILE)))
        if self.walls['bottom']:
            rects.append(pygame.Rect((x, y + TILE), (TILE, self.thickness)))
        if self.walls['left']:
            rects.append(pygame.Rect((x, y), (self.thickness, TILE)))
        return rects

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return self.grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        if neighbors:
            return choice(neighbors)
        else:
            return False


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False


def generate_maze():
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    array = []
    break_count = 1

    while break_count != len(grid_cells):
        current_cell.visited = True
        next_cell = current_cell.check_neighbors(grid_cells)
        if next_cell:
            next_cell.visited = True
            break_count += 1
            array.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif array:
            current_cell = array.pop()
    return grid_cells


def is_collide(x, y):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True


def is_game_over():
    pass


game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# use images
fon_maze = load_image('grass.jpg')

# get maze
maze = generate_maze()

Exit = load_image('exit.png').convert_alpha()
Exit = pygame.transform.scale(Exit, (TILE - 1 * maze[0].thickness, TILE - 1 * maze[0].thickness))

# player settings
player_speed = 6
player_img = load_image('hleb.png')
player_img = pygame.transform.scale(player_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
player_rect = player_img.get_rect()
player_rect.center = TILE // 2, TILE // 2
directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)}
keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
direction = (0, 0)

# collision list
walls_collide_list = sum([cell.get_rects() for cell in maze], [])

if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT = 723, 723
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    start_screen()
    while True:
        surface.blit(game_surface, (0, 0))
        game_surface.blit(fon_maze, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if player_rect[0] >= WIDTH - 55 and player_rect[1] >= HEIGHT - 55:
                print("YES")
                pygame.quit()

        # controls and movement
        pressed_key = pygame.key.get_pressed()
        for key, key_value in keys.items():
            if pressed_key[key_value] and not is_collide(*directions[key]):
                direction = directions[key]
                break
        if not is_collide(*direction):
            player_rect.move_ip(direction)

        # draw maze
        [cell.draw(game_surface) for cell in maze]

        # draw player
        game_surface.blit(player_img, player_rect)
        game_surface.blit(Exit, (WIDTH - 40, HEIGHT - 40))
        pygame.display.flip()
        clock.tick(FPS)
