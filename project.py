import pygame
import os
import sys

FPS = 50


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


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('bush.jpg'),
    'empty': load_image('earth.jpg')
}
player_image = load_image('hleb.png')

tile_width = tile_height = 50


class Maze(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.x, self.y = pos_x, pos_y
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 3, tile_height * pos_y + 3)


player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Maze('empty', x, y)
            elif level[y][x] == '#':
                Maze('wall', x, y)
            elif level[y][x] == '@':
                Maze('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    start_screen()
    level = load_level('level.txt')
    player, level_x, level_y = generate_level(level)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if level[player.y][player.x - 1] != '#':
                        player.rect.x -= 50
                        player.x -= 1
                if event.key == pygame.K_RIGHT:
                    if level[player.y][player.x + 1] != '#':
                        player.rect.x += 50
                        player.x += 1
                if event.key == pygame.K_UP:
                    if level[player.y - 1][player.x] != '#':
                        player.rect.y -= 50
                        player.y -= 1
                if event.key == pygame.K_DOWN:
                    if level[player.y + 1][player.x] != '#':
                        player.rect.y += 50
                        player.y += 1
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        all_sprites.update()
        pygame.display.flip()
    pygame.quit()
