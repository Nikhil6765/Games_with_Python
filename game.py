import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
lives = 3


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
projectiles = []
enemies = []

game_over = False  # flag to check if game is over

# define font
font = pygame.font.SysFont(None, 50)

# define "Start Game" button
start_button_rect = pygame.Rect(100, 100, 200, 50)
start_button_color = (255, 255, 255)
start_button_text = font.render("Start Game", True, (0, 0, 0))
start_button_text_rect = start_button_text.get_rect()
start_button_text_rect.center = start_button_rect.center


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # create a new projectile
                proj_pos = player_pos + pygame.Vector2(0, -50)
                proj_vel = pygame.Vector2(0, -800)
                projectiles.append({'pos': proj_pos, 'vel': proj_vel})
        
        elif event.type==pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                # reset game
                player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
                projectiles = []
                enemies = []
                game_over = False
                lives = 3  # reset number of lives


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # draw the player
    pygame.draw.circle(screen, "red", player_pos, 40)

    # draw "Start Game" button
    pygame.draw.rect(screen, start_button_color, start_button_rect)
    screen.blit(start_button_text, start_button_text_rect)

    # update and draw the projectiles
    for proj in projectiles:
        proj['pos'] += proj['vel'] * dt
        pygame.draw.circle(screen, "white", proj['pos'], 10)

        # check for collisions with enemies
        for enemy in enemies:
            if proj['pos'].distance_to(enemy['pos']) < 30:

                projectiles.remove(proj)
                enemies.remove(enemy)

    # update and draw the enemies
    for enemy in enemies:
        enemy['pos'] += enemy['vel'] * dt
        pygame.draw.circle(screen, "green", enemy['pos'], 30)
        
        # check for collision with player
        if enemy['pos'].distance_to(player_pos) < 70:
            game_over = True
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # spawn a new enemy every 3 seconds
    if pygame.time.get_ticks() % 3000 < dt * 1000 and not game_over:
        for i in range(3):
            enemy_pos = pygame.Vector2((i+1)*screen.get_width()/6, -50)
            enemy_vel = pygame.Vector2(0, 200)
            enemies.append({'pos': enemy_pos, 'vel': enemy_vel})

    # draw game over text if game over
    if game_over:
        font = pygame.font.SysFont(None, 100)
        text = font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, screen.get_height() / 2 - text.get_height() / 2))

    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
