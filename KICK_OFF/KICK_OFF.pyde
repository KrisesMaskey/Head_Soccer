add_library('minim')
import random, os
from ddf.minim import Minim
from random import randint

#GET PATH OF THE FOLDER
path = os.getcwd()

#INITIALIZING MINIM
minim = Minim(this)

#GLOBAL VARIABLES TO EXPORT SOUND
click_sound = None; whistle = None ; bounce_sound = None; kick_sound = None; goal_sound = None

#GLOBAL VARIABLES FOR BACKGROUND IMAGES & BUTTONS (IMAGE LOADED IN SETUP)
bg = None ; help_button = None ; img = None; play_button = None ; back_button = None; close_button = None; start_button = None; high_score_screen = None; top_score = None; control_screen = None; game_over_screen = None; info_screen = None

#GLOBAL VARIABLE SCREEN TO CHANGE SCREENS UPON BUTTON CLICK
screen = 0

#WIDTH & HEIGHT OF WINDOW
WIDTH = 1280
HEIGHT = 720

#PLAYER SPRITE LIST WITH DIMENSION AND FRAMES
PLAYER_IDLE = ["detective_idle.png", "robot_idle.png", "ninja_idle.png", "ninja_female_idle.png", "jack_idle.png"]
PLAYER_MOVE = ["detective.png", "robot.png", "ninja.png", "ninja_female.png", "jack.png"]
PLAYER_KICK = ["detective_kick.png", "robot_kick.png", "ninja_kick.png","ninja_female_kick.png", "jack_kick.png"]
PLAYER_DIM = [[104, 126, 10], [142,139,8], [91,114, 10], [94, 130, 10],[104, 137, 8]]

#CHOOSE RANDOM PLAYER SPRITE
rand_player = random.sample(range(0, 5), 2)

#HITBOX FOR PLAYER ONE AND TWO
hitbox_one = False
hitbox_two = False
hitbox_jump = False

#VARIABLE CNT TO INTERCHANGE TURN WHEN GOAL IS SCORED
cnt = 0

#GOAL COUNT AND DETECTION
GOAL_FLAG = False
GOAL_COUNT = [0,0]

