#New Pygame explorations
import pygame
import sys
from math import sqrt, sin, cos, degrees, radians

#colors
cSky = (66, 215, 244)
cYellow = (245, 242, 51)
GREY = (100, 100, 100)
cWHITE = (255, 255, 255)
cBLACK = (0, 0, 0)
cRED = (0, 0, 255)
cDARKRED = (198, 55, 11)

pygame.init()

class Button():
    def __init__(self, txt, location, action, bg=(255,255,255), fg=(0,0,0), size=(80, 30), font_name="Segoe Print", font_size=16):
        self.color = bg  # the static (normal) color
        self.bg = bg  # actual background color, can change on mouseover
        self.fg = fg  # text color
        self.size = size

        self.font = pygame.font.SysFont(font_name, font_size)
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, 1, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center=[s//2 for s in self.size])

        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(center=location)

        self.call_back_ = action

    def draw(self):
        self.mouseover()

        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surface, self.rect)

    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = GREY  # mouseover color

    def call_back(self):
        self.call_back_()


def mousebuttondown():
    pos = pygame.mouse.get_pos()
    print("int mousebuttondown x is: " + str(pos[0]) + ", y is: " + str(pos[1]))
    for button in buttons:
        if button.rect.collidepoint(pos):
            print("going to do callback")
            button.call_back()
            
def showScore():
    scoreFont = pygame.font.SysFont("Segoe Print", 36)
     
    text = scoreFont.render( str(autoDriveSpeed), True, cDARKRED)
    textRect = text.get_rect()
    textRect.centerx = int(sWidth * 0.10)
    textRect.centery = int(sHeight * 0.80)
    screen.blit(text, textRect)
        
        
    


sWidth = 1500
sHeight = 1000
size = (sWidth, sHeight)
FPS = 20
clock = pygame.time.Clock() #allows you to do a wait

screen = pygame.display.set_mode(size) #display
pygame.display.set_caption('My New Game')


#game images
car1_original = pygame.image.load("images/redCar.png").convert_alpha()
car1 = car1_original
bgPic = pygame.image.load("images/Track.png").convert_alpha()


#print(car1ImageSize)
car1ImageSize = car1.get_rect()
carIW = int(car1ImageSize[2] * 0.4)
carIH = int(car1ImageSize[3] * 0.4)
car1 = pygame.transform.scale(car1, (carIW, carIH) )
carAng = 0

