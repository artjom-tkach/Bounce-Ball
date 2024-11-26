import pygame
import random

# Инициализация pygame
pygame.init()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Размер окна
WIDTH = 800
HEIGHT = 600

# Настройки окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bounce Ball")

# Функция для перезапуска игры
def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, platform_x, score, game_over
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = random.choice([-5, 5])
    ball_dy = random.choice([-5, 5])
    platform_x = WIDTH // 2 - platform_width // 2
    score = 0
    game_over = False

# Настройки мяча
ball_radius = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = random.choice([-5, 5])  # Начальная скорость по оси X
ball_dy = random.choice([-5, 5])  # Начальная скорость по оси Y

# Настройки платформы
platform_width = 100
platform_height = 20
platform_x = WIDTH // 2 - platform_width // 2
platform_y = HEIGHT - platform_height - 10
platform_speed = 10

# Счетчик отскоков
score = 0

# Шрифт для вывода счета
font = pygame.font.SysFont('Arial', 30)

# Шрифт для вывода сообщения Game Over и кнопки Try Again
game_over_font = pygame.font.SysFont('Arial', 50)
button_font = pygame.font.SysFont('Arial', 40)

# Частота обновлений экрана
clock = pygame.time.Clock()

# Переменные для отслеживания состояния игры
running = True
game_over = False

# Основной игровой цикл
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            # Проверка на клик по кнопке Try Again
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if try_again_button.collidepoint(mouse_x, mouse_y):
                reset_game()

    if not game_over:
        # Управление платформой (влево/вправ)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and platform_x > 0:
            platform_x -= platform_speed
        if keys[pygame.K_RIGHT] and platform_x < WIDTH - platform_width:
            platform_x += platform_speed

        # Движение мяча
        ball_x += ball_dx
        ball_y += ball_dy

        # Отскок от стен
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
            ball_dx = -ball_dx  # Меняем направление по оси X
        if ball_y - ball_radius <= 0:
            ball_dy = -ball_dy  # Меняем направление по оси Y (от верхней стены)

        # Отскок от платформы
        if (platform_x <= ball_x <= platform_x + platform_width) and (ball_y + ball_radius >= platform_y):
            ball_dy = -ball_dy  # Меняем направление мяча по оси Y
            score += 1  # Увеличиваем счетчик при отскоке от платформы
            # Увеличиваем скорость мяча
            ball_dx = ball_dx * 1.05 if ball_dx > 0 else ball_dx * 1.05
            ball_dy = ball_dy * 1.05 if ball_dy > 0 else ball_dy * 1.05

        # Отскок от нижней стены (если мяч упал вниз)
        if ball_y + ball_radius >= HEIGHT:
            game_over = True  # Устанавливаем флаг Game Over
            final_score = score  # Сохраняем финальный счет

        # Заполнение экрана черным цветом
        screen.fill(BLACK)

        # Рисуем мяч
        pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

        # Рисуем платформу
        pygame.draw.rect(screen, BLUE, (platform_x, platform_y, platform_width, platform_height))

        # Отображаем счет на экране
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    else:
        # Отображение сообщения Game Over
        game_over_text = game_over_font.render("Game Over", True, WHITE)
        score_text = game_over_font.render(f"Score: {final_score}", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))

        # Создание кнопки "Try Again"
        try_again_text = button_font.render("Try Again", True, WHITE)
        try_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(screen, GREEN, try_again_button)  # Кнопка
        screen.blit(try_again_text, (WIDTH // 2 - try_again_text.get_width() // 2, HEIGHT // 2 + 60))

    # Обновление экрана
    pygame.display.flip()

    # Устанавливаем частоту обновлений экрана
    clock.tick(60)

# Завершаем работу pygame
pygame.quit()
