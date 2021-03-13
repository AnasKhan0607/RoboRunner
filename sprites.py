import pygame, csv, os, random
from settings import *
from math import *
vector = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    """
    Player class for the player of the game using a player sprite
    """
    def __init__(self, game):
        """
        initializes the player
        """
        pygame.sprite.Sprite.__init__(self)         # initializes sprite
        self.game = game
        self.walking = False                        # checks if player is walking
        self.jumping = False                        # checks if player is jumping
        self.shooting = False                       # checks if player is shooting
        self.curr_frame = 0                         # current fram of player when it has multiple frames
        self.last_update = 0                        # last frame of player when it has multiple frames
        self.load_images()                          # calls load images method to load the image of player
        self.image = self.idle_frames[0]            # initial image of player when game starts
        self.image.set_colorkey(BLACK)              # gets rid of black rectangle of image
        self.rect = self.image.get_rect()           # gets rectangle of image
        self.rect.center = (WIDTH/2, HEIGHT/2)      # initializes location of player
        self.position = vector(WIDTH/2, HEIGHT/2)   # initializes position of player
        self.velocity = vector(0, 0)                # initializes velocity of player
        self.acceleration = vector(0, 0)            # initializes acceleration of player

    def update(self, *args, **kwargs) -> None:
        """
        overides update in game inorder to check and update player movements
        """
        # changes acceleration of player from the direction it is going (creates friction and gravity)
        self.acceleration = vector(0, PLAYER_GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acceleration.x = -PLAYER_ACCELERATION
        if keys[pygame.K_d]:
            self.acceleration.x = PLAYER_ACCELERATION


        self.acceleration.x += self.velocity.x*PLAYER_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5*self.acceleration

        self.rect.midbottom = self.position
        self.animation()                                         # calls animation to get the image at the certain movement

    def jump(self):
        """
        jump method to make player jump if it is on ground
        """
        self.jumping = True
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.velocity.y = -15

    def load_images(self):
        """
        Loads all images of player
        """
        self.idle_frames = [pygame.image.load(os.path.join(img_folder, "Idle (1).png")).convert(),
                            pygame.image.load(os.path.join(img_folder, "Idle (9).png")).convert()]
        self.walk_frames_right = [pygame.image.load(os.path.join(img_folder, "Run (4).png")).convert(),
                                  pygame.image.load(os.path.join(img_folder, "Run (8).png")).convert()]
        self.walk_frames_left = []
        for f in self.walk_frames_right:
            self.walk_frames_left.append(pygame.transform.flip(f, True, False))
        self.jump_frame = [pygame.image.load(os.path.join(img_folder, "Jump (7).png")).convert(),
                           pygame.transform.flip(pygame.image.load(os.path.join(img_folder, "Jump (7).png")).convert(), True, False)]

        self.shooting_frame = [pygame.image.load(os.path.join(img_folder, "Shoot (4).png")).convert(),
                               pygame.image.load(os.path.join(img_folder, "RunShoot (4).png")).convert(),
                               pygame.transform.flip(pygame.image.load(os.path.join(img_folder, "RunShoot (4).png")).convert(), True, False),
                               pygame.image.load(os.path.join(img_folder, "JumpShoot (5).png")).convert(),
                               pygame.transform.flip(pygame.image.load(os.path.join(img_folder, "JumpShoot (5).png")).convert(), True, False)]

    def animation(self):
        """
        checks which image to load depending on players movement
        """
        real_time = pygame.time.get_ticks()

        if self.velocity.x >= 0.15 or self.velocity.x <= -0.15:
            self.walking = True
        else:
            self.walking = False


        if not self.walking and not self.jumping :      # when players idle loads idle image and shooting images when shooting
            if real_time - self.last_update > 200:
                self.last_update = real_time
                self.curr_frame = (self.curr_frame+1)% len(self.idle_frames)
                self.image = self.idle_frames[self.curr_frame]
                if self.shooting:
                    self.image = self.shooting_frame[0]
                    self.shooting = False
                self.image.set_colorkey(BLACK)

        if self.walking:                                # when players walking loads walking images and shooting images when shooting
            if real_time - self.last_update > 200:
                self.last_update = real_time
                self.curr_frame = (self.curr_frame+1)% len(self.walk_frames_right)
                if self.velocity.x > 0:
                    self.image = self.walk_frames_right[self.curr_frame]
                    if self.shooting:
                        self.image = self.shooting_frame[1]
                        self.shooting = False
                if self.velocity.x < 0:
                    self.image = self.walk_frames_left[self.curr_frame]
                    if self.shooting:
                        self.image = self.shooting_frame[2]
                        self.shooting = False
                self.image.set_colorkey(BLACK)

        if self.jumping:                            # when players jumping loads jumping image and shooting images when shooting
            if self.velocity.x > 0:
                self.image = self.jump_frame[0]
                if self.shooting:
                    self.image = self.shooting_frame[3]
            if self.velocity.x < 0:
                self.image = self.jump_frame[1]
                if self.shooting:
                    self.image = self.shooting_frame[4]
            self.image.set_colorkey(BLACK)
            if pygame.sprite.spritecollide(self, self.game.platforms, False):
                self.jumping = False


class Platform(pygame.sprite.Sprite):
    """
    class to creat platforms for the map
    """
    def __init__(self, x, y, width, height):
        """
        initializes platform
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Flyingbot(pygame.sprite.Sprite):
    """
    class for flying bots in the game (enemies)
    """
    def __init__(self, game, player: Player):
        """
        initializes the flying bot
        """
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.game = game
        game.all_sprites.add(self)
        game.bots.add(self)
        self.image = pygame.image.load(os.path.join(img_folder, "ballpurple1.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(HEIGHT/2)
        self.rect.centerx = player.rect.x + 500
        self.vx = -3
        self.vy = 0


    def update(self, *args, **kwargs) -> None:
        """
        method overrides update in game to update the bot acording to what happens
        """
        if self.game.kills > 15:            # checks how many kills player has to make bots faster
            self.vx = -5
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.x < 0:                 # kills bot once its off screen
            self.kill()
        elif self.rect.y > HEIGHT or self.rect.y < 0:
            self.kill()


class Groundbot(pygame.sprite.Sprite):
    """
    class for ground bots in the game (enemies)
    """
    def __init__(self, game, player: Player):
        """
        initializes the ground bot
        """
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.game = game
        game.all_sprites.add(self)
        game.bots.add(self)
        self.image = pygame.image.load(os.path.join(img_folder, "groundbot1.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - 110
        self.rect.centerx = player.rect.x + 500
        self.vx = -2.5
        self.vy = 0


    def update(self, *args, **kwargs) -> None:
        """
        method overrides update in game to update the bot acording to what happens
        """
        if self.game.kills > 15:            # checks how many kills player has to make bots faster
            self.vx = -4
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.x < 0:                 # kills bot once its off screen
            self.kill()
        elif self.rect.y > HEIGHT or self.rect.y < 0:
            self.kill()

class Boss(pygame.sprite.Sprite):
    """
    class for boss in the game (enemy)
    """
    def __init__(self, game, player: Player):
        """
        initializes the boss of the game
        """
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.game = game
        game.all_sprites.add(self)
        self.health = 30
        self.image = pygame.transform.flip(pygame.image.load(os.path.join(img_folder, "boss.png")).convert(), True, False)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT/5
        self.rect.centerx = 10000


    def update(self, *args, **kwargs) -> None:
        """
        method overrides update in game to update the boss acording to what happens
        """
        if self.health <= 0:                # kills boss once health is 0
            self.kill()


class Bullet(pygame.sprite.Sprite):
    """
    class for players bullets in the game
    """
    def __init__(self, x, y, speed, target_x, target_y, player: Player):
        """
        initializes the bullets of the game
        """
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = pygame.image.load(os.path.join(img_folder, "Bullet_002.png")).convert()
        if target_x < player.rect.x:
            self.image = pygame.transform.flip(pygame.image.load(os.path.join(img_folder, "Bullet_002.png")).convert(), True, False)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        angle = atan2(target_y-self.rect.y, target_x-self.rect.x)           # calculates angle bullet should be shot at
        self.dx = cos(angle)*self.speed
        self.dy = sin(angle)*self.speed
    def update(self):
        """
        method overrides update in game to update the bullet acording to what happens
        """
        self.rect.x += int(self.dx)             # shoots bullet at direction
        self.rect.y += int(self.dy)


class Bossbullet(pygame.sprite.Sprite):
    """
    class for boss's bullets in the game
    """
    def __init__(self, x, y, speed, target_x, target_y, player: Player):
        """
        initializes the boss's bullets in the game
        """
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = pygame.image.load(os.path.join(img_folder, "bossbullet.png"))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        angle = atan2(target_y-self.rect.y, target_x-self.rect.x)       # calculates angle bullet should be shot at
        self.dx = cos(angle)*self.speed
        self.dy = sin(angle)*self.speed
    def update(self):
        """
        method overrides update in game to update the boss's bullets acording to what happens
        """
        self.rect.x += int(self.dx)             # shoots bullet at direction
        self.rect.y += int(self.dy)

