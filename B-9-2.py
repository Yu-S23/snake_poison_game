import pyxel

pyxel.init(200,200)

ballx = pyxel.rndi(0,199)
bally = 0
angle = pyxel.rndi(30, 150)
vx = pyxel.cos(angle)
vy = pyxel.sin(angle)
padx = 100
speed = 1
point = 0 
point_flag = True
pyxel.sound(0).set(notes='A2C3', tones='TT', volumes='33', effects='NN', speed=10)




def update():
    global ballx, bally, vx, vy, padx, speed, point, point_flag, angle 
    ballx += vx * speed 
    bally += vy * speed 
    padx = pyxel.mouse_x
    
    if bally>=200:
        ballx = pyxel.rndi(0,199)
        bally = 0
        speed+=1 
        point_flag = True
        
    
    if (ballx >= 200) or (ballx <= 0) :
        vx *=-1

    if bally>=195 and padx-20<= ballx <=padx+20 and point_flag:
         point+=1
         point_flag = False 
         pyxel.play(0,0)

    



def draw():
    global ballx, bally, vx, vy, padx, speed, point, point_flag
    pyxel.cls(7)
    pyxel.circ(ballx, bally, 10, 6)
    pyxel.rect(padx-20, 195, 40, 5, 14)
    pyxel.text(10, 10,"point:"+str(point), 14)
   
pyxel.run(update, draw)
