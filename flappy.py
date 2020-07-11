import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_X_pos, 590))
    screen.blit(floor_surface, (floor_X_pos + 450, 590))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,
                                                  random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700,
                                                  random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 750:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 590:
        falling_sound.play()
        return False

    return True

def rotated_bird(new_bird):
    new_bird = pygame.transform.rotozoom(new_bird, -bird_movement
                                         * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (225, 100))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f"Score: {int(score)}", True,(255, 255, 255))
        score_rect = score_surface.get_rect(center=(225, 160))
        screen.blit(score_surface, score_rect)


        high_score_surface = game_font.render(f"High Score:{int(high_score)}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(225,
                                                          210))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# Initializing pygame
pygame.init()

# Display measurement
display_width = 450
display_height = 750

screen = pygame.display.set_mode((display_width, display_height))

clock = pygame.time.Clock()

# Fonts
game_font = pygame.font.Font('freesansbold.ttf', 40)

# Game variables
gravity = 0.25
bird_movement = 0
game_active = True

# Score display
score = 0
high_score = 0

# Background image
bg_surface = pygame.image.load('background_night.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

# Floor image
floor_surface = pygame.image.load('base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_X_pos = 0

# Bird flapping image
bird_downflap = pygame.transform.scale2x(pygame.image.load(
    'bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load(
    'bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load(
    'bluebird-upflap.png').convert_alpha())

# Frames for flapping bird
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 312))

bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)


# Pipes
pipe_surface = pygame.image.load('pipe-red.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)

pipe_height = [400, 450, 500, 550, 600]

game_over_image = pygame.transform.scale2x(pygame.image.load(
    'get_ready.png').convert_alpha())
game_over_rect = game_over_image.get_rect(center = (225, 300))


flap_sound = pygame.mixer.Sound('sfx_wing.wav')
death_sound = pygame.mixer.Sound('sfx_hit.wav')
score_sound = pygame.mixer.Sound('sfx_point.wav')
falling_sound = pygame.mixer.Sound('sfx_die.wav')
score_sound_countdown = 100


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Key stroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 7.5
                #flap_sound.play()

            if event.key == pygame.K_UP and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 312)
                bird_movement = 0
                score = 0


        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            print(pipe_list)

        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
                bird_surface,bird_rect = bird_animation()


    screen.blit(bg_surface, (0, -285))


    # Activation of game
    if game_active:

        # Bird movement
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotation = rotated_bird(bird_surface)
        screen.blit(rotation, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1

        if score_sound_countdown <= 0:
            # score_sound.play()
            score_sound_countdown = 108

    else:

        # Game over message
        screen.blit(game_over_image, game_over_rect)
        score_display('game_over')
        high_score = update_score(score, high_score)

    # Floor
    floor_X_pos -= 1
    draw_floor()
    if floor_X_pos <= -450:
        floor_X_pos = 0

    # Increasing the speed of the floor
    if score > 10:
        floor_X_pos -= 4

    elif score > 20:
        floor_X_pos -= 8

    elif score > 30:
        floor_X_pos -= 12

    elif score > 40:
        floor_X_pos -= 15

    elif score > 50:
        floor_X_pos -= 18

    elif score > 60:
        floor_X_pos -= 20


    pygame.display.update()
    clock.tick(120)