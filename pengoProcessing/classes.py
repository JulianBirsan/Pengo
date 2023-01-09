"""
Object Oriented Programming

"""
import random
import math

def binarySearch (arr, l, r, x):
    if r >= l:
 
        mid = l + (r - l) // 2
        if arr[mid][0] == x:
            return mid
        elif arr[mid][0] > x:
            return binarySearch(arr, l, mid-1, x)
        else:
            return binarySearch(arr, mid + 1, r, x)
 
    else:
        return -1

def indirectSort(listToSort, index):
    #A function to sort a 2d list by the value in a certain index of the inner lists (indirect sort)
    for i in range(1, len(listToSort)):
        done = True
        for j in range(len(listToSort) - i):
            if listToSort[j][index] > listToSort[j+1][index]:
                listToSort[j], listToSort[j+1] = listToSort[j+1], listToSort[j]
                done = False
        if done:
            break

def sortedInsert(lis, item):
    #A function to insert a list into a 2d array by the value in index 1
    if len(lis) == 0:
        lis.append(item)
        return
    for i in range(len(lis)):
        if lis[i][1] < item[1]:
            lis.insert(i, item)
            return
    lis.append(item)

def highscoreUpdate(hs, name, score):
    #A function for checking if a player is already on the highscore list, and updating his score if not.
    # hs is highscores list , name is the name of the player, and score is the score we want to update, checking if its a better score
    # Uses binary search
    check = False
    indirectSort(hs,0)
    index = binarySearch(hs,0,len(hs)-1, name)
    if index != -1:
        hs[index][1] = score if score > hs[index][1] else hs[index][1]
        check = True
    indirectSort(hs, 1)
    hs.reverse()
    if not check:
        sortedInsert(hs, [name, score])

def rangeOverlap(range1, range2):
    # Takes to range objects and returns true if they share some value
    for i in range1:
        if i in range2:
            return True
    return False

class Mode:
    def __init__(self, name, details = None):
        self.name = name
        self.details = details
        self.entryframe = frameCount
        self.scorepage = 0 #for scores page only

class Explosion:
    imgs = []
    CoolFont = None
    def __init__(self, x,y,w,h, score):
        self.xPos, self.yPos, self.wdth, self.hght = x,y,w,h
        self.frame = 0
        self.points = score
        self.nextFrame = frameCount + frameRate/24
    def display(self):
        
        image(self.imgs[self.frame], self.xPos, self.yPos, self.wdth, self.hght)
        if self.points:
            textFont(self.CoolFont)
            fill(255)
            text(self.points, self.xPos + self.wdth / 2, self.yPos)
        if (self.nextFrame < frameCount):
            self.nextFrame += frameRate/24
            self.frame += 1
        if self.frame == 12:
            return False
        return True
    

    
class ImageButton:
    #UI Button with click checking 
    
    def __init__(self, i, x, y, wdth,hght):
        #x,y is position of the of the button, wdth hght is the dimensions
        self.image = i
        self.x, self.y = x, y
        self.width, self.height = wdth,hght
    def setparams(self, x,y,wdth,hght):
        #x,y is position of the of the button, wdth hght is the dimensions
        self.x, self.y = x, y
        self.width, self.height = wdth,hght
        
    def display(self):
        # Draws our button to the screen
        imageMode(CENTER)
        image(self.image, self.x, self.y, self.width, self.height)
        
    def checkPressed(self, mouseloc):
        #checks if some mouselocation is on top of the button and returns bool
        if mouseloc[0] in range(int(self.x)-int(self.width/2), int(self.x) + int(self.width/2)) and mouseloc[1] in range(int(self.y)-int(self.height/2), int(self.y) + int(self.height/2)):
            return True
        return False

#Button holder class/namespace
class Button:
    START = None
    HELP = None
    SCORE = None
    BACK = None
    EXIT = None
    REPLAY = None
    NEXT = None
    PREV = None
