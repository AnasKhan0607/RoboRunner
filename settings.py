import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Robot Runner"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = -0.05
PLAYER_GRAVITY = 0.5

PLATFORMS = [(0, HEIGHT-40, 2000, 40), (2300, HEIGHT-40, 2000, 40), (4600, HEIGHT-40, 2000, 40), (6900, HEIGHT-40, 2000, 40), (9000, HEIGHT-40, 2000, 40),
             (WIDTH/3, HEIGHT/1.7, 200, 30), (800, HEIGHT/1.7, 200, 30), (1200, HEIGHT/3.3, 100, 30), (1900, HEIGHT/1.5, 200, 30), (2200, HEIGHT/3.3, 100, 30),
             (2600, HEIGHT/1.5, 200, 30), (3100, HEIGHT/1.7, 200, 30), (3700, HEIGHT/3.3, 100, 30), (4300, HEIGHT/1.5, 200, 30), (4900, HEIGHT/3.3, 100, 30),
             (5300, HEIGHT/1.5, 200, 30), (5700, HEIGHT/1.7, 200, 30), (6000, HEIGHT/3.3, 100, 30), (6500, HEIGHT/1.5, 200, 30), (6900, HEIGHT/3.3, 100, 30),
             (7200, HEIGHT/1.5, 200, 30), (7600, HEIGHT/1.7, 200, 30), (8000, HEIGHT/3.3, 100, 30), (8500, HEIGHT/1.5, 200, 30), (9000, HEIGHT/3.3, 100, 30)]
