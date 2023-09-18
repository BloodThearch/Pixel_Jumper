import pygame
from sys import exit
from random import randint

pygame.init()
game_active = False
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Pixel Jumper")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Minecraft.ttf", 50)

# Asset Objects
sky_surface = pygame.image.load("graphics/sky.jpg").convert()
sky_surface = pygame.transform.rotozoom(sky_surface,0,0.5)

ground_surface = pygame.image.load("graphics/ground.png").convert()
ground_surface = pygame.transform.rotozoom(ground_surface,0,0.3)
ground_rect = ground_surface.get_rect(topleft = (0,300))

obstacle_rect_list = []

slime_surface = pygame.image.load("graphics/slime.png").convert_alpha()
slime_surface = pygame.transform.rotozoom(slime_surface, 0, 2)

bird_surface = pygame.image.load("graphics/bird.png").convert_alpha()
bird_surface = pygame.transform.rotozoom(bird_surface, 0, 2)

player_run_0 = pygame.image.load("graphics/player/run/00.png").convert_alpha()
player_run_1 = pygame.image.load("graphics/player/run/01.png").convert_alpha()
player_run_2 = pygame.image.load("graphics/player/run/02.png").convert_alpha()
player_run_3 = pygame.image.load("graphics/player/run/03.png").convert_alpha()
player_run_4 = pygame.image.load("graphics/player/run/04.png").convert_alpha()
player_run_5 = pygame.image.load("graphics/player/run/05.png").convert_alpha()
player_run = [
    pygame.transform.rotozoom(player_run_0, 0, 2),
    pygame.transform.rotozoom(player_run_1, 0, 2),
    pygame.transform.rotozoom(player_run_2, 0, 2),
    pygame.transform.rotozoom(player_run_3, 0, 2),
    pygame.transform.rotozoom(player_run_4, 0, 2),
    pygame.transform.rotozoom(player_run_5, 0, 2),
]
player_run_idx = 0
player_jump = pygame.image.load("graphics/player/jump/00.png").convert_alpha()
player_jump = pygame.transform.rotozoom(player_jump, 0, 2)
player_surface = player_run[player_run_idx]
player_surface = pygame.transform.rotozoom(player_surface, 0, 2)
player_rect = player_surface.get_rect(midbottom = (100,300))

player_hitbox = pygame.transform.rotozoom(pygame.image.load("graphics/player.png").convert_alpha(),0,2).get_rect(midbottom = player_rect.center)

player_surface2 = pygame.image.load("graphics/player.png").convert_alpha()
player_surface2 = pygame.transform.rotozoom(player_surface2, 0, 2)
player_rect2 = player_surface2.get_rect(center = (400,200))

welcome_text_surf = test_font.render("Welcome to Pixel Jumper!", False, "Black")
welcome_text_rect = welcome_text_surf.get_rect(midtop = (400,20))

instruction_text_surf = test_font.render("Press <SPACE> to START and JUMP", False, "Black")
instruction_text_surf = pygame.transform.rotozoom(instruction_text_surf, 0, 0.5)
instruction_text_rect = instruction_text_surf.get_rect(midbottom = (400,380))

# last_score_text_surf = test_font.render(f"Last Score: 0", False, "Black")
# last_score_text_surf = pygame.transform.rotozoom(last_score_text_surf,0,0.5)
# last_score_text_rect = last_score_text_surf.get_rect(midbottom = (400,320))

# Variables
player_gravity = 0
start_time = 0
score = 0
last_tick = 0
blink = True

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Set before game opens
player_hitbox.bottom = ground_rect.top
player_rect.center = player_hitbox.center

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf = test_font.render(f"Score: {int(current_time/1000)}", False, (64,64,64))
    score_rect = score_surf.get_rect(midtop = (400,20))
    screen.blit(score_surf,score_rect)
    return int(current_time/1000)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(slime_surface, obstacle_rect)
            else:
                screen.blit(bird_surface, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.right>0]
        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surface, player_run_idx

    if player_hitbox.bottom < 300:
        player_surface = player_jump
    else:
        player_run_idx += 0.1
        if int(player_run_idx) >= len(player_run): player_run_idx = 0
        player_surface = player_run[int(player_run_idx)]

while True:
    # keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if game_active:
                if event.key == pygame.K_SPACE and player_hitbox.bottom>=ground_rect.top:
                    player_gravity=-20
            else:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    # slime_rect.left = 800
                    obstacle_rect_list = []
                    player_hitbox.bottom = ground_rect.top
                    player_gravity = 0
                    start_time = pygame.time.get_ticks()
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(slime_surface.get_rect(midbottom = (randint(900,1100),300)))
            else:
                obstacle_rect_list.append(bird_surface.get_rect(midbottom = (randint(900,1100), 200)))

    if game_active:
        # Draw
        # Environment
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, ground_rect)
        screen.blit(ground_surface, ground_rect.topright)
        screen.blit(ground_surface, (ground_rect.right*2,ground_rect.top))
        score = display_score()
        # Beings + functionality
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        # Player
        player_gravity+=1
        player_hitbox.y+=player_gravity
        if player_hitbox.bottom >= ground_rect.top: player_hitbox.bottom = ground_rect.top
        player_animation()
        player_rect.center = player_hitbox.center
        player_rect.centery = player_hitbox.centery+30
        player_rect.centerx = player_hitbox.centerx+41
        # pygame.draw.rect(screen, "Red", player_hitbox)
        screen.blit(player_surface, player_rect)
        # Collision
        game_active = collisions(player_hitbox, obstacle_rect_list)

    else:
        screen.fill((0, 153, 255))
        screen.blit(welcome_text_surf, welcome_text_rect)
        
        screen.blit(player_surface2, player_rect2)

        last_score_text_surf = test_font.render(f"Last Score: {score}", False, "Black")
        last_score_text_surf = pygame.transform.rotozoom(last_score_text_surf,0,0.5)
        last_score_text_rect = last_score_text_surf.get_rect(midbottom = (400,320))
        screen.blit(last_score_text_surf, last_score_text_rect)
        
        curr_tick = pygame.time.get_ticks()
        if blink: screen.blit(instruction_text_surf, instruction_text_rect)
        if curr_tick - last_tick >= 300:
            last_tick = curr_tick
            if blink:
                blink = False
            else:
                blink = True

        

    # Update
    pygame.display.update()
    clock.tick(60)