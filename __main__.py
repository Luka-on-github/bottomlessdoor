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
    clock = pygame.time.Clock()

class game:
    loadingPos = (100, 600)
    loadingAngle = 0
    loadingRotations = 0
    door = pygame.transform.scale(pygame.image.load("images/roomAssets/door.png"), (200, 200))
    doorPos = [700, 350]
    player = pygame.transform.scale(pygame.image.load("images/character/idle1.png"), (200, 200))
    loading = True
    walkAnimation = 1
    bgList = list(constant.bg)
    newRoom = False
    roomNumber = 1
    currentRoom = ""
    window = pygame.transform.scale(pygame.image.load("images/roomAssets/window.png"), (200, 200))
    windowPos = [600, 150]

    roomSelection = [
        "inverted",
        "flies",
        "window"
        "dark",
    ]

    def roomTrasition():
        constant.screen.fill(constant.bg)
        constant.bg = tuple(game.bgList)
        if game.newRoom == True:
            if game.bgList[1] < 255:
                game.bgList[0] = game.bgList[0] + 1
                game.bgList[1] = game.bgList[1] + 1
                game.bgList[2] = game.bgList[2] + 1
            else:
                game.doorPos[0] = game.doorPos[0] + 600
                game.windowPos[0] = game.windowPos[0] + 600
                game.newRoom = False
                game.roomNumber = game.roomNumber + 1
                game.currentRoom = random.choice(game.roomSelection)
            
        else:
            if constant.bg[1] > 0:
                game.bgList[0] = game.bgList[0] - 1
                game.bgList[1] = game.bgList[1] - 1
                game.bgList[2] = game.bgList[2] - 1
            else:
                game.newRoom = True

class start:
    textShade = 0
    text1 = pygame.font.Font("other/TTSupermolotNeue.ttf", 75)
    pfp = pygame.transform.scale(pygame.image.load("other/pfp.jpeg"), (300, 300))

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
    if constant.kL == 5:
        constant.kL = 0
        constant.timer = constant.timer + 1

