'''
Student Name: Amiva Pal
Game title: Maze
Period: 6/7
Features of Game: Uses functional decompostion to draw a scene
'''

import pygame, sys, math, random                                #pulls in the special code functions for pygame
pygame.init()                                           #initialize game engine
clock = pygame.time.Clock()
w=700                                                   #Open and set window size
h=w
xu=w/24
yu = xu
#must code graphics to auto resize based on window size
size=(w,h)
surface = pygame.display.set_mode(size)

pygame.display.set_caption("Maze")          #set window title

#declare global variables here

BLACK    = (   0,   0,   0)                             #Color Constants 
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
BROWN    = (  96,  70,  16)
YELLOW   = ( 237, 230,  33)
SPEED = 5
pygame.time.set_timer(pygame.USEREVENT,1000)
playerRect = pygame.Rect(2*xu,3*yu,42,42)
playerImage0 = pygame.image.load("leviathan.png")
playerImage = pygame.transform.scale(playerImage0,(42,42))
gemImage = pygame.image.load("gem1.png")
#other global variables (WARNING: use sparingly):

horWalls = [pygame.Rect(2*xu,5*yu,5*yu,2*yu), pygame.Rect(17*xu,14*yu,6*xu,2*yu), pygame.Rect(18*xu,4*yu,3*xu,2*yu), pygame.Rect(15*xu,18*yu,5*xu,1*yu), pygame.Rect(2*xu,14*yu,7*xu,2*yu), pygame.Rect(2*xu,14*yu,7*xu,2*yu), pygame.Rect(2*xu,18*yu,5*xu,1*yu), pygame.Rect(11*xu,2*yu,2*xu,2*yu), pygame.Rect(6*xu,9*yu,10*xu,2*yu)]
vertWalls = [pygame.Rect(15*xu,20*yu,2*xu,6*yu), pygame.Rect(11*xu,6*yu,2*xu,13*yu)]
borderWalls = [pygame.Rect(0,0,w,w/12), pygame.Rect(w-w/12+1,0,w/12,h), pygame.Rect(0,h-w/12+1,w,w/12), pygame.Rect(0,0,w/12,h)]
exitRect = pygame.Rect(20*xu,22*yu,2*xu,2*yu)


#clock = pygame.time.Clock()                            # Manage timing for screen updates
                                                        # Uncomment when timing/animation is needed
def showMessage(words, size, font, x, y, color, bg = None):
    text_font = pygame.font.SysFont(font, size, True, False)
    text = text_font.render(words, True, color, bg)
    textBounds = text.get_rect()
    textBounds.center = (x, y)    
    
    #return bounding rectangle for click detection
    return text, textBounds


    
def drawMaze():
    
    for wall in(horWalls):
        pygame.draw.rect(surface, BLACK, wall, 0)
    for wall in(vertWalls):
        pygame.draw.rect(surface, BLACK, wall, 0)
        
    for wall in(borderWalls):
        pygame.draw.rect(surface, BLACK, wall, 0)
    pygame.draw.rect(surface, RED, exitRect,0)
    surface.blit(playerImage,playerRect)


def placeGems():
    gems = []
    while len(gems)<20:
        x = random.randint(0,w-64)
        y = random.randint(0,h-64)
        tempgem = (pygame.Rect(x,y,64,64))
        if not collidesWithWall(tempgem):
            gems.append(tempgem)
    return gems

def movePlayer(keys,playerRect,gameOver):
    if not gameOver:
        
        if keys[pygame.K_LEFT]:
            playerRect.left -= SPEED
            if collidesWithWall(playerRect):
                playerRect.left+=SPEED
        if keys[pygame.K_RIGHT]:
            playerRect.right += SPEED
            if collidesWithWall(playerRect):
                playerRect.right -= SPEED
        if keys[pygame.K_UP]:
            playerRect.top -= SPEED
            if collidesWithWall(playerRect):
                playerRect.top += SPEED
        if keys[pygame.K_DOWN]:
            playerRect.bottom += SPEED
            if collidesWithWall:
                while collidesWithWall(playerRect):
                    playerRect.bottom -= 1
        
        #if keys[pygame.K_LEFT]:
            #playerRect.left-=SPEED
        #if keys[pygame.K_RIGHT]:
            #playerRect.right+=SPEED
        #if keys[pygame.K_UP]:
            #playerRect.top-=SPEED
        #if keys[pygame.K_DOWN]:
            #playerRect.bottom+=SPEED

def collidesWithWall(playerRect):
    for wall in (horWalls):
        if playerRect.colliderect(wall):
            return True
    for wall in (vertWalls):
        if playerRect.colliderect(wall):
            return True
    for wall in (borderWalls):
        if playerRect.colliderect(wall):
            return True
    return False

def drawGems(gems):
    for gem in gems:
        surface.blit(gemImage, gem)
    
def gemsTaken(playerRect,gems):
    gemTook = playerRect.collidelist(gems)
    if gemTook != -1:
        del gems[gemTook]
        sound = pygame.mixer.Sound('pickup.wav')
        sound.play()        
        
def drawScreen(gems, seconds, gameOver):
    drawMaze()
    drawGems(gems)
    gemsTaken(playerRect, gems)
    secondsText, secondsBounds = showMessage("Timer: " + str(seconds), 20, "Consolas", w/2, h/15, WHITE)
    surface.blit(secondsText,secondsBounds) 
    
    
    if gameOver == True and playerRect.colliderect(exitRect)==True:
        goText, goBounds = showMessage("MISSION COMPLETED", 50, "Consalas", w/2, h/2, BLUE)
        surface.blit(goText,goBounds)   
    elif seconds == 0:
        pygame.time.set_timer(pygame.USEREVENT,0)
        gameOver=True
        secText, secBounds = showMessage("OOF you ran out of time", 50, "Consalas", w/2, h/2, RED)
        surface.blit(secText,secBounds)
        
'''
def takeGems(gemsList):

    for gem in  gemsList:
        if gem.colliderect(playerRect):
            gemsList.remove(gem)
                                                                   
return gemsList
'''
# -------- Main Program Loop -----------
def main():
    gameOver = False
    seconds = 14
    gems = placeGems()
    #every program should have a main function
                                                        #other functions go above main
    rectangle = playerRect
    #declare local game variables here 
    
    
    while (True):
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():                #get all events in the last 1/60 sec & process them
            
            if ( event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
                pygame.quit();                          #for ending the game & closing window
                sys.exit();
            if event.type==pygame.USEREVENT and gameOver==False:
                seconds -= 1
                
        
            # if your program has a button, mouse, or keyboard interaction, code goes at this indentation level
        
        # ongoing game logic that occurs ever 1/60 second goes @ this indentation level
        
        if not gameOver:
            movePlayer(keys, playerRect, gameOver)
            if seconds == 0:
                gameOver=True
            if len(gems)==0:
                if playerRect.colliderect(exitRect):
                    gameOver = True
           
        
      
        surface.fill((WHITE))                             #set background color
        
        #drawing code goes here
        
        
        drawScreen(gems, seconds, gameOver)
        
        clock.tick(60)                                  #Change FPS - frames per sec- when animating
        pygame.display.update()                          #updates the screen- usually in main
        
        
        
            
main()                                                   #this calls the main function to run the program
