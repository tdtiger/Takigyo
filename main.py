import pyxel
import random

SCREEN_WIDTH = 128
SCREEN_HEIGHT = 192

PLAYER_U = 0
PLAYER_V = 0
PLAYER_W = 8
PLAYER_H = 16

LOG_U = 16
LOG_V = 0
LOG_W = 8
LOG_H = 8

LOVE_U = 24
LOVE_V = 0
LOVE_W = 8
LOVE_H = 8

MONEY_U = 32
MONEY_V = 0
MONEY_W = 8
MONEY_H = 8

SCENE_TITLE = "title"
SCENE_PLAY = "play"
SCENE_GAMEOVER = "gameover"

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title = "Takigyo Simulator", fps = 60)
        pyxel.load("my_resource.pyxres")
        pyxel.mouse(True)
        self.scene = SCENE_TITLE

        self.reset_game()

        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.score = 0
        self.is_gameover = False

        self.player_x = SCREEN_WIDTH // 2 - PLAYER_W // 2
        self.player_y = SCREEN_HEIGHT - PLAYER_H - 5
        self.last_mouse_x = SCREEN_WIDTH // 2 - PLAYER_W // 2
        self.last_mouse_y = 0

        self.max_spirit = 100
        self.spirit = self.max_spirit
        self.vanish_timer = 0

        self.particles = []
        for _ in range(50):
            self.particles.append([random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(2, 5)])

        self.logs = []
        for _ in range(8):
            self.logs.append(self.create_falling_object(LOG_W))

        self.loves = []
        for _ in range(2):
            self.loves.append(self.create_falling_object(LOVE_W))

        self.moneys = []
        for _ in range(1):
            self.moneys.append(self.create_falling_object(MONEY_W))
    
    def create_falling_object(self, width):
        return{
            "x": random.randint(0, SCREEN_WIDTH - width),
            "y": random.randint(-200, -20),
            "speed": random.randint(1, 3),
            "active": True
        }

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_background()

        if self.scene == SCENE_TITLE:
            self.update_title()
        elif self.scene == SCENE_PLAY:
            self.update_play()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover()

        if self.is_gameover:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.reset_game()
            return

    def update_background(self):
        for p in self.particles:
            p[1] += p[2]
            if p[1] > SCREEN_HEIGHT:
                p[1] = 0
                p[0] = random.randint(0, SCREEN_WIDTH)

    def update_title(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.reset_game()
            self.scene = SCENE_PLAY

    def update_play(self):
        if self.vanish_timer > 0:
            self.vanish_timer -= 1
        else:
            if self.spirit < self.max_spirit:
                self.spirit += 0.5

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.last_mouse_x = pyxel.mouse_x
            self.last_mouse_y = pyxel.mouse_y
            mx = pyxel.mouse_x
            my = pyxel.mouse_y

            for love in self.loves:
                if(love["x"] - 4 <= mx <= love["x"] + LOVE_W + 4) and (love["y"] - 4 <= my <= love["y"] + LOVE_H + 4):
                    love["y"] = -100
                    love["x"] = random.randint(0, SCREEN_WIDTH - LOVE_W)
                    self.score += 100
                    pyxel.play(0, 0)

            for money in self.moneys:
                if(money["x"] - 4 <= mx <= money["x"] + MONEY_W + 4) and (money["y"] - 4 <= my <= money["y"] + MONEY_H + 4):
                    money["y"] = -100
                    money["x"] = random.randint(0, SCREEN_WIDTH - MONEY_W)
                    self.score += 100
                    pyxel.play(0, 0)
        
        elif pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            delta_x = pyxel.mouse_x - self.last_mouse_x
            self.player_x += delta_x
            self.player_x = max(0, min(self.player_x, SCREEN_WIDTH - PLAYER_W))

            delta_y = pyxel.mouse_y - self.last_mouse_y
            if delta_y < -10 and self.spirit >= self.max_spirit:
                self.vanish_timer = 60
                self.spirit = 0
        
            self.last_mouse_x = pyxel.mouse_x
            self.last_mouse_y = pyxel.mouse_y

        for log in self.logs:
            log["y"] += log["speed"]
            if log["y"] > SCREEN_HEIGHT:
                log["x"] = random.randint(0, SCREEN_WIDTH - LOG_W)
                log["y"] = random.randint(-100, -10)
            
            if (self.vanish_timer == 0 and 
            self.player_x < log["x"] + LOG_W and self.player_x + PLAYER_W > log["x"] and
            self.player_y < log["y"] + LOG_H and self.player_y + PLAYER_H > log["y"]):
                self.scene = SCENE_GAMEOVER

        for love in self.loves:
            love["y"] += love["speed"]
            if love["y"] > SCREEN_HEIGHT:
                love["y"] = random.randint(-100, -10)
                love["x"] = random.randint(0, SCREEN_WIDTH - LOVE_W)
                self.score = max(0, self.score - 50)
                self.spirit = max(0, self.spirit - 10)

        for money in self.moneys:
            money["y"] += money["speed"]
            if money["y"] > SCREEN_HEIGHT:
                money["y"] = random.randint(-100, -10)
                money["x"] = random.randint(0, SCREEN_WIDTH - MONEY_W) 
                self.score = max(0, self.score - 50)
                self.spirit = max(0, self.spirit - 10)
    
    def update_gameover(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.scene = SCENE_TITLE

    def draw(self):
        pyxel.cls(1)
        self.draw_background()

        if self.scene == SCENE_TITLE:
            self.draw_title()
        elif self.scene == SCENE_PLAY:
            self.draw_play()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_play()
            self.draw_gameover()

    def draw_background(self):
        for p in self.particles:
            color = 6 if p[2] < 4 else 7
            pyxel.line(p[0], p[1], p[0], p[1] + 2, color)
    
    def draw_title(self):
        pyxel.text(52, 60, "TAKIGYO", 7)
        pyxel.text(60, 70, "SIM", 7)

        if pyxel.frame_count % 30 < 15:
            pyxel.text(42, 120, "TAP TO START", 10)

        pyxel.text(10, 180, "Created by Pyxel", 5)
    
    def draw_play(self):
        bar_x = SCREEN_WIDTH - 8
        bar_y = 50
        bar_h = 60
        pyxel.rectb(bar_x, bar_y, 4, bar_h, 13)
        current_h = int(bar_h * (self.spirit / self.max_spirit))
        color = 12 if self.spirit < self.max_spirit else 10
        pyxel.rect(bar_x + 1, bar_y + bar_h - current_h, 2, current_h, color)

        if self.vanish_timer > 0:
            if pyxel.frame_count % 2 == 0:
                pyxel.blt(self.player_x, self.player_y, 0, PLAYER_U, PLAYER_V, PLAYER_W, PLAYER_H, 0)
        else:
            pyxel.blt(self.player_x, self.player_y, 0, PLAYER_U, PLAYER_V, PLAYER_W, PLAYER_H, colkey = 0)

        for log in self.logs:
            pyxel.blt(log["x"], log["y"], 0, LOG_U, LOG_V, LOG_W, LOG_H, 0)
        
        for love in self.loves:
            pyxel.blt(love["x"], love["y"], 0, LOVE_U, LOVE_V, LOVE_W, LOVE_H, 0)
        
        for money in self.moneys:
            pyxel.blt(money["x"], money["y"], 0, MONEY_U, MONEY_V, MONEY_W, MONEY_H, 0)
        
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)

    def draw_gameover(self):
        pyxel.text(45, 80, "GAME OVER", 8)
        pyxel.text(45, 90, f"SCORE: {self.score}", 7)

        if pyxel.frame_count % 30 < 15:
            pyxel.text(40, 130, "TAP TO TITLE", 10)
        
App()