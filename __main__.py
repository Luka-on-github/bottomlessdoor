import pygame, random, sys, math, numpy as np
from pygame import mixer
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
)

class constant:
    timer = 0
    bg = (255, 255, 255)
    pygame.init()
    pygame.display.set_caption("The Bottomless Door")
    icon = pygame.image.load("images/roomAssets/door.png")
    pygame.display.set_icon(icon)
    mixer.init()
    mixer.music.set_volume(1)
    screen = display_surface = pygame.display.set_mode((1300, 700))
    state = "start"
    mL = 0
    sL = 0
    kL = 0
    clock = pygame.time.Clock()

class game:
    textShade = 0
    title = pygame.font.Font("other/slkscreb.ttf", 90)
    text = pygame.font.Font("other/slkscr.ttf", 50)

    pfp = pygame.transform.scale(pygame.image.load("other/pfp.jpeg"), (300, 300))
    lag_delay = 0
    lag_movement_buffer = []
    confetti_particles = []
    loadingPos = (100, 600)
    loadingAngle = 0
    loadingRotations = 0
    door = pygame.transform.scale(pygame.image.load("images/roomAssets/door.png"), (200, 200))
    doorPos = [700, 250]
    playerSize = [200,200]
    player = pygame.transform.scale(pygame.image.load("images/character/idle1.png"), tuple(playerSize))
    loading = True
    walkAnimation = 1
    bgList = list(constant.bg)
    newRoom = False
    roomNumber = 1
    window = pygame.transform.scale(pygame.image.load("images/roomAssets/window.png"), (200, 200))
    windowPos = [400, 100]
    fly = pygame.transform.scale(pygame.image.load("images/roomAssets/fly.png"), (50, 50))
    flyPos = [100, 400]
    meme = pygame.transform.scale(pygame.image.load("images/roomAssets/memes.png"), (600, 300))
    memePos = [0, 0]
    playerEndPos = [500, 350]
    street = pygame.transform.scale(pygame.image.load("images/roomAssets/alley.png"), (1300, 700))

    roomSelection = [
        "inverted",
        "flies",
        "window",
        "dark",
        "confetti",
        "lag",
        "meme",
        "static",
    ]

    currentRoomRand = random.choice(roomSelection)
    currentRoom = "default"

    class ConfettiParticle:
        def __init__(self, x, y):
            self.pos = pygame.Vector2(x, y)
            self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-3, -1))
            self.color = random.choice([
                (255, 0, 0), (0, 255, 0), (0, 0, 255),
                (255, 255, 0), (255, 0, 255), (0, 255, 255)
            ])
            self.size = random.randint(2, 4)
            self.lifetime = 60

        def update(self):
            self.pos += self.velocity
            self.velocity.y += 0.1
            self.lifetime -= 1

        def draw(self, surface):
            pygame.draw.rect(surface, self.color, (*self.pos, self.size, self.size))

        def is_dead(self):
            return self.lifetime <= 0

    def roomTrasition():
        mixer.music.stop()
        constant.bg = tuple(game.bgList)
        if game.roomNumber > 1 and game.currentRoom in game.roomSelection:
            game.roomSelection.remove(game.currentRoom)
        if game.newRoom == True:
            if game.bgList[1] != 255:
                game.bgList[0] = game.bgList[0] + 1
                game.bgList[1] = game.bgList[1] + 1
                game.bgList[2] = game.bgList[2] + 1
            else:
                mixer.music.stop()
                game.doorPos[0] = game.doorPos[0] + 600
                game.windowPos[0] = game.windowPos[0] + 600
                game.newRoom = False
                game.roomNumber = game.roomNumber + 1
                game.currentRoom = game.currentRoomRand
                constant.timer = 0
                if game.currentRoom == "dark":
                    mixer.music.load("other/voice4.wav")
                    mixer.music.play(1)
                    constant.bg = (0, 0, 0)
                if game.currentRoom == "street":
                    game.playerSize[0] = 300
                    game.playerSize[1] = 300
                    game.playerEndPos[0] = 100 
                    game.playerEndPos[1] = 400

                game.lag_movement_buffer = []
                game.lag_delay = 0
                if game.currentRoom == "meme":
                    mixer.music.load("other/vineboom.mp3")
                    mixer.music.play(1)

                elif game.currentRoom == "fly":
                    mixer.music.load("other/fly.mp3")
                    mixer.music.play(1)
            
        else:
            if constant.bg[1] > 0:
                game.bgList[0] = game.bgList[0] - 1
                game.bgList[1] = game.bgList[1] - 1
                game.bgList[2] = game.bgList[2] - 1
            else:
                game.newRoom = True

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
    print(constant.timer, game.currentRoom, game.roomSelection, pygame.mouse.get_pos())

    if game.currentRoom == "meme":
        screen.blit(game.meme, tuple(game.memePos))

    if game.currentRoom == "window":
        screen.blit(game.window, tuple(game.windowPos))

    if game.currentRoom == "flies":
        if constant.timer == 5:
            mixer.music.load("other/voice3.wav")
            mixer.music.play(1)
            constant.timer = 6

        screen.blit(game.fly, tuple(game.flyPos))
        if game.flyPos[1] == 400 and game.flyPos[0] > 0:
            game.flyPos[0] = game.flyPos[0] - 10
        elif game.flyPos[0] == 0 and game.flyPos[1] > 0:
            game.flyPos[1] = game.flyPos[1] - 10
        elif game.flyPos[1] == 0 and game.flyPos[0] < 1400:
            game.flyPos[0] = game.flyPos[0] + 10
        elif game.flyPos[0] == 1400 and game.flyPos[1] < 400:
            game.flyPos[1] = game.flyPos[1] + 10
        elif game.flyPos[0] > 0 and game.flyPos[1] == 400:
            game.flyPos[0] = game.flyPos[0] - 10

    if game.currentRoom == "confetti":
        player_pos = pygame.Vector2(600, 500)
        if keys[K_LEFT] or keys[K_RIGHT]:
            for _ in range(5):
                game.confetti_particles.append(game.ConfettiParticle(player_pos.x, player_pos.y))

        for particle in game.confetti_particles[:]:
            particle.update()
            if particle.is_dead():
                game.confetti_particles.remove(particle)
            else:
                particle.draw(screen)

    if game.currentRoom == "lag":
        game.lag_delay = game.lag_delay + 1
        constant.clock.tick(20)
        input_state = {
            "left": keys[K_LEFT],
            "right": keys[K_RIGHT]
        }
        game.lag_movement_buffer.append(input_state)
        if len(game.lag_movement_buffer) > 5:
            delayed_input = game.lag_movement_buffer.pop(0)
            if delayed_input["left"]:
                game.doorPos[0] = game.doorPos[0] + 5
                game.windowPos[0] = game.windowPos[0] + 5
            if delayed_input["right"]:
                game.doorPos[0] = game.doorPos[0] - 5
                game.windowPos[0] = game.windowPos[0] - 5
    
    if game.currentRoom == "static":
        subtitle4 = game.text.render("What happened to the signal?", True, (game.textShade, game.textShade, game.textShade))
        if not mixer.music.get_busy():
            mixer.music.load("other/static.mp3")
            mixer.music.play(-1)
        noise_surface = pygame.Surface((260, 140))
        arr = pygame.surfarray.pixels3d(noise_surface)
        arr[:, :, :] = np.random.randint(0, 256, (260, 140, 3))
        del arr
        scaled_noise = pygame.transform.scale(noise_surface, (1400, 750))
        screen.blit(scaled_noise, (0, 0))
        screen.blit(subtitle4, (100, 100))

    if game.currentRoom == "escaped":
        if constant.timer == 5:
            mixer.music.load("other/robot.wav")
            mixer.music.play(1)
            constant.timer = 6

        subtitle5 = game.title.render("END OF GAME:", True, (game.textShade, game.textShade, game.textShade))
        subtitle6 = game.title.render("SYSTEMS DOWN", True, (game.textShade, game.textShade, game.textShade))
        screen.blit(subtitle5, (100, 100))
        screen.blit(subtitle6, (100, 200))
        game.door = pygame.transform.scale(pygame.image.load("images/roomAssets/doorClosed.png"), (200, 200))

        if game.playerEndPos[0] >= 1400 or game.playerEndPos[0] <= -100:
            if "street" not in game.roomSelection and len(game.roomSelection) == 0:
                game.roomSelection.append("street")
            else:
                game.roomTrasition()
    
    if game.currentRoom == "street":
        screen.blit(game.street, (0, 0))
        if game.playerEndPos[0] > 1050:
            pygame.quit()
            sys.exit("User quit: Game finished")

    if game.doorPos[0] >= 1500:
        game.doorPos[0] = -150
    elif game.doorPos[0] <= -200:
        game.doorPos[0] = 1450

    if game.windowPos[0] >= 1500:
        game.windowPos[0] = -150
    elif game.windowPos[0] <= -200:
        game.windowPos[0] = 1450

    if game.memePos[0] >= 1500:
        game.memePos[0] = -150
    elif game.memePos[0] <= -200:
        game.memePos[0] = 1450

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
            subtitle1 = game.text.render("How about this, you never know", True, (game.textShade, game.textShade, game.textShade))
            subtitle2 = game.text.render("what's on the other side of a door", True, (game.textShade, game.textShade, game.textShade))
            screen.blit(subtitle1, (10, 100))
            screen.blit(subtitle2, (10, 200))

        if game.loadingRotations == 19:
            mixer.music.load("other/voice2.wav")
            mixer.music.play(1)

        if game.loadingRotations == 20 or game.loadingRotations == 21:
            subtitle3 = game.text.render("The games not loading again...", True, (game.textShade, game.textShade, game.textShade))
            screen.blit(subtitle3, (10, 100))
        if game.loadingAngle == 2:
            game.loadingRotations = game.loadingRotations + 1

    elif game.loading == False:
        screen.blit(game.player, tuple(game.playerEndPos))
        screen.blit(game.door, (game.doorPos[0] - 50, game.doorPos[1] + 100))

        if game.doorPos[0] >= 550 and game.doorPos[0] <= 600 and game.doorPos[1] >= 250 and game.doorPos[1] <= 350 and game.currentRoom != "escaped":
            game.roomTrasition()
        else:
            if game.currentRoom != "dark":
                constant.bg = (255, 255, 255)

    if keys[K_LEFT]:
        if game.currentRoom == "inverted":
            game.doorPos[0] -= 5
            game.windowPos[0] -= 5
            game.memePos[0] -= 5
        elif game.currentRoom in ["escaped", "street"]:
            game.playerEndPos[0] -= 5
        else:
            game.doorPos[0] += 5
            game.windowPos[0] += 5
            game.memePos[0] += 5

        if constant.kL == 1:
            if game.walkAnimation == 2:
                game.player = pygame.transform.scale(pygame.image.load("images/character/walkingRight4.png"), tuple(game.playerSize))
            else:
                game.player = pygame.transform.scale(pygame.image.load("images/character/walkingRight1.png"), tuple(game.playerSize))
        elif constant.kL == 2:
            if game.walkAnimation == 2:
                game.player = pygame.transform.scale(pygame.image.load("images/character/walkingRight5.png"), tuple(game.playerSize))
            else:
                game.player = pygame.transform.scale(pygame.image.load("images/character/walkingRight2.png"), tuple(game.playerSize))
        elif constant.kL == 3:
            if game.walkAnimation == 2:
                game.walkAnimation = 1
                game.player = pygame.transform.scale(pygame.image.load("images/character/walkingRight6.png"), tuple(game.playerSize))
        elif constant.kL == 4:
            if game.walkAnimation == 1:
                game.walkAnimation = 2
                game.player = pygame.transform.scale(pygame.image.load("images/character/walkingRight3.png"), tuple(game.playerSize))

    elif keys[K_RIGHT]:
        if game.currentRoom == "inverted":
            game.doorPos[0] += 5
            game.windowPos[0] += 5
            game.memePos[0] += 5
        elif game.currentRoom in ["escaped", "street"]:
            game.playerEndPos[0] += 5
        else:
            game.doorPos[0] -= 5
            game.windowPos[0] -= 5
            game.memePos[0] -= 5

        if constant.kL == 1:
            if game.walkAnimation == 2:
                game.player = pygame.transform.scale(pygame.image.load("images/character/walkingLeft4.png"), tuple(game.playerSize))
            else:
                game.player = pygame.transform.scale(pygame.image.load("images/character/walkingLeft1.png"), tuple(game.playerSize))
        elif constant.kL == 2:
            if game.walkAnimation == 2:
                game.player = pygame.transform.scale(pygame.image.load("images/character/walkingLeft5.png"), tuple(game.playerSize))
            else:
                game.player = pygame.transform.scale(pygame.image.load("images/character/walkingLeft2.png"), tuple(game.playerSize))
        elif constant.kL == 3:
            if game.walkAnimation == 2:
                game.walkAnimation = 1
                game.player = pygame.transform.scale(pygame.image.load("images/character/walkingLeft6.png"), tuple(game.playerSize))
        elif constant.kL == 4:
            if game.walkAnimation == 1:
                game.walkAnimation = 2
                game.player = pygame.transform.scale(pygame.image.load("images/character/walkingLeft3.png"), tuple(game.playerSize))


    else:
        if constant.kL == 1:
            game.player = pygame.transform.scale(pygame.image.load("images/character/idle1.png"), tuple(game.playerSize))
        elif random.randint(1, 150) == 2:
            if constant.kL == 2:
                game.player = pygame.transform.scale(pygame.image.load("images/character/idle2.png"), tuple(game.playerSize))
            elif constant.kL == 3:
                game.player = pygame.transform.scale(pygame.image.load("images/character/idle3.png"), tuple(game.playerSize))

        if game.roomNumber == 1:
            if constant.timer >= 70:
                subtitle3 = game.text.render("Use the arrow keys to move", True, (game.textShade, game.textShade, game.textShade))
                screen.blit(subtitle3, (100, 100))
        else:
            if len(game.roomSelection) > 0:
                game.currentRoomRand = random.choice(game.roomSelection)
            else:
                game.currentRoomRand = "escaped"

def draw_splash(screen):
    game.textShade = game.textShade + 0.5
    intro1 = game.title.render("Luka22r presents...", True, (game.textShade, game.textShade, game.textShade))
    intro2 = game.title.render("Bottomless Door", True, (game.textShade, game.textShade, game.textShade))
    screen.fill(constant.bg)
    screen.blit(game.pfp, (500, 100))
    screen.blit(intro1, (0, 400))
    screen.blit(intro2, (0, 500))
    if game.textShade == 255:
        constant.state = "game"
        game.textShade = 0


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