#BALL CLASS
class Ball: 
    #CONSTRUCTOR  
    def __init__(self, r, img_name, img_w, img_h, num_frames):
        self.r = r
        self.x = 640 
        self.y = 100 
        self.vy = 0
        self.vx = 0
        self.g = 645
        self.img = loadImage(path + "/Ball/" + img_name)
        self.img_w = img_w
        self.img_h = img_h
        self.num_frames = num_frames
        self.frame = 0
        self.airres = 0.0001
        self.friction = 0.175
        self.dir = RIGHT
        self.turn = 0
        self.temp = 1
    
    #TURN METHOD TO ALTERNATE TURNS
    def Turn(self, cnt):
        self.turn = (cnt + 1) % 2
        if self.turn == 0:
            self.vx = 6
        elif self.turn == 1:
            self.vx = -6
            
    #DISPLAY METHOD FOR THE BALL CLASS     
    def display(self):
        self.move()
        imageMode(CORNER)

        #Used to load image and display sprite
        if self.dir == RIGHT:
            image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
        elif self.dir == LEFT: 
            image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h, (self.frame + 1) * self.img_w, 0, self.frame * self.img_w, self.img_h)       
    
        #ellipseMode(CORNER)               
        #noFill()
        #stroke(255, 0, 0)
        #strokeWeight(2)
        #ellipse(self.x - self.img_w//2, self.y - self.img_h//2, self.r * 2, self.r * 2)

    #GRAVITY METHOD FOR THE BALL SO THAT THE BALL DROPS AND THEN BOUNCES 
    def gravity(self):
        if self.y + self.img_h//2 >= self.g:
            self.vy *= -1
            self.vy -= self.vy * self.friction
        else:
            self.vy += 0.5
            self.vy -= self.vy * self.airres 
            
   #MOVE METHOD TO UPDATE MOVEMENT OF BALL                     
    def move(self):
         self.gravity()
         global GOAL_FLAG, GOAL_COUNT
         
    #MAKE THE BALL SPIN ACCORDING TO FRAMERATE    
         if frameCount % 5 == 0 and self.vx != 0 and self.vy < 550:
            self.frame = (self.frame + 1) % self.num_frames
            
     #UPDATE LOCATION   
         self.y += self.vy 
         self.x += self.vx 
            
    #BOUNCE OF EDGES, CROSS BAR AND GOAL DETECTION FOR BOTH POST
    
        #BOUNCE OFF CROSS BAR LEFT GOAL POST
         if 0<self.x - self.r and self.x - self.r<128 and 440 > self.y and self.y > 370:
             self.vx = 10
             self.vy = -10
        #GOAL DETECTION LEFT GOAL POST
         elif  self.x - self.r < 90 and 425 < self.y + self.r  < 650 and self.temp==1:
            GOAL_FLAG = True
            self.temp = 0
            GOAL_COUNT[0] += 1
            self.vy = 1
            self.vx = 0
        #BOUNCE OF SCREEN EDGES (LEFT)
         elif self.x - self.r - 5< 0:
            self.vx = 15  
         
        #BOUNCE OFF CROSS BAR RIGHT GOAL POST
         if WIDTH > self.x + self.r and self.x + self.r>1150 and 440 > self.y and self.y > 370:
             self.vx = 10
             self.vy = -10
        #GOAL DETECTION RIGHT GOAL POST    
         elif  (self.x + self.r > 1270 or self.x + self.r > 1200) and 425 < self.y + self.r  < 650 and self.temp == 1:
            self.temp = 0
            GOAL_FLAG = True
            GOAL_COUNT[1] += 1
            self.vy = 1
            self.vx = 0
        #BOUNCE OF SCREEN EDGES (RIGHT)
         elif self.x + self.r + 5 > WIDTH:
             self.vx = -15

#PLAYER CLASS
class Player:
    #CONSTRUCTOR
    def __init__(self, x, y, r, g, img, w, h, num_frames):
        self.img_name = img
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.vy = 0
        self.vx = 0
        self.imgx = loadImage(path + "/Player/" + img)
        self.img_w = w
        self.img_h = h
        self.num_frames = num_frames
        self.frame = 0
        self.flag = False
        self.dir = RIGHT
    
    #INITIALIZE GRAVITY FOR PLAYERS
    def gravity(self):
        if self.y + self.r >= self.g:
            self.vy = 0
        else:
            self.vy += 0.3
            if self.y + self.r + self.vy > self.g:
                self.vy = self.g - (self.y + self.r)
                
    #UPDATE LOCATION OF PLAYERS
    def update(self):
        self.gravity()
        self.y += self.vy
        self.x += self.vx
        
    #DISPLAY SPRITE MOVEMENT ACCORDING TO KEY PRESSED
    def display(self):
        self.update()
        if self.dir == RIGHT or self.dir == ord('d'):
            image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
        elif self.dir == LEFT or self.dir == ord('a'):
            image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h, (self.frame + 1) * self.img_w, 0, self.frame * self.img_w, self.img_h)
    
