import pyxel

class Ball:
    speed=1
    point=0
    miss=0
    gameover_flag=False

    def _init_(self):
        self.x = pyxel.rndi(0,199)
        self.y = 0 
        angle = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)
        self.score_flags = [True]     
    
    def move(self):
        self.x += self.vx * Ball.speed
        self.y += self.vy * Ball.speed
        if (self.x < 0 and self.vx < 0) or (self.x > 200 and self.x > 0):
          self.vx *= -1  

class Pad:
    def __init__(self):
        self.x = 100

    pyxel.init(200, 200)

    pyxel.sound(0).set(notes='A2C3', tones='TT', volumes='33', effects='NN', speed=10)
    pyxel.sound(1).set(notes='B3C2', tones='TT', volumes='33', effects='NN', speed=10)

    balls = [Ball()]
    pad = Pad()

    def update():
        global balls, Pad
        if Ball.gamover_flag:
            return
        pad.x = 
