import pygame

pygame.init()
clock = pygame.time.Clock()
screenw = 800
screenh = 600
screen = pygame.display.set_mode((screenw, screenh))

done = False
lives = 3
game_loss = False
game_win = False

# платформа
plat_width = 150
plat_height = 20
plat_x = screenw/2 - plat_width/2
plat_y = screenh - plat_height - 10

# мяч
ball_radius = 20
ball_x = screenw/2 - ball_radius/2
ball_y = screenh/2 - ball_radius/2
ball_speed_x = 0
ball_speed_y = 0
ball_done = False

# блоки
block_rows = 5
block_cols = 8
block_width = 86
block_height = 30

blocks = []
for i in range(block_rows):
    for j in range(block_cols):
        block_x = j * (block_width + 10) + 20
        block_y = i * (block_height + 10) + 20
        blocks.append(pygame.Rect(block_x, block_y, block_width, block_height))


# жизни
def draw_lives():
    font = pygame.font.SysFont(None, 30)
    screen.blit(font.render(f"Жизни: {lives}", True, (255, 0, 0)), (10, 10))

# конец игры
def show_message(message):
    font = pygame.font.SysFont(None, 50)
    screen.fill((0, 0, 0))
    text = font.render(message, True, (255, 0, 0))
    screen.blit(text, (screenw / 2 - text.get_width() / 2, screenh / 2 - text.get_height() / 2))
    pygame.display.flip()
    pygame.time.wait(4000)


while not done:
    clock.tick(60)
    if game_loss:
        show_message("Проигрыш")
        break

    if game_win:
        show_message("Победа")
        break

    screen.fill((253, 106, 2))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # платформа
    pygame.draw.rect(screen, (0,255,255), pygame.Rect(plat_x, plat_y, plat_width, plat_height))

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        plat_x -= 6
        if not ball_done:
            ball_speed_x = 2
            ball_speed_y = -2
            ball_done = True
    if pressed[pygame.K_RIGHT]:
        plat_x += 6
        if not ball_done:
            ball_speed_x = 2
            ball_speed_y = -2
            ball_done = True

    if plat_x < 0:
        plat_x = 0
    elif plat_x > screenw - plat_width:
        plat_x = screenw - plat_width

    if not ball_done:
        ball_x = screenw / 2 - ball_radius / 2
        ball_y = screenh / 2 - ball_radius / 2

    # блоки
    for block in blocks:
        pygame.draw.rect(screen, (0, 255, 0), block)
    if len(blocks) == 0:
        game_win = True

    # мяч
    pygame.draw.circle(screen, (0, 128, 255), (ball_x,ball_y),ball_radius)

    if ball_done:
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # отскакивание от границ
        if ball_x < ball_radius or ball_x + ball_radius > screenw:
            ball_speed_x = -ball_speed_x
        if ball_y < ball_radius:
            ball_speed_y = -ball_speed_y

        # отскакивание от платформы
        if ball_y + ball_radius > plat_y and plat_x < ball_x < plat_x + plat_width:
            ball_speed_y = -ball_speed_y
            ball_x = max(plat_x, min(ball_x, plat_x + plat_width))

        # отскакивание от блоков
        for block in blocks:
            if ((ball_x - max(block.left, min(ball_x, block.right)))**2 + (ball_y -max(block.top, min(ball_y, block.bottom)))**2) < (ball_radius**2):
                ball_speed_y = -ball_speed_y
                blocks.remove(block)
                break

        if ball_y > screenh:
            lives -= 1
            if lives == 0:
                game_loss = True
            else:
                ball_done = False
                ball_x = screenw / 2 - ball_radius / 2
                ball_y = screenh / 2 - ball_radius / 2
                ball_speed_x = 0
                ball_speed_y = 0

    draw_lives()
    pygame.display.flip()