class Board:
    # The class we will use for our game itself, handles input/output logic too
    gameFont = None
    def __init__(self, x,y,w, h,r,c, images, sounds):
        #xPos, yPos are location to draw at, wdth hght are dimensions, r c, is rows and columns in the board
        # images is a list of PImage objects holding all the sprites we need
        self.xPos = x
        self.yPos = y
        self.wdth = w
        self.hght = h
        self.rows = r
        self.cols = c
        self.images = images
        self.score = 0
        self.bonus = False
        self.explosions = []
        self.startframe = float("inf")
        self.lives = 0
        self.gamedone = False
        self.bonusRemaining = 0
        self.sounds = sounds
        self.beesLeft = 0
        self.name = ""
        self.lostlife = False
        self.BEESPEED = 0
        self.PENGOSPEED = 0

    def fill_board(self, numice, numbees, level):
        # Initializes game board with random generation pengo starts in center
        #Num ice is the number of ice blocks we want to add to the board (>= 3)
        self.PENGOSPEED = self.wdth // 100
        self.BEESPEED = self.PENGOSPEED * 4 // 5
        self.startframe = frameCount + frameRate*2
        self.board = []  #Board is structured as a one dimensional list of collision objects
        self.lives = 3
        board_coordinates = [(x, y) for x in range(0,self.rows) for y in range(0, self.cols)]
        board_coordinates.remove((self.cols // 2, self.rows // 2)) #this will be pengo's starting location
        item_coordinates = random.sample(board_coordinates, numice + numbees)
        diamonds = random.sample(item_coordinates[:len(item_coordinates)-3], 3) #leave the last 3 out, because those will be bees
        numEggs = 3
        eggCount = 0
        self.beesLeft = numEggs + numbees
        self.gamedone = False
        self.score = 0
        for i in range(numice):
            cur = item_coordinates[i]
            if cur not in diamonds:
                self.board.append(Block("ice", self.xPos+cur[0]*self.wdth/self.cols, self.yPos + cur[1] * self.hght/self.rows, self.wdth/self.cols, self.hght/self.rows, self.images[0], 2*self.PENGOSPEED))
                if eggCount < numEggs: #make this block an egg
                    eggCount += 1
                    self.board[-1].hasEgg = True
            else:
                self.board.append(Block("diamond", self.xPos+cur[0]*self.wdth/self.cols, self.yPos + cur[1] * self.hght/self.rows, self.wdth/self.cols, self.hght/self.rows, self.images[1], 2*self.PENGOSPEED))
            
        #Pengo and bee generation below
        pengoX = self.cols // 2
        pengoY = self.rows // 2
        self.board.append(Pengo(self.images[2], self.xPos + pengoX*self.wdth/self.cols, self.yPos+pengoY*self.hght/self.rows, self.wdth/self.cols, self.hght/self.rows, self.PENGOSPEED))
        for i in range(numice, len(item_coordinates)):
            bee = item_coordinates[i]
            self.board.append(Bee(self.images[3], self.xPos + bee[0]*self.wdth/self.cols, self.yPos + bee[1]*self.hght/self.rows, self.wdth/self.cols, self.hght/self.rows, self.BEESPEED))

    def startGame(self, r = False):
        imageMode(CORNER)
        for item in self.board:
            if isinstance(item, Block) and item.hasEgg and not r:
                item.img = self.images[4]
            item.display()
            if isinstance(item, Block) and item.hasEgg:
                item.img = self.images[0]

    def gameOver(self):
        self.sounds[0].play()
        self.sounds[0].rewind()
        self.lives -= 1
        delay(180)
        if self.lives == 0:
            delay(500)
            self.gamedone = True
        else:
            self.lostlife = True
            pengo = self.pengo()
            #run BFS to find empty restart location 
            pengoX = self.xPos + self.cols // 2 * self.wdth/self.cols
            pengoY = self.yPos + self.rows // 2 * self.hght/self.rows
            q = [(pengoX, pengoY)] #queue
            xMove = [0,0,1,-1]
            yMove = [1,-1,0,0]
            while q:
                x,y = q.pop(0)
                pengo.xPos, pengo.yPos = x,y
                pengo.newX, pengo.newY = x,y
                pengo.xMove, pengo.yMove = 0,0
                collision = pengo.move(self)
                if collision == None:
                    break
                for i in range(4):
                    q.append((x + xMove[i] * self.wdth/self.cols, y + yMove[i] * self.hght/self.rows))
            
    
    def pengo(self):
        #Returns a pointer to the Pengo
        for i in self.board:
            if isinstance(i, Pengo):
                return i
    
    def destruct(self, pointer, points):
        #Destroys some object in board, assigns points
        self.score += points
        self.explosions.append(Explosion(pointer.xPos, pointer.yPos, pointer.wdth, pointer.hght, points))
        self.board.remove(pointer)

    def movepengo(self, whichKey):
        #Calls all necessary functions for Pengo to perform a move
        if whichKey == '':
            return
        pengo = self.pengo()
        if not self.bonusRemaining: #dont let it move while the bonus animation plays
            pengo.userInput(whichKey)
        collision = pengo.move(self)
        if isinstance(collision, Bee):
            if collision.stunned:
                self.destruct(collision,400)
                self.beesLeft -= 1
            else:
                self.gameOver()
    
    def pButton(self, whichKey):
        # all functionality of p button (pushing blocks, stunning bees)
        if whichKey != "P":
            return
        pengo = self.pengo()
        projectedX, projectedY = -1, -1   #Coords of where p button is acting on
        if pengo.xPos != pengo.newX or pengo.yPos != pengo.newY:
            return
        if pengo.facing == 'S':
            xmove, ymove = 0, 1   # Movement Vector
            projectedX, projectedY = pengo.xPos, pengo.yPos + self.hght/self.rows
        elif pengo.facing == 'D':
            xmove, ymove = 1, 0
            projectedX, projectedY = pengo.xPos + self.wdth/self.cols, pengo.yPos
        elif pengo.facing == 'A':
            xmove, ymove = -1, 0
            projectedX, projectedY = pengo.xPos - self.wdth/self.cols, pengo.yPos
        elif pengo.facing == 'W':
            xmove, ymove = 0, -1
            projectedX, projectedY = pengo.xPos, pengo.yPos - self.hght/self.rows
        sameY, sameX = False, False 
        #sameX is set to true if a bee with the same x as pengo will be stunned, likewise for sameY
        if projectedX + 10 > self.xPos + self.wdth or projectedX - 10 < self.xPos:
            sameX = True
        elif projectedY + 10 > self.yPos + self.hght or projectedY - 10 < self.yPos:
            sameY = True
        for item in self.board:
            if isinstance(item, Block):
            #Room for error of 5 pixels (due to division errors)
                if abs(item.xPos - projectedX) <= 5 and abs(item.yPos - projectedY) <= 5: #this block gets pushed
                    item.xMove, item.yMove = xmove, ymove
                    collision = item.move(self)
                    if isinstance(collision, Bee):
                        self.beesLeft -= 1
                        self.destruct(collision, 400)
                    elif collision != None and item.name == "ice":
                        self.destruct(item, [0,500][item.hasEgg])
                        if item.hasEgg:
                            self.beesLeft -= 1
                    break
            elif isinstance(item, Bee) and not item.stunned:
                if abs(item.xPos - pengo.xPos) <= 10 and sameX:
                    item.stunned = 1
                elif abs(item.yPos - pengo.yPos) <= 10 and sameY:
                    item.stunned = 1
    
    def display(self):
        #call all drawing functions as well as
        #all game logic that relies on time (like bee movement and block movement and animation)
        imageMode(CORNER)
        beecount = 0
        diamonds = []
        for item in self.board:
            if isinstance(item, Block) and item.name == "diamond":
                diamonds.append(item)
            if isinstance(item, Block):
                collided = item.move(self)
                if isinstance(collided, Bee):
                    self.destruct(collided, 400)
                    self.beesLeft -= 1
            elif isinstance(item, Bee):
                beecount += 1
                item.generateMovement(self)
                collided = item.move(self)
                if isinstance(collided, Pengo):
                    self.gameOver()
                elif isinstance(collided, Block) and (collided.newX != collided.xPos or collided.newY != collided.yPos): #check if it collides with moving block
                    self.destruct(item, 400)
                    self.beesLeft -= 1
            item.display()
            if not self.bonusRemaining:
                item.animate()
        for e in self.explosions:
            if not e.display():
                self.explosions.remove(e)
        
        #hatch the eggs while there are less than 3 bees on the screen
        for item in self.board:
            if beecount == 3:
                break
            if isinstance(item, Block) and item.hasEgg:
                self.board.append(Bee(self.images[3],item.xPos, item.yPos, item.wdth, item.hght, self.BEESPEED))
                self.destruct(item, 0)
                beecount += 1    

        #check to see if diamond blocks are stacked
        if not self.bonus:
            minX, minY, maxX, maxY = float("inf"), float("inf"), float("-inf"), float("-inf")
            for diamond in diamonds:
                minX = min(minX, diamond.xPos)
                maxX = max(maxX, diamond.xPos)
                minY = min(minY, diamond.yPos)
                maxY = max(maxY, diamond.yPos)
            if abs(maxX - minX - 2 * diamonds[0].wdth) <= 10 and abs(maxY - minY) <= 10:
                self.bonus = True
            if abs(maxY - minY - 2 * diamonds[0].hght) <= 10 and abs(minX - maxX) <= 10:
                self.bonus = True   
            if self.bonus: 
                self.score += 1800
                self.bonusRemaining = 1800
                for item in self.board:
                    if isinstance(item, Bee):
                        item.stunned = 1  
                        
        #display lives, bees remaining, score, name
        sx = self.wdth // 15
        sy = self.wdth // 15
        for i in range(self.lives):
            image(self.images[5], sx + sx * i, sy, sx, sy)
        fill(255)
        textFont(self.gameFont)
        text("Bees remaining: " + str(self.beesLeft), sx, sy * 3)
        text("Player: " + self.name, sx, sy * 4)
        text("Score: " + str(self.score), sx, sy * 5)

        if self.beesLeft == 0:
            delay(600)
            self.gamedone = True       

class Sprite:
    #General reference sprite class with collision logic
    def __init__(self, img, x,y,w,h, speed):
        self.img, self.xPos, self.yPos, self.wdth, self.hght, self.speed = img,x,y,w,h,speed
        self.xMove, self.yMove = 0, 0
        self.newX, self.newY = self.xPos, self.yPos
        #xPos and yPos are current position, newX and newY are position we want to move to, xMove and yMove are movement vectors

    def collision(self, other, x, y):
        #Checks collision between self and some other sprite object
        #Room for error of 5 pixels
        if rangeOverlap(range(other.xPos + 5, other.xPos + other.wdth - 5), range(x + 5, x + self.wdth - 5)) and rangeOverlap(range(other.yPos + 5, other.yPos + other.hght - 5), range(y + 5, y + self.hght - 5)):
            return True
        return False

    def move(self, board):
        #calculate movement, looks for collisions, returns the collision (if any)
        if self.xPos != self.newX or self.yPos != self.newY or (self.xMove == 0 and self.yMove == 0 and not isinstance(self, Pengo)):
            return #we want to return if this item is in the process of moving
        self.newX = self.xPos + self.xMove * (board.wdth/board.cols)
        self.newY = self.yPos + self.yMove * (board.hght/board.rows)
        if self.newX < board.xPos or self.newY < board.yPos or self.newX + self.wdth > board.xPos + board.wdth or self.newY + self.hght > board.yPos + board.hght:
            #off the board
            self.newX = self.xPos
            self.newY = self.yPos
            self.xMove, self.yMove = 0, 0
            return -1
        for i in board.board:
            if i is self:
                continue
            if self.collision(i, self.newX, self.newY):
                if isinstance(i,Block):
                    self.xMove, self.yMove = 0, 0
                    self.newX = self.xPos
                    self.newY = self.yPos
                return i
        return None

    def animate(self):
        #Actual movement
        if self.xMove == -1 and self.xPos > self.newX:
            self.xPos = max(self.xPos - self.speed, self.newX)
        elif self.xMove == 1 and self.xPos < self.newX:
            self.xPos = min(self.xPos + self.speed, self.newX)
        elif self.yMove == -1 and self.yPos > self.newY:
            self.yPos = max(self.yPos - self.speed, self.newY)
        elif self.yMove == 1 and self.yPos < self.newY:
            self.yPos = min(self.yPos + self.speed, self.newY)      

    def display(self):
        image(self.img, self.xPos, self.yPos, self.wdth, self.hght)
        

class Block(Sprite):
    #Class for diamond and ice block objects
    EXPLOSION = []
    def __init__(self, name,x,y,w,h, image, speed):
        #Name: ice or diamond
        #xmove ymove: movement vector
        #newX, newY: Position block is trying to reach
        self.name, self.xPos, self.yPos, self.wdth, self.hght, self.speed = name,x,y,w,h, speed
        self.xMove, self.yMove = 0, 0
        self.newX, self.newY = x, y
        self.img = image
        self.hasEgg = False
        
class Pengo(Sprite):
    #Player class
    def __init__(self, img, x,y,w,h, speed):
        self.img, self.xPos, self.yPos, self.wdth, self.hght, self.speed = img,x,y,w,h,speed
        self.xMove, self.yMove = 0, 0
        self.newX, self.newY = x, y
        self.facing = 'S'
        self.isDead = False
        self.walkFrame = frameCount
        self.walking = True

    def userInput(self, whichKey):
        #Create movement vector based on user input
        if self.xPos != self.newX or self.yPos != self.newY:
            return
        if whichKey == "W":
            self.xMove, self.yMove = 0, -1
        elif whichKey == "S":
            self.xMove, self.yMove = 0, 1
        elif whichKey == "D":
            self.xMove, self.yMove = 1, 0
        elif whichKey == "A":
            self.xMove, self.yMove = -1, 0
        if whichKey == 'W' or whichKey == 'S' or whichKey == 'A' or whichKey == 'D':
            self.facing = whichKey
    def display(self):
        #special display that displays different image based on movement direction
        i = None
        if self.facing == 'S':
            i = 0
        elif self.facing == 'A':
            i = 2
        elif self.facing == 'W':
            i = 4
        elif self.facing == 'D':
            i = 6
        if self.walkFrame <= frameCount:
            self.walkFrame = frameCount + frameRate/3
            self.walking = not self.walking
        if self.walking:
            i+= 1
        image(self.img[i], self.xPos, self.yPos, self.wdth, self.hght)

class Bee(Sprite):
    def __init__(self, img, x,y,w,h, speed):
        self.img, self.xPos, self.yPos, self.wdth, self.hght, self.speed = img,x,y,w,h,speed
        self.xMove, self.yMove = 0, 0
        self.previous = [0,0]
        self.newX, self.newY = x, y
        self.stunned = 0
        self.walkFrame = frameCount
        self.walking = True
        self.facing = 'S'


    def generateMovement(self, board):
        #choose random movement, but make it more likely to choose previous direction
        if self.xPos != self.newX or self.yPos != self.newY:
            return
        
        if board.bonusRemaining:
            return

        if self.stunned == 120:
            self.stunned = 0

        if self.stunned:
            self.xMove, self.yMove = 0, 0
            self.stunned += 1
            return
        
        opposite = [self.previous[0] * -1, self.previous[1] * -1] # make it impossible to choose opposite direction
        
        #possible is a list of movement vectors
        possible = [[0,-1], [0,1], [1,0], [-1,0], self.previous, self.previous, self.previous, self.previous, self.previous, self.previous, self.previous]
        possible.remove(opposite)
        chosen = random.choice(possible)
        self.xMove, self.yMove = chosen[0], chosen[1]
        if chosen == [0,-1]:
            self.facing = 'W'
        elif chosen == [0,1]:
            self.facing = 'S'
        elif chosen == [1,0]:
            self.facing = 'D'
        elif chosen == [-1,0]:
            self.facing = 'A'
        self.previous = chosen

    def display(self):
        if self.stunned:
            image(self.img[-1], self.xPos, self.yPos, self.wdth, self.hght)
            return
        i = None
        if self.facing == 'S':
            i = 0
        elif self.facing == 'A':
            i = 2
        elif self.facing == 'W':
            i = 4
        elif self.facing == 'D':
            i = 6
        if self.walkFrame <= frameCount:
            self.walkFrame = frameCount + frameRate/3
            self.walking = not self.walking
        if self.walking:
                i+= 1
        image(self.img[i], self.xPos, self.yPos, self.wdth, self.hght)