#PLAYER 1 CLASS THAT INHERITS FROM PLAYER CLASS
class Player_One(Player):
    #CONSTRUCTOR
    def __init__(self, x, y, r, g, img, w, h, num_frames):
        Player.__init__(self, x, y, r, g, img, w, h, num_frames)
        self.key_handler = {LEFT:False, RIGHT:False, UP:False, 'M':False}
        self.idle_img = loadImage(path + "/Player/" + PLAYER_IDLE[rand_player[0]])
        self.move_img = loadImage(path + "/Player/" + PLAYER_MOVE[rand_player[0]])
        self.kick_img = loadImage(path + "/Player/" + PLAYER_KICK[rand_player[0]])
        self.score = GOAL_COUNT[0]
        self.dir = LEFT
    
    #UPDATE MOVEMENT ACCORDING TO KEYPRESSED 
    def update(self):
        global rand_player, hitbox_one, hitbox_two
        self.gravity()
        
        #CHANGE SPRITE IMAGE FROM IDLE TO MOVING
        if keyPressed==True and (game.player1.key_handler[LEFT] == True or game.player1.key_handler[RIGHT] == True):
            self.img = self.move_img
        else:
            self.img = self.idle_img
        
        #PLAYER 1 MOVEMENT
        if self.key_handler[LEFT] == True and self.x - self.r > 60 and hitbox_one == False:
            self.vx = -5
            self.dir = LEFT
        elif self.key_handler[RIGHT] == True and self.key_handler[LEFT] == False and self.x + self.r < 1230 and hitbox_two == False:
            self.vx = 5
            self.dir = RIGHT
        else:
            self.vx = 0
            
        #PLAYER 1 JUMP
        if self.key_handler[UP] == True and self.y + self.r == self.g:
            self.vy = -10
            
        #PLAYER 1 SHOOT IMG
        if self.key_handler['M'] == True and (self.key_handler[LEFT] == False and self.key_handler[RIGHT] == False):
            self.img = self.kick_img
        
        #UPDATE LOCATION
        self.y += self.vy
        self.x += self.vx
        
        #SPRITE FRAME CHANGE 
        if frameCount%5 == 0 and self.vx != 0 and self.vy == 0:
            self.frame = (self.frame + 1) % self.num_frames
        elif self.vx == 0:
            self.frame = 0
            
#INITIALIZE PLAYER 2 CLASS THAT INHERITS FROM PLAYER CLASS
class Player_Two(Player):
    #CONSTRUCTOR
    def __init__(self, x, y, r, g, img, w, h, num_frames):
        Player.__init__(self, x, y, r, g, img, w, h, num_frames)
        self.key_handler = {'A':False, 'D':False, 'W':False, 'SPACE': False}
        self.idle_img = loadImage(path + "/Player/" + PLAYER_IDLE[rand_player[1]])
        self.move_img = loadImage(path + "/Player/" + PLAYER_MOVE[rand_player[1]])
        self.kick_img = loadImage(path + "/Player/" + PLAYER_KICK[rand_player[1]])
        self.score = GOAL_COUNT[1]
    
    #UPDATE MOVEMENT ACCORDING TO KEYPRESSED
    def update(self):
        global rand_player, hitbox_one, hitbox_two
        self.gravity()
        
        # CHANGE SPRITE BASED ON KEY PRESS
        if keyPressed==True and (game.player2.key_handler['A'] == True or game.player2.key_handler['D'] == True):
            self.img = self.move_img
        else:
            self.img = self.idle_img
        
        # MOVEMENT BASED ON KEY HANDLER
        if self.key_handler['A'] == True and self.x - self.r > 60 and hitbox_two == False:
            self.vx = -5
            self.dir = ord('a')
        elif self.key_handler['D'] == True and self.key_handler['A'] == False and self.x + self.r < 1230 and hitbox_one == False:
            self.vx = 5
            self.dir = ord('d')
        else:
            self.vx = 0
            
        # PLAYER 2 JUMP
        if self.key_handler['W'] == True and self.y + self.r == self.g:
            self.vy = -10
        
        # SHOW KICK SPRITE
        if self.key_handler['SPACE'] == True and (self.key_handler['A'] == False and self.key_handler['D'] == False):
            self.img = self.kick_img
        
        # UPDATE PLAYER MOVEMENT
        self.y += self.vy
        self.x += self.vx
        
        # CHANGE SPRITE FRAME ACCORDING TO FRAMECOUNT
        if frameCount%5 == 0 and self.vx != 0 and self.vy == 0:
            self.frame = (self.frame + 1) % self.num_frames
        elif self.vx == 0:
            self.frame = 0
            
