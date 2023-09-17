import pygame
import random

# Ініціалізація Pygame
pygame.init()


# Параметри вікна
width, height = 400, 600
background_image = pygame.transform.scale(pygame.image.load("background.png"), (width, height))
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Гра на Pygame")

# Колір фону
bg_color = (0, 0, 0)

# Головний корабель гравця
player_color = (0, 255, 0)
player_width, player_height = 50, 100
player_x = width // 2 - player_width // 2
player_y = height - player_height * 2
player_speed = 5

player_image = pygame.transform.scale(pygame.image.load("car.png"), (player_width, player_height))
enemy_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("enemy.png"), (player_width * 2, player_height)), 180)


# Ворожі кораблі
enemy_color = (255, 0, 0)
enemy_width, enemy_height = 50, 50
enemy_x = random.randint(0, width - enemy_width)
enemy_y = 0
enemy_speed = 3

# Вибухи
explosion_color = (255, 255, 0)
explosions = []


# Функція для виводу тексту
def draw_text(text, x, y):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (255, 255, 255))
    win.blit(text_surface, (x, y))


# Головний цикл гри
running = True
score = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Керування гравцем
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_width:
        player_x += player_speed

    # Рух ворожих кораблів
    enemy_y += enemy_speed

    # Перевірка зіткнення гравця з ворожим кораблем
    if (
            player_x < enemy_x + enemy_width and
            player_x + player_width > enemy_x and
            player_y < enemy_y + enemy_height and
            player_y + player_height > enemy_y
    ):
        running = False

    # Перевірка зіткнень ворожих кораблів з вибухами
    for explosion in explosions:
        if (
                explosion[0] < enemy_x + enemy_width and
                explosion[0] + enemy_width > enemy_x and
                explosion[1] < enemy_y + enemy_height and
                explosion[1] + enemy_height > enemy_y
        ):
            explosions.remove(explosion)
            score += 1
            enemy_x = random.randint(0, width - enemy_width)
            enemy_y = 0

    # Видалення вибухів, які вийшли за межі екрану
    explosions = [explosion for explosion in explosions if explosion[1] < height]

    # Створення нових вибухів
    if enemy_y >= height:
        enemy_x = random.randint(0, width - enemy_width)
        enemy_y = 0

    # Оновлення вікна
    win.blit(background_image, (0, 0))
    win.blit(player_image, (player_x, player_y))
    win.blit(enemy_image, (enemy_x, enemy_y))

    for explosion in explosions:
        pygame.draw.rect(win, explosion_color, (explosion[0], explosion[1], enemy_width, enemy_height))

    draw_text(f"Score: {score}", 10, 10)
    pygame.display.update()

# Завершення гри
pygame.quit()
