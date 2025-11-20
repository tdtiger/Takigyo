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
LOG_W = 12
LOG_H = 12

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title = "Takigyo Simulator", fps = 60)
        pyxel.load("my_resource.pyxres")
        pyxel.mouse(True)

        self.player_x = SCREEN_WIDTH // 2 - PLAYER_W // 2
        self.player_y = SCREEN_HEIGHT - PLAYER_H - 5

        self.particles = []
        for _ in range(50):
            self.particles.append([random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(2, 5)])

        self.logs = []
        for _ in range(6):
            self.logs.append({"x": random.randint(0, SCREEN_WIDTH - LOG_W), "y": random.randint(-SCREEN_HEIGHT, 0), "speed": random.randint(1, 3)})
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.player_x = pyxel.mouse_x - PLAYER_W
            self.player_x = max(0, min(self.player_x, SCREEN_WIDTH - PLAYER_W))
        
        for p in self.particles:
            p[1] += p[2]
            if p[1] > SCREEN_HEIGHT:
                p[1] = 0
                p[0] = random.randint(0, SCREEN_WIDTH)

        for log in self.logs:
            log["y"] += log["speed"]
            if log["y"] > SCREEN_HEIGHT:
                log["x"] = random.randint(0, SCREEN_WIDTH - LOG_W)
                log["y"] = random.randint(-LOG_H * 5, -LOG_H)
                log["speed"] = random.randint(1, 3)
        
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
    
    def draw(self):
        pyxel.cls(1)

        for p in self.particles:
            color = 3 if p[2] < 4 else 7
            pyxel.line(p[0], p[1], p[0], p[1] + 2, color)

        pyxel.blt(self.player_x, self.player_y, 0, PLAYER_U, PLAYER_V, PLAYER_W, PLAYER_H, colkey = 0)

        for log in self.logs:
            pyxel.blt(log["x"], log["y"], 0, LOG_U, LOG_V, LOG_W, LOG_H, colkey = 0)
        
App()