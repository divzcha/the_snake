from abc import abstractmethod
from random import randint
import pygame
from typing import List, Tuple

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (255, 255, 255)

# Цвет яблока
APPLE_COLOR = (168, 228, 160)

# Цвет змейки
SNAKE_COLOR = (255, 192, 203)

# Скорость движения змейки:
SPEED = 14

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
# Объявление класса базового игрового объекта
class GameObject:
    """
    Базовый класс для всех игровых объектов.

    Предоставляет основные параметры и методы для управления положением
    и цветом объекта на игровом поле.
    """

    def __init__(self, position: Tuple[int, int] = (0, 0),
                 body_color: Tuple[int, int, int] = (0, 0, 0)):
        """
        Инициализация базового игрового объекта с указанием позиции и цвета.

        Аргументы:
            position (Tuple[int, int]): начальная позиция объекта
            на игровом поле (координаты x и y).
            body_color (Tuple[int, int, int]): RGB цвет объекта.
        """
        self.position: Tuple[int, int] = position
        self.body_color: Tuple[int, int, int] = body_color

    @abstractmethod
    def draw(self):
        """
        Метод для отрисовки объекта на экране.

        Должен быть переопределен в дочерних классах для
        специфической визуализации объекта.
        """
        pass


# Класс игрового объекта "Яблоко"
class Apple(GameObject):
    """
    Класс, представляющий яблоко в игре.

    Является подклассом GameObject и имеет методы для
    генерации случайной позиции и отрисовки на игровом поле.
    """

    def __init__(self):
        """
        Инициализация объекта "Яблоко" с заданным цветом и
        случайной позицией на игровом поле.
        """
        super().__init__(position=self.randomize_position(),
                         body_color=APPLE_COLOR)

    def randomize_position(self):
        """
        Генерация случайной позиции для яблока на игровом поле.

        Возвращает:
            Tuple[int, int]: новая случайная позиция яблока,
            кратная размеру сетки (GRID_SIZE).
        """
        while True:
            x_pos = randint(0, GRID_WIDTH - 1)
            y_pos = randint(0, GRID_HEIGHT - 1)
            new_position = (x_pos * GRID_SIZE, y_pos * GRID_SIZE)
            return new_position

    def draw(self):
        """
        Отрисовка объекта "Яблоко" на экране.

        Создает прямоугольник с цветом яблока и обводкой.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


# Класс игрового объекта "Змейка"
class Snake(GameObject):
    """
    Класс, представляющий змейку в игре.

    Содержит методы для управления движением, изменением длины,
    проверкой на столкновение и отрисовкой сегментов змейки.
    """

    def __init__(self):
        """
        Инициализация объекта "Змейка" с заданной позицией и цветом.

        Устанавливает начальные параметры, такие как длина змейки,
        направление движения и статус игры.
        """
        super().__init__(SCREEN_CENTER, SNAKE_COLOR)
        self.length: int = 1
        self.positions: List[Tuple[int, int]] = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.game_over = False
        self.speed = SPEED

    def update_direction(self):
        """
        Обновляет направление движения змейки на новое,
        если оно было установлено.


        Проверяет на корректность направления перед сменой.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def insert_next_position(self, next_position: Tuple[int, int]):
        """
        Добавляет новую позицию в начало списка позиций змейки.

        Аргументы:
            next_position (Tuple[int, int]): следующая позиция головы змейки.
        """
        self.position = next_position
        self.positions.insert(0, self.position)

    def remove_last_segment(self):
        """
        Удаляет последний сегмент из списка позиций змейки,
        если ее длина больше текущей.

        Обеспечивает нужную длину змейки на экране.
        """
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def is_snake_dead(self, next_position: Tuple[int, int]):
        """
        Проверяет, не произошло ли столкновение змейки с самой собой.

        Если да, устанавливает статус game_over в True.

        Аргументы:
            next_position (Tuple[int, int]): следующая позиция головы змейки.
        """
        if next_position in self.positions[2:]:
            self.game_over = True

    def move(self):
        """
        Обновляет позицию головы змейки, вычисляя следующую позицию
        на основании текущего направления.

        Возвращает:
            Tuple[int, int]: новая позиция головы змейки
            с учетом границ экрана (цикличное перемещение).
        """
        self.update_direction()
        x, y = self.position
        dx, dy = self.direction
        new_x = (x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        next_position = (new_x, new_y)
        return next_position

    def draw(self):
        """
        Отрисовка сегментов змейки на экране.

        Создает и отрисовывает прямоугольники для каждого сегмента,
        а также затирает последний сегмент.
        """
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """
        Возвращает текущую позицию головы змейки.

        Возвращает:
            Tuple[int, int]: позиция головы змейки.
        """
        return self.positions[0]

    def reset(self):
        """
        Сбрасывает параметры змейки к исходным после столкновения,
        включая позицию и длину.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None
        self.position = SCREEN_CENTER


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш для управления направлением движения змейки.

    Аргументы:
        game_object (Snake): объект змейки, для которого обрабатываются
        клавиши.


    Возвращает:
        bool: False, если закрытие окна, иначе True для продолжения игры.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif (event.key == pygame.K_LEFT
                  and game_object.direction != RIGHT):
                game_object.next_direction = LEFT
            elif (event.key == pygame.K_RIGHT
                  and game_object.direction != LEFT):
                game_object.next_direction = RIGHT
            elif (event.key == pygame.K_ESCAPE):
                pygame.quit()

    return True


def main():
    """
    Основной цикл игры.

    Создает экземпляры змейки и яблока, инициализирует игровой цикл,
    проверяет на столкновения и обновляет экран.
    """
    # Инициализация PyGame и создание объектов
    pygame.init()
    snake = Snake()
    apple = Apple()
    game = True

    record = 0

    while game:
        clock.tick(snake.speed)
        screen.fill(BOARD_BACKGROUND_COLOR)
        game = handle_keys(snake)

        # Движение змейки и проверка на столкновение
        next_position = snake.move()
        snake.is_snake_dead(next_position)
        snake.insert_next_position(next_position)
        snake.remove_last_segment()

        # Проверка на поедание яблока
        if snake.position == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

        # Отрисовка объектов на экране
        snake.draw()
        apple.draw()

        pygame.display.update()

        pygame.display.set_caption(f'Змейка | Рекорд: {record}')

        # Сброс игры после столкновения
        if snake.game_over:
            if (snake.length > record):
                record = snake.length

            snake.reset()
            snake.game_over = False


if __name__ == '__main__':
    main()
