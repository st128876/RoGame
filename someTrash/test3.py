import random

# Размеры карты
WIDTH = 100
HEIGHT = 100

# Символы
WALL = 'x'
SPACE = ' '
EXIT = 'E'

# Минимальные и максимальные размеры комнат
MIN_ROOM_SIZE = 5
MAX_ROOM_SIZE = 15

# Количество комнат
NUM_ROOMS = 25


# Генерация карты с маленькими комнатами
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

    # Генерация случайных комнат
    for _ in range(NUM_ROOMS):
        room_width = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        room_height = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        room_x = random.randint(1, width - room_width - 1)
        room_y = random.randint(1, height - room_height - 1)

        create_room(room_x, room_y, room_width, room_height)
        rooms.append((room_x, room_y, room_width, room_height))

    # Связывание комнат случайными туннелями
    for i in range(1, len(rooms)):
        x1, y1, _, _ = rooms[i - 1]
        x2, y2, _, _ = rooms[i]
        create_corridor(x1 + random.randint(1, 3), y1 + random.randint(1, 3), x2 + random.randint(1, 3),
                        y2 + random.randint(1, 3))

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