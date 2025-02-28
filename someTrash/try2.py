import random

# Размеры карты
WIDTH = 60
HEIGHT = 70

# Символы
WALL = 'x'
SPACE = ' '

# Направления для генерации коридоров
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # вниз, вправо, вверх, влево

# Функция для создания карты
def generate_map(width, height):
    # Создаем начальную карту, заполненную стенами
    game_map = [[WALL for _ in range(width)] for _ in range(height)]

    # Начальная точка для генерации пути
    start_x, start_y = random.randint(1, width - 2), random.randint(1, height - 2)
    game_map[start_y][start_x] = SPACE

    # Список для хранения координат текущего пути
    path = [(start_x, start_y)]

    # Генерация путей
    while path:
        x, y = path[-1]
        possible_directions = []

        # Проверяем все направления
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 < nx < width - 1 and 0 < ny < height - 1 and game_map[ny][nx] == WALL:
                possible_directions.append((dx, dy))

        if possible_directions:
            # Выбираем случайное направление
            dx, dy = random.choice(possible_directions)
            nx, ny = x + dx * 2, y + dy * 2

            # Создаем коридор
            game_map[ny][nx] = SPACE
            game_map[y + dy][x + dx] = SPACE
            path.append((nx, ny))
        else:
            # Если нет доступных направлений, возвращаемся назад
            path.pop()

    return game_map

# Функция для отображения карты
def print_map(game_map):
    for row in game_map:
        print(''.join(row))

# Генерация карты
game_map = generate_map(WIDTH, HEIGHT)

# Выводим карту в консоль (это может занять много времени на больших картах)
print_map(game_map)