#game initial locations and settings
carX = 100
carY = 100
carXSpeed = 0
carYSpeed = 0
cBX = 0
cBY = 0
cYX = 0
cYY = 0
siteX = 0
siteY = 0
carR = car1.get_rect()
siteLen = carR.width //2
cBLen = int(sqrt( ((carR.width //2)*(carR.width //2)) + (25*25)     ))
sepAng = 15

done = False
autoDriveTime = False
autoDriveSpeed = 3

def rot_center(image_original, rect, angle):
    global carIW, carIH
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image_original, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    rotIW = int(rot_rect[2] * 0.4)
    rotIH = int(rot_rect[3] * 0.4)
    rot_image = pygame.transform.scale(rot_image, (rotIW, rotIH) )
    #rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect

def autoDrive():
    global autoDriveTime, carXSpeed, carYSpeed, carAng
    
    if autoDriveTime == False:
        autoDriveTime = True
    else:
        autoDriveTime = False
        carXSpeed = 0
        carYSpeed = 0
        carAng = 0
    print("In Bottom of AutoDrive!! ADT is " + str(autoDriveTime))


adButton = Button("Autodrive!", (sHeight - 200, 100), autoDrive,  bg=(50, 200, 255), fg=cYellow, size=(300,100),font_size=28)
buttons = [adButton]

def moveCar():
    global carX, carY, carXSpeed, carYSpeed, cBX, cBY, cYX, cYY, siteX, siteY, autoDriveTime, carAng, autoDriveSpeed

    sa = 15
    if autoDriveTime:
        bColor = screen.get_at( (cBX, cBY) )
        yColor = screen.get_at( (cYX, cYY) )
        sColor = screen.get_at( (siteX, siteY) )

        if(yColor != cBLACK):
            #print("yColor on black: " + str(yColor.r) + ", " + str(yColor.g) + ", " + str(yColor.b) )
            if(sColor != cBLACK):
                carAng -= 20 + int(autoDriveSpeed * 0.70)
            else:
                carAng -= 10 + int(autoDriveSpeed * 0.25)
        
        if(bColor != cBLACK):
            #print("bColor on black: " + str(bColor.r) + ", " + str(bColor.g) + ", " + str(bColor.b) )
            if(sColor != cBLACK):
                carAng += 20 + int(autoDriveSpeed * 0.70)
            else:
                carAng += 10 + int(autoDriveSpeed * 0.25)

            
        carXSpeed = int(cos(radians(carAng)) * autoDriveSpeed)
        carYSpeed = int(sin(radians(carAng)) * autoDriveSpeed) * -1
        carX += carXSpeed
        carY += carYSpeed
        sa = sa + int(autoDriveSpeed * 0.20)
    else:
        carX += carXSpeed
        carY += carYSpeed

    
    siteX = carX + int(cos(radians(carAng)) * siteLen)
    siteY = carY + int(sin(radians(carAng)) * siteLen) * -1
    cBX = carX+ int(cos(radians(carAng - sa)) * cBLen)
    cBY = carY +int(sin(radians(carAng - sa)) * cBLen) * -1
    cYX = carX + int(cos(radians(carAng + sa)) * cBLen)
    cYY = carY + int(sin(radians(carAng + sa)) * cBLen) * -1



    
    
def drawCar():
    global car1, car1_original, carX, carY, carIW, carIH, cBX, cBY, cYX, cYY, siteX, siteY, carAng
    
    carR = car1.get_rect()
    car1, carR = rot_center(car1_original, carR, carAng)
    screen.blit(car1, (carX - car1.get_width() // 2, carY - car1.get_height() // 2))
    
    
    pygame.draw.circle(screen, cWHITE, (carX , carY), 10)
    pygame.draw.circle(screen, cRED, (siteX, siteY), 10, 3)
    pygame.draw.circle(screen, cYellow, (cYX, cYY), 10, 3)
    pygame.draw.circle(screen, cSky, (cBX, cBY), 10, 3)

    #testing stuff
    #carAng += 1
    #carAng = carAng % 360
    #gColor = screen.get_at( (carX, carY) )
    #print("Car at: " + str(gColor.r) + ", " + str(gColor.g) + ", " + str(gColor.b) )
    
while not done:

    # 1 -- Capture Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("MOUSEBUTTON DOWN !!!!!!!")
            mousebuttondown()

        #print(event)  #this is for bug checking
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            
            if autoDriveTime:
                autoDriveSpeed += 3
            else:
                #print("Up")
                carYSpeed -= 3
            
        if keys[pygame.K_DOWN]:

            if autoDriveTime:
                autoDriveSpeed -= 3
            else:
                #print("Down")
                carYSpeed += 3
            
        if keys[pygame.K_LEFT]:
            #print("Left")
            carXSpeed -= 3
            
        if keys[pygame.K_RIGHT]:
            #print("Right")
            carXSpeed += 3
            
        if keys[pygame.K_l]:
            #print("Right")
            carXSpeed += 3
            
        if keys[pygame.K_SPACE]:

            if autoDriveTime:
                autoDriveSpeed = 0
            else:
                #print("Space")
                carXSpeed = 0
            carYSpeed = 0
                       
        
    # 2 -- Do Game Events
    

    # 3 -- Do Window drawing stuff
    #screen.fill(skyColor)
    screen.blit(bgPic, (0,0))
    showScore()
    #code to work with button class for drawing buttons
    for button in buttons:
        button.draw()
    moveCar()
    drawCar()
    
    
    pygame.display.flip()
    clock.tick(FPS)
    




#probably redundant     
pygame.quit()
sys.exit()

