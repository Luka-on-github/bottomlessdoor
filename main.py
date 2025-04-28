import pygame, random, sys, math
from pygame import mixer
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,
    QUIT,
)



class game:
    loadingPos = (100, 600)
    loadingAngle = 0
    loadingRotations = 0
    door = pygame.transform.scale(pygame.image.load("door.png"), (200, 200))
    doorPos = [750, 500]
    player = pygame.transform.scale(pygame.image.load("idle1.png"), (200, 200))
    loading = True

class constant:
    timer = 0
    bg = (255, 255, 255)
    pygame.init()
    mixer.init()
    mixer.music.set_volume(1)
    screen = display_surface = pygame.display.set_mode((1300, 700))
    state = "start"
    mL = 0
    sL = 0
    kL = 0

class start:
    textShade = 0
    text1 = pygame.font.Font("TTSupermolotNeue.ttf", 75)
    pfp = pygame.transform.scale(pygame.image.load("pfp.jpeg"), (300, 300))

def physicClock():
    if constant.mL >= 0:
        constant.mL = constant.mL + 1
    if constant.mL == 5:
        constant.mL = constant.mL - 5
    if constant.mL == 4:
        constant.sL = constant.sL + 1
    elif constant.sL >= 4:
        constant.sL = 0
        constant.kL = constant.kL + 1
        print("Clock:", constant.kL)
    if constant.kL == 4:
        constant.kL = 0
        constant.timer = constant.timer + 1

def draw_game(screen):
    keys = pygame.key.get_pressed()
    screen.fill(constant.bg)

    if game.loadingRotations <= 28:
        pygame.draw.circle(screen, (0, 0, 0), game.loadingPos, 10)
        game.loadingPos = (100 + 30 * math.cos(math.radians(game.loadingAngle)), 600 + 30 * math.sin(math.radians(game.loadingAngle)))
        game.loadingAngle = (game.loadingAngle + 2) % 360
    else:
        game.loading = False

    if game.loadingRotations == 25:
        mixer.music.load("voice1.wav")
        mixer.music.play(1)

    if game.loadingRotations == 26 or game.loadingRotations == 27:
        subtitle1 = start.text1.render("How about this, you never know", True, (start.textShade, start.textShade, start.textShade))
        subtitle2 = start.text1.render("what's on the other side of a door", True, (start.textShade, start.textShade, start.textShade))
        screen.blit(subtitle1, (10, 100))
        screen.blit(subtitle2, (10, 200))

    if game.loadingRotations == 19:
        mixer.music.load("voice2.wav")
        mixer.music.play(1)

    if game.loadingRotations == 20 or game.loadingRotations == 21:
        subtitle3 = start.text1.render("The games not loading again...", True, (start.textShade, start.textShade, start.textShade))
        screen.blit(subtitle3, (10, 100))
    if game.loadingAngle == 2:
        game.loadingRotations = game.loadingRotations + 1

    if game.loading == False:
        constant.timer = 0
        screen.blit(game.player, (500, 350))
        screen.blit(game.door, tuple(game.doorPos))
        if keys[K_LEFT]:
            game.doorPos[0] = game.doorPos[0] + 5
        if keys[K_RIGHT]:
            game.doorPos[0] = game.doorPos[0] - 5
            if constant.mL == 1:
                game.player = pygame.transform.scale(pygame.image.load("walkingLeft1.png"), (200, 200))
        if keys[K_UP]:
            game.doorPos[1] = game.doorPos[1] + 5
        if keys[K_DOWN]:
            game.doorPos[1] = game.doorPos[1] - 5
        if constant.timer <= 10:
            subtitle3 = start.text1.render("Use the arrow keys to move", True, (start.textShade, start.textShade, start.textShade))
            screen.blit(subtitle3, (100, 100))
        


def draw_splash(screen):
    start.textShade = start.textShade + 0.5
    intro1 = start.text1.render("Luka22r presents...", True, (start.textShade, start.textShade, start.textShade))
    intro2 = start.text1.render("Bottomless Doodle", True, (start.textShade, start.textShade, start.textShade))
    screen.fill(constant.bg)
    screen.blit(start.pfp, (450, 100))
    screen.blit(intro1, (300, 400))
    screen.blit(intro2, (300, 500))
    if start.textShade == 255:
        constant.state = "game"
        start.textShade = 0


while True:
    physicClock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit("User quit: Program shutdown")

    if constant.state == "start":
        draw_splash(constant.screen)
    elif constant.state == "game":
        draw_game(constant.screen)
    pygame.display.update()