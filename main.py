import pygame, sys
import random

#pygame initialisieren mit init
pygame.init()

#basic game setup
window_width = 450
window_height = 800
window = pygame.display.set_mode((window_width,window_height))
pygame_icon = pygame.image.load('textures/hdbw.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("HDBW Bird")
refresh_rate = 120
FPS = pygame.time.Clock()


#import sounds
pygame.mixer.init()
coin_sound = pygame.mixer.Sound('sounds/point.ogg')
hit_sound = pygame.mixer.Sound('sounds/hit.ogg')
wing_sound = pygame.mixer.Sound('sounds/wing.ogg')
backround_song = pygame.mixer.music.load('sounds/backroundsong.ogg')

#play background song
pygame.mixer.music.play()

#score fontstyle
font = pygame.font.SysFont("Arial",48)

#StarterScreen
startscreen = pygame.transform.scale2x(pygame.image.load('textures/message2.png').convert_alpha())

#load backround
backround = pygame.image.load('textures/bg.png').convert()
#load and transform ground
ground = pygame.image.load('textures/base.png').convert()
ground = pygame.transform.scale(ground,(window_width, ground.get_height()))



#load player images
player_down = pygame.transform.scale2x(pygame.image.load('player/yellowbird-downflap.png').convert())
player_mid = pygame.transform.scale2x(pygame.image.load('player/yellowbird-midflap.png').convert())
player_up = pygame.transform.scale2x(pygame.image.load('player/yellowbird-upflap.png').convert())
#player setup
player_animation = [player_up, player_mid, player_down]
player = player_animation[0]
player_rect = player.get_rect(center=(100,400))

#player userevent
ANIMATIONEVENT = pygame.USEREVENT
pygame.time.set_timer(ANIMATIONEVENT, 100)
player_counter = 0
#obstacle userevent
SPAWNOBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNOBSTACLE, 800)

#load and scale obstacles
obstacle = pygame.transform.scale2x(pygame.image.load('textures/pipe.png').convert())
#create random obstacle list
obstacle_choices = [700,800,900,1000]

obstacles = [0]

#set counter 0
counter = 0

def score(counter, obstacles):
    text = "Score:"
    text += str(int(counter / 2))

    score = font.render(text, True, (255, 255, 255))
    window.blit(score, (150, 50))

    for obstacle in obstacles:
        if player_rect.centerx == obstacle.centerx:
            counter += 1
            pygame.mixer.Sound.play(coin_sound)
    return counter



def collisions(obstacles, player_rect):
    if player_rect.centery > 720:
        pygame.mixer.Sound.play(hit_sound)
        return True

    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            pygame.mixer.Sound.play(hit_sound)
            return True

    return False


def spawn_obstacle():
    obstacle_height = random.choice(obstacle_choices)
    obstacle_rect_normal = obstacle.get_rect(center = (700, obstacle_height))
    obstacle_rect_flip = obstacle.get_rect(center = (700, obstacle_height - 900))
    return(obstacle_rect_normal, obstacle_rect_flip)


def draw_obstacles(obstacles):
    for obstacle_x in obstacles:
        if obstacle_x.bottom >= 800:
            window.blit(obstacle, obstacle_x)
        else:
            new_obstacle = pygame.transform.flip(obstacle, False, True)
            window.blit(new_obstacle, obstacle_x)


def move_obstacles(obstacles):
    for obstacle in obstacles:
        obstacle.centerx -= 4


#x-achse des hintergrund
ground_x = 0
backround_x = 0

collision = True

#while-schleife (gameloop)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.mixer.Sound.play(wing_sound)
                player_move = 0
                player_move -= 7
            collision = False

        if event.type == SPAWNOBSTACLE:
            obstacles.extend(spawn_obstacle())

        if event.type == ANIMATIONEVENT:
            player = player_animation[player_counter % 3]
            player_counter += 1


    window.blit(backround, (backround_x,0))
    window.blit(backround, (backround_x + window_width,0))
    backround_x -=0.5
    if abs(backround_x) == window_width:
        backround_x = 0

    if collision is not True:
        player_move += 0.25
        player_rect.centery += player_move
        newplayer = pygame.transform.rotate(player, player_move * -5)
        window.blit(newplayer, player_rect)
        draw_obstacles(obstacles)
        move_obstacles(obstacles)
        collision = collisions(obstacles, player_rect)
        counter = score(counter, obstacles)

    else:
        obstacles = []
        counter = 0
        player_rect.centery = 500
        window.blit(startscreen, (40,50))


    window.blit(ground, (ground_x, 720))
    window.blit(ground, (ground_x + window_width, 720))
    ground_x -= 1.5
    if abs(ground_x) == window_width:
        ground_x = 0

    FPS.tick(refresh_rate)
    pygame.display.update()