#GAME CLASS
class Game():
    #CONSTRUCTOR
    def __init__(self, player):
        global cnt
        self.mins = 2
        self.sec = 59
        self.goal_post = loadImage(path + "/Goal_Post/goal_post_left.png")
        self.scoreboard = loadImage(path + "/Goal_Post/scoreboard.png")
        self.rand_player = player
        self.player1 = Player_One(950, 360, 35, 590, PLAYER_IDLE[self.rand_player[0]], PLAYER_DIM[self.rand_player[0]][0], PLAYER_DIM[self.rand_player[0]][1], PLAYER_DIM[self.rand_player[0]][2]) 
        self.player2 = Player_Two(330, 360, 35, 590, PLAYER_IDLE[self.rand_player[1]], PLAYER_DIM[self.rand_player[1]][0], PLAYER_DIM[self.rand_player[1]][1], PLAYER_DIM[self.rand_player[1]][2]) 
        self.ball = Ball(27, 'ball1.png',54, 86, 6)
        self.ball.Turn(cnt)
        
    #GAME DISPLAY
    def display(self):
        global screen, GOAL_FLAG, hitbox_one, hitbox_two
        
    # INITIALIZE TIMER
        if (frameCount ) % 60 == 59:
            if self.sec == '00':
                self.mins -= 1
                self.sec = '60'
            self.sec = int(self.sec) - 1
            if self.sec < 10:
                self.sec = "0"+str(self.sec)
    #GOAL CHECK
        if GOAL_FLAG == True:
            goal_sound.play()
            goal_sound.rewind()
            GOAL_FLAG = False
            global game, cnt
            cnt += 1
            game = Game(rand_player) 
            game.ball.Turn(cnt)  
            game.mins = self.mins
            game.sec = self.sec
            
    
    # DISPLAY GOAL POST  
        imageMode(CORNER)
        image(self.goal_post, -70, 400, 204, 240)
        image(self.goal_post, 1150, 400, 204, 240, 204,0,0,240)
        
    #DISPLAY BALL & PLAYERS
        self.ball.display()
        self.player1.display()
        self.player2.display()

    #PLAYER & BALL COLLISION
        #CHECK IF BALL IS BELOW PLAYER 
        if (self.ball.y - 42 < self.player1.y + 70 and self.ball.y > self.player1.y + 70 and self.player1.x - 60 < self.ball.x < self.player1.x + 60) or \
            (self.ball.y - 42 < self.player2.y + 70 and self.ball.y > self.player2.y + 70 and self.player2.x - 60 < self.ball.x < self.player2.x + 60):
            self.ball.vy = 20
            
        #CHECK IF BALL TOUCHES PLAYER HEAD LEFT 
        if (self.ball.y + self.ball.r > self.player1.y - 65 and self.ball.y - self.ball.r < self.player1.y - 55 and self.ball.x  < self.player1.x + 1  and self.ball.x - self.ball.r > self.player1.x - 70) or \
            (self.ball.y + self.ball.r > self.player2.y - 65 and self.ball.y - self.ball.r < self.player2.y - 55 and self.ball.x  < self.player2.x + 1  and self.ball.x - self.ball.r > self.player2.x - 70):
            self.ball.vy = -15
            self.ball.vx = -8
            
        #CHECK IF BALL TOUCHES PLAYER HEAD RIGHT
        elif (self.ball.y + self.ball.r > self.player1.y - 65 and self.ball.y - self.ball.r < self.player1.y - 55 and self.ball.x  > self.player1.x and self.ball.x + self.ball.r < self.player1.x + 70) or \
             (self.ball.y + self.ball.r > self.player2.y - 65 and self.ball.y - self.ball.r < self.player2.y - 55 and self.ball.x  > self.player2.x and self.ball.x + self.ball.r < self.player2.x + 70):
            self.ball.vy = -15
            self.ball.vx = 8
        
    #CHECK IF BALL HITS PLAYER FEET AND IF SHOOT OPTIONS ARE PRESSED
        #KICK LEFT PLAYER 1
        if (self.player1.x - 35 > self.ball.x and self.player1.x - 35 < self.ball.x + self.ball.r and self.ball.y - self.ball.r > self.player1.y and self.player1.y + 35 > self.ball.y - self.ball.r): 
            if self.player1.key_handler['M'] == True :
                kick_sound.play()
                self.ball.vy = 27
                self.ball.vx -= 10
            kick_sound.rewind()
            self.ball.vx = -5
        #KICK LEFT PLAYER 2  
        if (self.player2.x - 35 > self.ball.x and self.player2.x - 35 < self.ball.x + self.ball.r and self.ball.y - self.ball.r > self.player2.y and self.player2.y + 35 > self.ball.y - self.ball.r): 
            if self.player2.key_handler['SPACE'] == True:
                kick_sound.play()
                self.ball.vy = 27
                self.ball.vx -= 10
            kick_sound.rewind()
            self.ball.vx = -5
            
        #KICK RIGHT PLAYER 1
        if (self.player1.x  + 35 > self.ball.x - self.ball.r and self.player1.x + 35 < self.ball.x  and self.ball.y - self.ball.r > self.player1.y and self.player1.y + 35 > self.ball.y - self.ball.r): 
            if self.player1.key_handler['M'] == True :
                kick_sound.play()
                self.ball.vy = 27 
                self.ball.vx += 5
            self.ball.vx = 5
        #KICK RIGHT PLAYER 1
        if (self.player2.x  + 35 > self.ball.x - self.ball.r and self.player2.x + 35 < self.ball.x  and self.ball.y - self.ball.r > self.player2.y and self.player2.y + 35 > self.ball.y - self.ball.r): 
            if self.player2.key_handler['SPACE'] == True:
                kick_sound.play()
                self.ball.vy = 27 
                self.ball.vx += 5
            self.ball.vx = 5
            kick_sound.rewind()
        
        #REBOUND BALL IF BALL HITS PLAYER FROM LEFT SIDE
        if (self.player1.x - 35 > self.ball.x and self.player1.x - 35 < self.ball.x + self.ball.r and self.ball.y < self.player1.y + 55 and self.player1.y - 65 < self.ball.y) or \
            (self.player2.x - 35 > self.ball.x and self.player2.x - 35 < self.ball.x + self.ball.r and self.ball.y < self.player2.y + 55 and self.player2.y - 65 < self.ball.y):
            self.ball.vx = -8
            
        #REBOUND BALL IF BALL HITS PLAYER FROM RIGHT SIDE 
        if (self.player1.x  + 35 > self.ball.x - self.ball.r and self.player1.x + 35 < self.ball.x  and self.ball.y < self.player1.y + 55 and self.player1.y - 65 < self.ball.y) or \
            (self.player2.x  + 35 > self.ball.x - self.ball.r and self.player2.x + 35 < self.ball.x  and self.ball.y < self.player2.y + 55 and self.player2.y - 65 < self.ball.y):
            self.ball.vx = 8
           
        
     # CHECK IF PLAYERS COLLIDE AND PROVIDE BOOST IF THEY STEP OVER ONE ANOTHER
        #CHECK OVERHEAD COLLISION TO PROVIDE BOOST
        if  self.player1.x > self.player2.x - 60 and self.player1.x < self.player2.x + 50 and self.player1.y + 35 > self.player2.y - 70 and self.player1.y+35 < self.player2.y:
            self.player1.vy = -15 
        if  self.player2.x > self.player1.x - 60 and self.player2.x < self.player1.x + 50 and self.player2.y + 35 > self.player1.y - 70 and self.player2.y+35 < self.player1.y:#
            self.player2.vy = -15
            
        #CHECK LEFT AND RIGHT COLLISION TO STOP MOVEMENT
        if ((self.player2.x + 35) >= (self.player1.x - 35)) and self.player2.y - 32 < self.player1.y + 35 and ((self.player2.x + 35) < (self.player1.x+35)):
            hitbox_one = True
        elif (((self.player1.x + 35) >= (self.player2.x - 35)) and self.player1.y - 32 < self.player2.y + 35 and ((self.player1.x + 35) < (self.player2.x+35))):
            hitbox_two = True
        else:
            hitbox_one = False
            hitbox_two = False
        
        #RESET FLAG IF NOT COLLIDING
        if self.player1.y - 32 > self.player2.y + 35:
            hitbox_one = False
        if self.player2.y - 32 > self.player1.y + 35:
            hitbox_two = False
       
        #DISPLAY SCORE BOARD & SCORE
        imageMode(CENTER)
        image(self.scoreboard, 640, 100, 400, 300)
        textSize(30)
        fill(255,255,51)
        text(str(self.mins) + " : " + str(self.sec), 596, 67)
        textSize(60)
        fill(255,0,0)
        text(self.player2.score, 520, 165)
        text(self.player1.score, 700, 165)
        
        #CHECK GAME END IF TIME IS OVER
        if self.mins == 0 and self.sec == "00":
            print(True)
            whistle.rewind()
            HighScore(max(GOAL_COUNT))
            screen = 5
            whistle.play()
        
