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
    print_map(game_map)


def type2():
    import random

    # Размеры карты
    WIDTH = 100
    HEIGHT = 100

    # Символы
    WALL = 'x'
    SPACE = ' '
    EXIT = 'E'
    BULLET = 'p'  # Патрон
    ENEMY_NORMAL = 'h'  # Обычный враг
    ENEMY_STRONG = 's'  # Сильный враг

    # Минимальные и максимальные размеры комнат
    MIN_ROOM_SIZE = 5
    MAX_ROOM_SIZE = 15

    # Количество комнат
    NUM_ROOMS = 30

    # Количество патронов и врагов в каждой комнате
    MIN_BULLETS = 1
    MAX_BULLETS = 5
    MIN_ENEMIES = 1
    MAX_ENEMIES = 3

    # Генерация карты с маленькими комнатами и объектами
    def generate_map(width, height):
        # Создаем пустую карту, заполненную стенами
        game_map = [[WALL for _ in range(width)] for _ in range(height)]

        rooms = []

        # Функция для создания комнаты
        def create_room(x, y, w, h):
            for i in range(x, x + w):
                for j in range(y, y + h):
                    if 0 < i < width - 1 and 0 < j < height - 1:
                        game_map[j][i] = SPACE

        # Функция для создания туннеля между двумя точками
        def create_corridor(x1, y1, x2, y2):
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    game_map[y][x1] = SPACE
            elif y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    game_map[y1][x] = SPACE
            else:
                # Проводим сначала горизонтальный туннель
                if x1 > x2:
                    x1, x2 = x2, x1
                for x in range(x1, x2 + 1):
                    game_map[y1][x] = SPACE
                # Затем вертикальный туннель
                if y1 > y2:
                    y1, y2 = y2, y1
                for y in range(y1, y2 + 1):
                    game_map[y][x2] = SPACE

        # Функция для размещения патронов и врагов внутри комнаты
        def populate_room(room_x, room_y, room_w, room_h):
            # Размещение патронов (p)
            num_bullets = random.randint(MIN_BULLETS, MAX_BULLETS)
            for _ in range(num_bullets):
                bx = random.randint(room_x + 1, room_x + room_w - 2)
                by = random.randint(room_y + 1, room_y + room_h - 2)
                game_map[by][bx] = BULLET

            # Размещение врагов (h и s)
            num_enemies = random.randint(MIN_ENEMIES, MAX_ENEMIES)
            for _ in range(num_enemies):
                ex = random.randint(room_x + 1, room_x + room_w - 2)
                ey = random.randint(room_y + 1, room_y + room_h - 2)
                enemy_type = random.choice([ENEMY_NORMAL, ENEMY_STRONG])
                game_map[ey][ex] = enemy_type

        # Функция для размещения сильных врагов на стенах
        def place_strong_enemies():
            for y in range(height):
                for x in range(width):
                    if game_map[y][x] == WALL:
                        if random.random() < 0.1:  # Вероятность появления сильного врага на стене
                            game_map[y][x] = ENEMY_STRONG

        # Генерация случайных комнат
        for _ in range(NUM_ROOMS):
            room_width = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
            room_height = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
            room_x = random.randint(1, width - room_width - 1)
            room_y = random.randint(1, height - room_height - 1)

            create_room(room_x, room_y, room_width, room_height)
            rooms.append((room_x, room_y, room_width, room_height))

            # Заполняем комнату патронами и врагами
            populate_room(room_x, room_y, room_width, room_height)

        # Связывание комнат случайными туннелями
        for i in range(1, len(rooms)):
            x1, y1, _, _ = rooms[i - 1]
            x2, y2, _, _ = rooms[i]
            create_corridor(x1 + random.randint(1, 3), y1 + random.randint(1, 3), x2 + random.randint(1, 3),
                            y2 + random.randint(1, 3))

        # Размещение сильных врагов на стенах
        place_strong_enemies()

        # Генерация случайного выхода в одной из комнат
        exit_room = random.choice(rooms)
        exit_x = random.randint(exit_room[0] + 1, exit_room[0] + exit_room[2] - 2)
        exit_y = random.randint(exit_room[1] + 1, exit_room[1] + exit_room[3] - 2)

        game_map[exit_y][exit_x] = EXIT

        return game_map

    # Функция для отображения карты
    def print_map(game_map):
        for row in game_map:
            print(''.join(row))

    # Генерация карты
    game_map = generate_map(WIDTH, HEIGHT)

    # Выводим карту в консоль (это может занять много времени на больших картах)
    print_map(game_map)

def type3():
    # Размеры карты
    WIDTH = 100
    HEIGHT = 100

    # Символы
    WALL = 'x'
    SPACE = ' '
    EXIT = 'E'

    # Количество шагов
    MAX_STEPS = 30000

    # Генерация карты с помощью случайного блуждания
    def generate_map(width, height):
        # Создаем пустую карту, заполненную стенами
        game_map = [[WALL for _ in range(width)] for _ in range(height)]

        # Стартовая точка
        start_x, start_y = width // 2, height // 2
        game_map[start_y][start_x] = SPACE

        # Направления для движения (вверх, вниз, влево, вправо)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Начинаем случайное блуждание
        current_x, current_y = start_x, start_y
        steps = 0

        while steps < MAX_STEPS:
            # Выбираем случайное направление
            dx, dy = random.choice(directions)
            new_x, new_y = current_x + dx, current_y + dy

            # Проверяем, чтобы новая позиция была в пределах карты
            if 0 < new_x < width - 1 and 0 < new_y < height - 1:
                game_map[new_y][new_x] = SPACE  # Проводим путь

                # Обновляем текущую позицию
                current_x, current_y = new_x, new_y

            steps += 1

        # Создаем случайный выход на карте
        exit_x, exit_y = random.randint(1, width - 2), random.randint(1, height - 2)
        while game_map[exit_y][exit_x] != SPACE:
            exit_x, exit_y = random.randint(1, width - 2), random.randint(1, height - 2)

        game_map[exit_y][exit_x] = EXIT

        return game_map

    # Функция для отображения карты
    def print_map(game_map):
        for row in game_map:
            print(''.join(row))

    # Генерация карты
    game_map = generate_map(WIDTH, HEIGHT)

    # Выводим карту в консоль (это может занять много времени на больших картах)
    print_map(game_map)


type1()