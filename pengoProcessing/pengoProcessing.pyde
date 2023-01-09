"""
PENGO
"""
import time, math, os, random, pickle

from classes import *
add_library("minim")

def stripCharacters(string):
    #strips non-characters from beginning and end of word, and extra spaces between words
    spaceCount = 0
    i = 0
    while i < len(string):
        if string[i].isalnum():
            if i - spaceCount == 0:
                string = string[i:]
            elif spaceCount > 1:
                string = string[:i-spaceCount+1] + string[i:]
            spaceCount = 0
        else:
            spaceCount += 1
        i += 1
    string = string[:len(string) - spaceCount]
    return string

def formatWords(wordList):
    #recieves list of words and strips the spaces and converts it to uppercase
    for i in range(len(wordList)):
        wordList[i] = stripCharacters(wordList[i])

def readFromFile(filename):
    #takes a file and reads from it, stores it in a database
    #terminates program if file is not found
    try:
        file = open(filename)
    except OSError:
        print("File not found!")
        exit(0)
        
    database = []
    text = file.readlines()
    
    for line in text:
        line = line.strip()
        line = line.split(',')
        formatWords(line)
        database.append(line)
        
    file.close()
    
    return database

def settings():
    pass

def setup():
    global mouseLocation, whichKey, allowedChars, font, game, mode, offset, logo, startScreenBees, R, G, B, bonusFont, dimension, highscores, sprites
    fullScreen()

    font = createFont("PressStart2P.ttf", width // 90)
    
    background(0)
    mouseLocation = [-1,-1]
    whichKey = ""
    allowedChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY1234567890 "
    logo = loadImage("logo.png")
    database = readFromFile("images.txt")
    pengoSprites = database[0]
    pengoSprites = [loadImage(i) for i in pengoSprites]
    beeSprites = database[1]
    beeSprites = [loadImage(i) for i in beeSprites]
    sprites = database[2]
    sprites = [loadImage(i) for i in sprites]
    sprites.insert(2, pengoSprites)
    sprites.insert(3, beeSprites)
    Explosion.imgs = database[3]
    Explosion.imgs = [loadImage(i) for i in Explosion.imgs]
    dimension = int(database[4][0])
    minim = Minim(this)
    sound = minim.loadFile("pengomusic.mp3")
    loseLife = minim.loadFile("loselife.mp3")
    sound.loop()
    
    startScreenBees = [Bee(sprites[3], width/12, height/24 + height * 2 * i/24, height /20, height/20, 20) for i in range(6)]
    offset = height // dimension
    game = Board((width - height) // 2 + offset,offset,height - 2*offset,height - 2*offset,dimension,dimension, sprites, [loseLife])
    game.gameFont = createFont("PressStart2P.ttf", game.wdth//game.cols // 5)
    bonusFont = createFont("PressStart2P.ttf", game.wdth//13)
    Explosion.CoolFont = createFont("PressStart2P.ttf", game.wdth//game.cols // 3)
    mode = Mode("start")
    R, G, B = 0, 0, 0 # used later for random colors of border during bonus
    
    #Declare buttons
    Button.START = ImageButton(loadImage("start.png"), 0,0,0,0)
    Button.HELP = ImageButton(loadImage("help.png"), 0,0,0,0)
    Button.SCORE = ImageButton(loadImage("score.png"), 0,0,0,0)
    Button.BACK = ImageButton(loadImage("previous.png"), 0,0,0,0)
    Button.EXIT = ImageButton(loadImage("exit.png"), 0,0,0,0)
    Button.REPLAY = ImageButton(loadImage("replay.png"),0,0,0,0)
    Button.NEXT = ImageButton(loadImage("next.jpg"), 0,0,0,0)
    Button.PREV = ImageButton(loadImage("previous.jpg"),0,0,0,0)
    
    #load highscores
    highscores = []
    try:
        highscores = pickle.load( open( "highscores", "rb" ))
        indirectSort(highscores, 1)
        highscores.reverse()
    except IOError:
        pass

def draw():
    global whichKey, mode, game, R, G, B, mouseLocation, highscores, startScreenBees
    if mode.name == "start":
        background(0, 30, 200)
        imageMode(CENTER)
        image(logo, width/2, height/4, width*5/6, height *5/12)
        fill(0, 30, 200)
        noStroke()
        rect(startScreenBees[0].xPos, height/24, width*5/6, height *5/12)
        for bee in startScreenBees:
            bee.display()
            bee.xPos += bee.speed
        Button.START.setparams(width/4, height*7/12, width/3, height/8)
        Button.HELP.setparams(width/4, height*9/12, width/3, height/8)
        Button.SCORE.setparams(width*3/4, height*7/12, width/3, height/8)
        Button.EXIT.setparams(width*3/4, height*9/12, width/3, height/8)
        Button.START.display()
        Button.HELP.display()
        Button.SCORE.display()
        Button.EXIT.display()
        if Button.START.checkPressed(mouseLocation):
            game.name = ""
            mode = Mode("name")
            game.fill_board(int(game.cols*game.rows/4), 3, 1)
        if Button.HELP.checkPressed(mouseLocation):
            mode = Mode("help", "start")
        if Button.SCORE.checkPressed(mouseLocation):
            mode = Mode("scores", "start")
        if Button.EXIT.checkPressed(mouseLocation):
            closeProgram()
    elif mode.name == "name":
        background(0, 30, 200)
        textSize(height/40)
        textAlign(LEFT, TOP)
        text("Player, Type your name. Press 0 for backspace. \nMax length 15. Press start when ready.", width/12,height/8)
        textFont(Explosion.CoolFont)
        fill(0)
        text("> " + game.name, width/12, height/4)
        if whichKey == "0":
            game.name = game.name[:-1]
        elif whichKey in allowedChars and len(game.name) <= 15:
            game.name += whichKey
        Button.START.setparams(width/4, height*7/12, width/3, height/8)
        Button.BACK.setparams(width/4, height*9/12, width/3, height/8)
        Button.START.display()
        Button.BACK.display()
        if Button.START.checkPressed(mouseLocation) and len(game.name):
            mode = Mode("game")
        elif Button.BACK.checkPressed(mouseLocation):
            mode = Mode("start")
            startScreenBees = [Bee(sprites[3], width/12, height/24 + height * 2 * i/24, height /20, height/20, 20) for i in range(6)]
    elif mode.name == "scores":
        AMOUNTINPAGE = 10
        background(0, 30, 200)
        Button.BACK.setparams(width*3.3/4, height*11/12, width/3.4, height/8)
        Button.PREV.setparams(width*0.8/4, height*11/12, width/3.4, height/8)
        Button.NEXT.setparams(width*2/4, height*11/12, width/3.4, height/8)
        Button.BACK.display()
        Button.PREV.display()
        Button.NEXT.display()
        textFont(Explosion.CoolFont)
        textSize(height/30)
        fill(0)
        textAlign(LEFT, TOP)
        textSize(height/40)
        text("HIGH SCORES", width/30, height/40)
        #Code for multiple pages in highscores
        for i in range(AMOUNTINPAGE*mode.scorepage, AMOUNTINPAGE*(mode.scorepage+1)):
            try:
                textAlign(LEFT, TOP)
                text(str(i+1) + ". " + highscores[i][0], width/30, height/8+height*(i%AMOUNTINPAGE)/16)
                textAlign(RIGHT, TOP)
                text(str(highscores[i][1]) + " Points", width-width/30, height/8+height*(i%AMOUNTINPAGE)/16)
            except IndexError:
                text(str(i+1) + ".", width/30, height/8+height*(i%AMOUNTINPAGE)/16)
        if Button.BACK.checkPressed(mouseLocation):
            mode = Mode(mode.details, "return")
        elif Button.NEXT.checkPressed(mouseLocation):
            mode.scorepage += 1
        elif Button.PREV.checkPressed(mouseLocation):
            mode.scorepage -= 1 if mode.scorepage > 0 else 0
    elif mode.name == "help":
        background(0, 30, 200)
        Button.BACK.setparams(width*3.3/4, height*11/12, width/3, height/8)
        Button.BACK.display()
        if Button.BACK.checkPressed(mouseLocation):
            mode = Mode(mode.details, "return")
        textFont(font)
        fill(255)
        text("This is the help screen for Pengo.", width * 1/12, height * 1/12)
        text("Your objective is to kill all the Sno-Bees.", width * 1/12, height * 2/12)
        text("You can do this the following ways:", width * 1/12, height * 3/12)
        text("- You can push a block into them.", width * 1/12, height * 4/12)
        text("- You can stun them against a wall and run into them.", width * 1/12, height * 5/12)
        text("But, when you kill a Sno-Bee, a new one might hatch from an egg.", width * 1/12, height * 6/12)
        text("However, you can destroy blocks with eggs so that Sno-Bees can't hatch from them!", width * 1/12, height*7/12)
        text("You can also recieve bonus points from stacking the diamond blocks.", width * 1/12, height * 8/12)
        text("Use W,A,S,D to move around.", width * 1/12, height * 9/12)
        text("Press 'P' to push and destroy blocks, and to stun bees.", width * 1/12, height * 10/12)
        text("Good luck!", width * 1/12, height * 11/12)
    elif mode.name == "game":
        background(0)
        if game.bonusRemaining:
            if game.bonusRemaining % 100 == 0:
                R = random.randint(0,255)
                G = random.randint(0,255)
                B = random.randint(0,255)
            game.bonusRemaining -= 10
            fill(R,G,B)
        else:
            fill(255)
        rect((width - height) // 2, 0, height, height)
        fill(0)
        rect((width - height) // 2 + offset,offset,height - 2*offset,height - 2*offset)
        if frameCount < mode.entryframe + frameRate:
            game.startGame(True if mode.details == "return" else False)
        else:
            game.display()
            game.movepengo(whichKey)
            game.pButton(whichKey)
        if game.bonusRemaining:
            fill(255)
            textFont(bonusFont)
            text(game.bonusRemaining, width // 2 - 2 * game.wdth/game.cols, height // 2)
        if game.gamedone:
            mode = Mode("done")
            highscoreUpdate(highscores, game.name, game.score)
        if game.lostlife:
            mode.details = "return"
            mode.entryframe = frameCount
            game.lostlife = False
        Button.SCORE.setparams(width*10.6/12, height*2/4, width/5, height/10)
        Button.HELP.setparams(width*10.6/12, height*2/4+height/9, width/5, height/10)
        Button.EXIT.setparams(width*10.6/12, height*2/4+height*2/9, width/5, height/10)
        Button.SCORE.display()
        Button.HELP.display()
        Button.EXIT.display()
        if Button.SCORE.checkPressed(mouseLocation):
            mode = Mode("scores", "game")
        elif Button.HELP.checkPressed(mouseLocation):
            mode = Mode("help", "game")
        elif Button.EXIT.checkPressed(mouseLocation):
            mode = Mode("start")
            startScreenBees = [Bee(sprites[3], width/12, height/24 + height * 2 * i/24, height /20, height/20, 20) for i in range(6)]
    elif mode.name == "done":
        background(0)
        Button.BACK.setparams(width*2/3, height/2, width/5, height/10)
        Button.REPLAY.setparams(width * 1/3, height / 2, width/5, height / 10)
        Button.BACK.display()
        Button.REPLAY.display()
        if Button.BACK.checkPressed(mouseLocation):
            mode = Mode("start")
            startScreenBees = [Bee(sprites[3], width/12, height/24 + height * 2 * i/24, height /20, height/20, 20) for i in range(6)]
        elif Button.REPLAY.checkPressed(mouseLocation):
            game.fill_board(int(game.cols*game.rows/4), 3, 1)
            mode = Mode("game")
        fill(255)
        textFont(bonusFont)
        text("Your score was " + str(game.score), width * 2/11, height * 1/12)
    whichKey = ''
    mouseLocation = [-1, -1]

def mouseReleased():
    global mouseLocation
    mouseLocation = [int(mouseX), int(mouseY)]

def keyReleased():
    #No keycodes used in program
    global whichKey, allowedChars
    whichKey = ''

def closeProgram():
    #Dumps highscores
    global highscores
    pickle.dump(highscores, open('highscores', 'wb'))
    exit()
def keyPressed():
    global whichKey, allowedChars
    if key == CODED:
        return
    elif key in allowedChars:
        whichKey = key.upper()
    else:
        whichKey = ''