#FUNTION THAT UPDATES HIGHSCORE
def HighScore(goal):
    input_file = open(path + "/HighScore/HighScore.txt", "r")
    score = input_file.readline().strip()
    score = str(max(int(score),goal))
    input_file.close()
    writing_file = open(path + "/HighScore/HighScore.txt", "w")
    writing_file.write(score)
    writing_file.close()
    return score

#FUNCTION THAT INITIALIZES NEW BG AND PLAYERS WHEN GAME RESTARTS
def Restart():
    global rand_player, bg, GOAL_COUNT
    GOAL_COUNT[0] = 0
    GOAL_COUNT[1] = 0
    rand_player = random.sample(range(0, 5), 2)
    bg = loadImage(path + "/Background/stadium_" + str(randint(1,3))+".jpg")

#FUNCTION THAT CHANGES SCREEN / HOLDS EACH SCREEN'S COMPONENT
def Screens():
    global screen, game #help_button, button, img, control_screen, start_button, close_button, back_button, high_score_screen, top_score, play_button, game, game_over_screen, info_screen
    
    #START SCREEN
    if screen == 0:
        imageMode(CORNER)
        background(0,0,0)
        image(img, 0, 0, 1280, 720)
        image(play_button, 620,400,128, 130)
        image(help_button, 15,15)
        image(top_score, 757,382)
        
    #GAME DISPLAY SCREEN  
    elif screen == 1:
        global bg, whistle
        whistle.play()
        background(bg)
        image(close_button, 1220, 30)
        game.display()
    
    #CONTROL DISPLAY SCREEN
    elif screen == 4:
        background(control_screen)
        image(start_button, 1205, 15)
        image(back_button, 15,15)
    
    #GENERAL GUIDELINE SCREEN
    elif screen == 2:
        background(info_screen)
        image(close_button, 1205, 15)
    
    #HIGHSCORE SCREEN
    elif screen == 3:
        background(125,125,125)
        image(high_score_screen,0,0)
        image(close_button, 1205, 15)
        textSize(100)
        fill(255,196,12)
        text(HighScore(0),590, 580)
    
    #GAMEOVER SCREEN
    elif screen == 5:
        background(game_over_screen)
        textSize(100)
        fill(255,255,255)
        text(game.player2.score, 320, 450)
        text(game.player1.score, 930, 450)
        #RESTART
        if keyPressed == True and key == 'r':
            Restart()
            game = Game(rand_player)
            screen = 1
        
