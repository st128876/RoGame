import random

def type1():
    # Размеры карты
    import random

    # Размеры карты
    WIDTH = 50
    HEIGHT = 50

    # Символы
    WALL = 'x'
    SPACE = ' '
    EXIT = 'E'

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

        # Выбираем случайную клетку для выхода
        exit_x, exit_y = random.randint(1, width - 2), random.randint(1, height - 2)

        # Пока эта клетка не является частью пути, выбираем другую
        while game_map[exit_y][exit_x] != SPACE:
            exit_x, exit_y = random.randint(1, width - 2), random.randint(1, height - 2)

        # Обозначаем выход
        game_map[exit_y][exit_x] = EXIT

        return game_map

    # Функция для отображения карты
    def print_map(game_map):
        for row in game_map:
            print(''.join(row))

    # Генерация карты
    game_map = generate_map(WIDTH, HEIGHT)
    game_map[0][0] = ' '

    # Выводим карту в консоль (это может занять много времени на больших картах)
    # print_map(game_map)
    return game_map