def draw_game(screen):
    keys = pygame.key.get_pressed()
    screen.fill(constant.bg)
    if game.loading == True:
        if game.loadingRotations <= 28:
            pygame.draw.circle(screen, (0, 0, 0), game.loadingPos, 10)
            game.loadingPos = (100 + 30 * math.cos(math.radians(game.loadingAngle)), 600 + 30 * math.sin(math.radians(game.loadingAngle)))
            game.loadingAngle = (game.loadingAngle + 2) % 360
        else:
            game.loading = False

        if game.loadingRotations == 25:
            mixer.music.load("other/voice1.wav")
            mixer.music.play(1)

        if game.loadingRotations == 26 or game.loadingRotations == 27:
            subtitle1 = start.text1.render("How about this, you never know", True, (start.textShade, start.textShade, start.textShade))
            subtitle2 = start.text1.render("what's on the other side of a door", True, (start.textShade, start.textShade, start.textShade))
            screen.blit(subtitle1, (10, 100))
            screen.blit(subtitle2, (10, 200))

        if game.loadingRotations == 19:
            mixer.music.load("other/voice2.wav")
            mixer.music.play(1)

        if game.loadingRotations == 20 or game.loadingRotations == 21:
            subtitle3 = start.text1.render("The games not loading again...", True, (start.textShade, start.textShade, start.textShade))
            screen.blit(subtitle3, (10, 100))
        if game.loadingAngle == 2:
            game.loadingRotations = game.loadingRotations + 1

    elif game.loading == False:
        constant.timer = 0
        mousePos = pygame.mouse.get_pos()
        screen.blit(game.player, (500, 350))
        screen.blit(game.door, (game.doorPos[0] - 50, game.doorPos[1] + 100))
        print(mousePos)

        if game.doorPos[0] >= 550 and game.doorPos[0] <= 600 and game.doorPos[1] >= 250 and game.doorPos[1] <= 350:
            game.roomTrasition()
        else:
            if game.currentRoom is not "dark":
                constant.bg = (255, 255, 255)

        if keys[K_LEFT]:
            game.doorPos[0] = game.doorPos[0] + 5
            game.windowPos[0] = game.windowPos[0] + 5
            if constant.kL == 1:
                if game.walkAnimation == 2:
                    game.player = pygame.transform.scale(pygame.image.load("images/character/walkingRight4.png"), (200, 200))
                else:
                    game.player = pygame.transform.scale(pygame.image.load("images/character/walkingRight1.png"), (200, 200))
            elif constant.kL == 2:
                if game.walkAnimation == 2:
                    game.player = pygame.transform.scale(pygame.image.load("images/character/walkingRight5.png"), (200, 200))
                else:
                    game.player = pygame.transform.scale(pygame.image.load("images/character/walkingRight2.png"), (200, 200))
            elif constant.kL == 3:
                if game.walkAnimation == 2:
                    game.walkAnimation = 1
                    game.player = pygame.transform.scale(pygame.image.load("images/character/walkingRight6.png"), (200, 200))
            elif constant.kL == 4:
                if game.walkAnimation == 1:
                    game.walkAnimation = 2
                    game.player = pygame.transform.scale(pygame.image.load("images/character/walkingRight3.png"), (200, 200))

        elif keys[K_RIGHT]:
            game.doorPos[0] = game.doorPos[0] - 5
            game.windowPos[0] = game.windowPos[0] - 5
            if constant.kL == 1:
                if game.walkAnimation == 2:
                    game.player = pygame.transform.scale(pygame.image.load("images/character/walkingLeft4.png"), (200, 200))
                else:
                    game.player = pygame.transform.scale(pygame.image.load("images/character/walkingLeft1.png"), (200, 200))
            elif constant.kL == 2:
                if game.walkAnimation == 2:
                    game.player = pygame.transform.scale(pygame.image.load("images/character/walkingLeft5.png"), (200, 200))
                else:
                    game.player = pygame.transform.scale(pygame.image.load("images/character/walkingLeft2.png"), (200, 200))
            elif constant.kL == 3:
                if game.walkAnimation == 2:
                    game.walkAnimation = 1
                    game.player = pygame.transform.scale(pygame.image.load("images/character/walkingLeft6.png"), (200, 200))
            elif constant.kL == 4:
                if game.walkAnimation == 1:
                    game.walkAnimation = 2
                    game.player = pygame.transform.scale(pygame.image.load("images/character/walkingLeft3.png"), (200, 200))

        elif keys[K_UP]:
            game.doorPos[1] = game.doorPos[1] + 5
            game.windowPos[1] = game.windowPos[1] + 5
            game.player = pygame.transform.scale(pygame.image.load("images/character/idle3.png"), (200, 200))

        elif keys[K_DOWN]:
            game.doorPos[1] = game.doorPos[1] - 5
            game.windowPos[1] = game.windowPos[1] - 5
        else:
            if constant.kL == 1:
                game.player = pygame.transform.scale(pygame.image.load("images/character/idle1.png"), (200, 200))
            elif random.randint(1, 150) == 2:
                if constant.kL == 2:
                    game.player = pygame.transform.scale(pygame.image.load("images/character/idle2.png"), (200, 200))
                elif constant.kL == 3:
                    game.player = pygame.transform.scale(pygame.image.load("images/character/idle3.png"), (200, 200))
        if game.roomNumber == 1:
            if constant.timer <= 50:
                subtitle3 = start.text1.render("Use the arrow keys to move", True, (start.textShade, start.textShade, start.textShade))
                screen.blit(subtitle3, (100, 100))
        else:
            if game.currentRoom == "inverted":
                if constant.kL == 2 or constant.kL == 4:
                    if keys[K_RIGHT]:
                        game.doorPos[0] = game.doorPos[0] + 10
                    if keys[K_LEFT]:
                        game.doorPos[0] = game.doorPos[0] - 10

            elif game.currentRoom == "dark":
                screen.fill(0, 0, 0)

            elif game.currentRoom == "window":
                screen.blit(game.window, tuple(game.windowPos))
                

                



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
    constant.clock.tick(120)
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
