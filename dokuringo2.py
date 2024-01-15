from collections import deque, namedtuple
import pyxel
import random 
import time

Point = namedtuple("Point", ["x", "y"])

COL_BACKGROUND = 3
COL_BODY = 11
COL_HEAD = 7
COL_DEATH = 8
COL_APPLE = 8
COL_POISON_APPLE = 13  # 毒りんごの色

TEXT_DEATH = ["GAME OVER", "(Q)UIT", "(R)ESTART"]
COL_TEXT_DEATH = 0
HEIGHT_DEATH = 5

WIDTH = 40
HEIGHT = 50

HEIGHT_SCORE = pyxel.FONT_HEIGHT
COL_SCORE = 6
COL_SCORE_BACKGROUND = 5

UP = Point(0, -1)
DOWN = Point(0, 1)
RIGHT = Point(1, 0)
LEFT = Point(-1, 0)

START = Point(5, 5 + HEIGHT_SCORE)

POISON_APPLE_TIMEOUT=15 #毒りんごタイムアウト

class Snake:
    def __init__(self):#ゲームの初期設定
        pyxel.init(WIDTH, HEIGHT, title="Snake!", fps=12, display_scale=20, capture_scale=20)
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):#ゲームの初期化（スコア、位置、方向）
        self.direction = RIGHT
        self.snake = deque()
        self.snake.append(START)
        self.death = False
        self.score = 0
        self.poisoned = False
        self.poison_apples=[]
        self.poison_apples_visible = False 
        self.eaten_apples=0
        self.last_poison_time = time.time()#毒りんごのタイムを追跡する変数
        self.generate_apple()
      

        pyxel.playm(0, loop=True)

    def update(self):#メインループ（スネイクの方向更新、りんごの取得、毒りんご処理）
        if not self.death:
            self.update_direction()
            self.update_snake()
            self.check_death()
            self.check_apple()

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            self.reset()

    def update_direction(self):#スネイクの方向を更新
        if pyxel.btn(pyxel.KEY_UP):
            if self.direction is not DOWN:
                self.direction = UP
        elif pyxel.btn(pyxel.KEY_DOWN):
            if self.direction is not UP:
                self.direction = DOWN
        elif pyxel.btn(pyxel.KEY_LEFT):
            if self.direction is not RIGHT:
                self.direction = LEFT
        elif pyxel.btn(pyxel.KEY_RIGHT):
            if self.direction is not LEFT:
                self.direction = RIGHT

    def update_snake(self):#スネイクの位置更新
        old_head = self.snake[0]
        new_head = Point(old_head.x + self.direction.x, old_head.y + self.direction.y)
        self.snake.appendleft(new_head)
        self.popped_point = self.snake.pop()

    def check_apple(self):#スネイクがりんごを食べたか判断し、食べてたらスコアの更新
        head = self.snake[0]
        if head == self.apple:
            self.snake.append(self.popped_point)
            self.generate_apple()
            pyxel.play(0,0)
            self.score += 1
        
        #毒りんごを食べた場合の処理
        for poison_apple in self.poison_apples[:]:
            if head == poison_apple:
                self.poison_apples.remove(poison_apple)
                self.handle_poison_apple()
                break 

    def generate_apple(self):#りんごの生成
        snake_pixels = set((point.x, point.y) for point in self.snake)

        while True:
            x = pyxel.rndi(0, WIDTH - 1)
            y = pyxel.rndi(HEIGHT_SCORE + 1, HEIGHT - 1)
            if (x, y) not in snake_pixels:
                self.apple = Point(x, y)
                break

        #スコアに応じて毒林檎の出現確率を変更する
        if random.random() < 0.4:
            self.poison_apples.append(self.generate_random_point())
            self.poison_apples_visible = True 
        

    def generate_random_point(self):#ランダムに画面上に生成（ほかのりんごやスネイクと重ならないように）
        occupied_pixels = set((point.x, point.y)for point in self.snake)
        occupied_pixels.add((self.apple.x, self.apple.y))#通常のりんごの位置も追加
     
        while True:
            x = pyxel.rndi(0, WIDTH - 1)
            y = pyxel.rndi(HEIGHT_SCORE + 1, HEIGHT - 1)
            point = Point(x, y)
            if point not in occupied_pixels:
                return point


    def handle_poison_apple(self):#毒りんごを食べた時の処理
        self.death = True
        #ゲームオーバーの状態にする
        pyxel.play(0,1)
        ##ゲームオーバーの音


    def check_death(self):#ゲームオーバーの条件を確認
        head = self.snake[0]
        if head.x < 0 or head.y < HEIGHT_SCORE or head.x >= WIDTH or head.y >= HEIGHT:
            self.death_event()


    def death_event(self):#ゲームオーバーの時の処理
        self.death = True
        pyxel.stop()
        pyxel.play(0, 1)


    def draw(self):#ゲームの描画
        if self.death:
            self.draw_death()#ゲームオーバー画面表示

        else:
            pyxel.cls(col=COL_BACKGROUND)
            self.draw_snake()
            self.draw_score()
            pyxel.pset(self.apple.x, self.apple.y, col=COL_APPLE)
            for poison_apple in self.poison_apples:
                pyxel.pset(poison_apple.x, poison_apple.y, col=COL_POISON_APPLE)

    def draw_snake(self):#スネイクの描画
        for i, point in enumerate(self.snake):
            colour = COL_HEAD if i == 0 else COL_BODY
            pyxel.pset(point.x, point.y, col=colour)



    def draw_score(self):#スコアの描画
        score = f"{self.score:04}"
        pyxel.rect(0, 0, WIDTH, HEIGHT_SCORE, COL_SCORE_BACKGROUND)
        pyxel.text(1, 1, score, COL_SCORE)

    def draw_death(self):#ゲームオーバー画面の描画
        pyxel.cls(col=COL_DEATH)
        display_text = TEXT_DEATH[:]
        display_text.insert(1, f"{self.score:04}")
        for i, text in enumerate(display_text):
            y_offset = (pyxel.FONT_HEIGHT + 2) * i
            text_x = self.center_text(text, WIDTH)
            pyxel.text(text_x, HEIGHT_DEATH + y_offset, text, COL_TEXT_DEATH)

    @staticmethod
    def center_text(text, page_width, char_width=pyxel.FONT_WIDTH):
        text_width = len(text) * char_width
        return (page_width - text_width) // 2

Snake()
