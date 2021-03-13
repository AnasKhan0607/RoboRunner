import pygame
import random
from sprites import *


class Game:
    """ This class represents the Game. It contains all the game objects. """

    def __init__(self):
        """ Set up the game on creation. """

        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()
        # --- Create the window
        self.screen = pygame.display.set_mode(
            [WIDTH, HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()  # timer
        self.running = True               # boolean to check if game is running
        self.playing = True               # boolean to check if user is playing
        self.all_sprites = None           # all sprites group
        self.platforms = None             # all platform sprites group
        self.bots = None                  # all enemy sprites group
        self.bullets = None               # all bullets sprites group
        self.boss_bullets = None          # all boss bullets sprites group
        self.player = None                # the player of the game
        self.kills = 0                    # amount of kills player has
        self.boss = None                  # boss of the game
        self.win = None                   # to see if player has won by killing boss



    def new(self):
        """
        Creates a new instance of a game. initializes a new game.
        """
        self.kills = 0
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.bots = pygame.sprite.Group()
        self.bots_timer = 0                       # timer for when to spawn bots
        self.bullets = pygame.sprite.Group()
        self.boss_bullets = pygame.sprite.Group()
        self.player = Player(self)
        self.boss= Boss(self, self.player)
        self.all_sprites.add(self.player)
        self.win = False
        for platform in PLATFORMS:                # adds all platforms made into the sprite groups
            plat = Platform(*platform)
            self.all_sprites.add(plat)
            self.platforms.add(plat)
        self.run()                                # calls run function after initializing new game

    def events(self):
        """
        handles all the user events in the game(inputs)
        """
        for event in pygame.event.get():                # loops through all events
            if event.type == pygame.QUIT:               # quit event when close is clicked to leave window
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:            # event for when player wants to jump with spacebar
                if event.key == pygame.K_w:
                    self.player.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:    # event for when player shoots with mouse(creates bullet and adds to sprite group)
                x, y = pygame.mouse.get_pos()
                bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, 20, x, y, self.player)
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)
                self.player.shooting = True



    def update(self):
        """
        update function to update the game every frame.
        """
        self.all_sprites.update()                   # updates all sprites

        real_time = pygame.time.get_ticks()         # gets time at the moment


        if self.kills > 5:                          # checks if kills reach certain point to make game harder by spawning more bots
            if real_time - self.bots_timer > 2000:
                self.bots_timer = real_time
                Groundbot(self, self.player)
                Flyingbot(self, self.player)

                bullet = Bossbullet(self.boss.rect.centerx, self.boss.rect.centery, 10, self.player.rect.centerx, self.player.rect.centery, self.player)
                self.boss_bullets.add(bullet)
                self.all_sprites.add(bullet)

        else:
            if real_time - self.bots_timer > 2000:
                self.bots_timer = real_time
                Flyingbot(self, self.player)


        # Collision detection

        enemy_hits = pygame.sprite.spritecollide(self.player, self.bots, False)    # checks if player hits bot to make player lose
        if enemy_hits:
            self.playing = False

        enemy_hits = pygame.sprite.collide_rect(self.player, self.boss)    # checks if player hits boss to make player lose
        if enemy_hits:
            self.playing = False

        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)    # checks if player is on platform to keep player from falling
        if self.player.velocity.y > 0:
            if hits:
                self.player.position.y = hits[0].rect.top + 1
                self.player.velocity.y = 0

        for enemy in self.bots:                     # checks if enemy is hit by bullet to kill them and make score go up
            if pygame.sprite.spritecollide(enemy, self.bullets, False):
                enemy.kill()
                self.kills+=1

        for bullet in self.boss_bullets:            # checks if enemy bullet hits player to make player loose
            if pygame.sprite.collide_rect(bullet, self.player):
                bullet.kill()
                self.playing = False

        for bullet in self.bullets:                 # checks if bullet hits enemy or goes off screen to kill the bullet
            if pygame.sprite.spritecollide(bullet, self.bots, False):
                bullet.kill()
                self.kills += 1
            if pygame.sprite.collide_rect(bullet, self.boss):
                self.boss.health -= 1
                bullet.kill()
            if bullet.rect.x > WIDTH or bullet.rect.x < 0:
                bullet.kill()
            elif bullet.rect.y > HEIGHT or bullet.rect.y < 0:
                bullet.kill()

        # Screen Scrolling
        if self.player.rect.right >= WIDTH/1.7:
            self.player.position.x -= self.player.velocity.x
            self.boss.rect.centerx -= 7
            for platform in self.platforms:
                platform.rect.x -= 7
            for bot in self.bots:
                bot.rect.x -= 5
        if self.player.rect.right <= WIDTH/2:
            self.player.position.x += abs(self.player.velocity.x)
            self.boss.rect.centerx += 7
            for platform in self.platforms:
                platform.rect.x += 7
            for bot in self.bots:
                bot.rect.x += 5

        if self.boss.health == 0:
            self.win = True
            self.playing = False
        # Game over
        if self.player.rect.bottom > HEIGHT:
            self.playing = False


    def draw(self):
        """
        draws screen and all sprites onto screen and displays it
        """
        self.screen.fill(RED)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.kills), 22, WHITE, WIDTH/2, 20)


        pygame.display.flip()


    def draw_text(self, text, size, color, x, y):
        """
        helper function to draw text to the screen
        """
        font = pygame.font.Font(pygame.font.match_font("arial"), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


    def run(self):
        """
        Run method to run the game loop and call all other methods until games closed
        """
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        return


    def show_start_screen(self):
        """
        starting screen for the game
        """
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("A, D to move, W to jump, Mouse to aim and shoot", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT/1.25)
        pygame.display.flip()

        dont_start = True
        while dont_start:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    dont_start = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    dont_start = False

    def show_go_screen(self, win):
        """
        Game over or won screen for the game when player looses or wins and wants to play again
        """
        if self.running:
            self.screen.fill(BLACK)
            if win == False:
                self.draw_text("Game Over", 48, WHITE, WIDTH/2, HEIGHT/4)
            if win == True:
                self.draw_text("You Win", 48, WHITE, WIDTH/2, HEIGHT/4)
            self.draw_text(f"Score: {self.kills}", 22, WHITE, WIDTH/2, HEIGHT/2)
            self.draw_text("Press a key to play again", 22, WHITE, WIDTH/2, HEIGHT/1.25)
            pygame.display.flip()

            dont_start = True
            while dont_start:
                self.clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        dont_start = False
                        self.running = False
                    if event.type == pygame.KEYUP:
                        dont_start = False

if __name__ == '__main__':
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_go_screen(g.win)

    pygame.quit()