#INITIALIZE VARIABLE GAME THAT IS AN INSTANCE OF GAME CLASS        
game = Game(rand_player)

#SETUP FUNCTION THAT INITALIZES SCREEN SIZE & LOADS IMAGES
def setup():
    global bg, screen, help_button, button, img, control_screen, start_button, close_button, back_button, high_score_screen, top_score, play_button, click_sound, whistle, kick_sound, game_over_screen, info_screen, goal_sound
    size(WIDTH, HEIGHT)
    
    #LOAD IMAGES
    bg = loadImage(path + "/Background/stadium_" + str(randint(1,3))+".jpg")
    help_button = loadImage(path + "/Buttons/Help.png")
    play_button = loadImage(path + "/Buttons/play_button.png")
    img = loadImage(path + "/Background/start_screen.jpg")
    top_score = loadImage(path + "/Buttons/highscore.png")
    control_screen = loadImage(path + "/Background/Controls.png")
    start_button = loadImage(path + "/Buttons/Start.png")
    close_button = loadImage(path + "/Buttons/Cross.png")
    back_button = loadImage(path + "/Buttons/Back.png")
    high_score_screen = loadImage(path + "/Background/HighScore.png")
    game_over_screen = loadImage(path + "/Background/gameover.png")
    info_screen = loadImage(path + "/Background/info.png")
    rectMode(CENTER)
    
    #LOAD SOUND
    bg_sound = minim.loadFile(path + "/Sounds/bg_sound.mp3")
    bg_sound.loop()
    click_sound = minim.loadFile(path + "/Sounds/click1.mp3")
    whistle = minim.loadFile(path + "/Sounds/whistle.mp3")
    goal_sound = minim.loadFile(path + "/Sounds/goal.wav")
    kick_sound = minim.loadFile(path + "/Sounds/hit.mp3")
    
#DRAW FUNCTION
def draw():
    Screens()

#MFUNCTION THAT DETECTS MOUSE CLICK ON SPECIFIC PART OF SCREEN WHICH COORDINATES SCREEN CHANGE
def mousePressed():
    global screen
    if (mouseX > 652 and mouseX < 730 and mouseY > 415 and mouseY < 515 and screen == 0):
        click_sound.play()
        # CONTROL SCREEN
        screen = 4
        click_sound.rewind()
        
    if mouseX > 18 and mouseX < 68 and mouseY > 17 and mouseY < 67:
        click_sound.play()
        # GENERAL GUIDELINE/ INFO SCREEN
        if screen == 0:
            screen = 2
            
        # START SCREEN
        elif screen == 4:
            screen = 0
        click_sound.rewind()
    
    if (mouseX > 752 and mouseX < 830 and mouseY > 377 and mouseY < 460 and screen == 0):
        click_sound.play()
        # HIGH SCORE SCREEN
        screen = 3
        click_sound.rewind()
    
    if (mouseX > 1200 and mouseX < 1235 and mouseY > 2 and mouseY < 55):
        if screen == 1:
            whistle.rewind()
            whistle.play()
            click_sound.play()
            # GAME OVER SCREEN
            screen = 5
            click_sound.rewind()
    
    if (mouseX > 1210 and mouseX < 1250 and mouseY > 17 and mouseY < 67):
        if(screen == 3 or screen == 2):
            click_sound.play()
            # START SCREEN
            screen = 0
            click_sound.rewind()
            
        if screen == 4:
            click_sound.play()
            # GAME DISPLAY SCREEN
            screen = 1
            click_sound.rewind()
    
#KEYPRESSED FUNCTION THAT UPDATES KEY DIRECTORY ACCORDING TO KEY PRESSED    
def keyPressed():
    # KEY PRESSED FOR PLAYER 1
    if keyCode == LEFT:
        game.player1.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.player1.key_handler[RIGHT] = True
    elif keyCode == UP:
        game.player1.key_handler[UP] = True
    elif key == 'm':
        game.player1.key_handler['M'] = True
        
    # KEY PRESSED FOR PLAYER 2
    if key == 'w':
        game.player2.key_handler['W'] = True
    elif key == 'a':
        game.player2.key_handler['A'] = True
    elif key == 'd':
        game.player2.key_handler['D'] = True
    elif key == ' ':
        game.player2.key_handler['SPACE'] = True

#CHECK KEY RELEASED
def keyReleased():
    # PLAYER 1
    if keyCode == LEFT:
        game.player1.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.player1.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.player1.key_handler[UP] = False
    elif key == 'm':
        game.player1.key_handler['M'] = False
    
    #PLAYER 2
    if key == 'w':
        game.player2.key_handler['W'] = False
    elif key == 'a':
        game.player2.key_handler['A'] = False
    elif key == 'd':
        game.player2.key_handler['D'] = False
    elif key == ' ':
        game.player2.key_handler['SPACE'] = False
