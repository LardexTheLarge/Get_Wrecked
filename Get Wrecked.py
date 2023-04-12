import pygame, random

#Initialize pygame
pygame.init()

#Create a display surface
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Get Wrecked")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Game values
BUFFER_DISTANCE = -100

#Define classes
class Game():
    #A class to help control and update gameplay
    def __init__(self, player, comet_group, bomb_group, player_bullet_group):
        #Initialize the game
        self.round_number = 1
        
        self.player = player
        self.comet_group = comet_group
        self.bomb_group = bomb_group
        self.player_bullet_group = player_bullet_group

        #Set sounds and music
        self.comet_hit = pygame.mixer.Sound("comet_hit.wav")
        self.bomb_hit = pygame.mixer.Sound("bomb.wav")
        self.player_hit = pygame.mixer.Sound("player_hit.wav")

        #Set font
        self.font = pygame.font.Font("Blacknorth.otf", 32)

    def update(self):
        #Update the game
        self.check_collisions()
        self.check_round_completion()

    def draw(self):
        #Draw the HUD and other information to display
        
        #Set colors
        WHITE = (255,255,255)

        round_text = self.font.render("Round: " + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (20, 10)

        lives_text = self.font.render("Lives: " + str(self.player.lives), True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (WINDOW_WIDTH - 20, 10)

        #Blit HUD to the display
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text, lives_rect)
        pygame.draw.line(display_surface, WHITE, (0, 65), (WINDOW_WIDTH, 65), 4)
        pygame.draw.line(display_surface, WHITE, (0, WINDOW_HEIGHT - 70), (WINDOW_WIDTH, WINDOW_HEIGHT - 70), 4)
        pygame.draw.rect(display_surface, WHITE, (WINDOW_WIDTH//2 - 100, 6, 200, 52))

    def check_collisions(self):
        #check for collisions
        
        #See if any bullet in the player bullet group hits a comet in comet group
        comet_collide = pygame.sprite.groupcollide(self.player_bullet_group, self.comet_group, True, True)
        if comet_collide:
            self.comet_hit.play()
            for collide in comet_collide:
                comet = Comet(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE, 3)
                my_comet_group.add(comet)


        #See if any bullet in the player bullet group hits a bomb in bomb group
        if pygame.sprite.groupcollide(self.player_bullet_group, self.bomb_group, True, True):
            self.bomb_hit.play()

        if pygame.sprite.spritecollide(self.player, self.comet_group, True):
            self.player_hit.play()
            self.player.lives -= 1

    def check_round_completion(self):
        #Check to see if a player has completed a single round
        pass

    def start_new_round(self):
        #Start a new round
        pass
    
    def check_game_status(self, main_text, sub_text):
        #Check to see the status of the game and how the player died
        pass

    def pause_game(self, main_text, sub_text):
        #pause the game
        pass

    def reset_game(self):
        #Reset the game
        pass

class Player(pygame.sprite.Sprite):
    #A class to model the spaceship the user can control

    def __init__(self, bullet_group):
        #Initialize the player
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom = WINDOW_HEIGHT - 5

        self.lives = 5
        self.velocity = 8

        self.bullet_group = bullet_group

        self.shoot_sound = pygame.mixer.Sound("ship_gun.wav")
        self.shoot_sound.set_volume(.01)

    def update(self):
        #update the player
        keys = pygame.key.get_pressed()

        #Outline the player for the template to fill
        pygame.draw.rect(display_surface, (255,255,255), self.rect, 1)

        #move the player within the bounds of the screen
        if keys[pygame.K_a] and self.rect.left > 10:
            self.rect.x -= self.velocity
        if keys[pygame.K_d] and self.rect.right < WINDOW_WIDTH - 10:
            self.rect.x += self.velocity

    def fire(self):
        #fire a bullet
        
        #Restrict the number of bullets on the screen at a time
        if len(self.bullet_group) < 4:
            self.shoot_sound.play()
            PlayerBullet(self.rect.left, self.rect.top, self.bullet_group)
            PlayerBullet(self.rect.right, self.rect.top, self.bullet_group)

    def reset(self):
        #reset the players position
        self.rect.centerx = WINDOW_WIDTH//2

class Comet(pygame.sprite.Sprite):
    #A class to model a comet that will hit the players rect
    def __init__(self, x, y, velocity):
        #Initialize the comet
        super().__init__()
        self.image = pygame.image.load("comet.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity = velocity

    def update(self):
        #Update the comet
        if self.rect.y > WINDOW_HEIGHT:
            self.rect.x = random.randint(64, WINDOW_WIDTH - 48)
            self.rect.y = 200
        else:
            self.rect.y += self.velocity

class Bomb(pygame.sprite.Sprite):
    #A class to model a bomb colliding with the player and resetting the users progress
    
    #Initialize the player
    def __init__(self, x, y, velocity):
        #Initialize the bomb
        super().__init__()
        self.image = pygame.image.load("bomb.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity = velocity

    def update(self):
        #Update the bomb
        if self.rect.y > WINDOW_HEIGHT:
            self.rect.x = random.randint(64, WINDOW_WIDTH - 48)
            self.rect.y = BUFFER_DISTANCE
        else:
            self.rect.y += self.velocity

class PlayerBullet(pygame.sprite.Sprite):
    #A class to model a bullet fired by the player

    def __init__(self, x, y, bullet_group):
        #Initialize the player's bullet
        super().__init__()
        self.image = pygame.image.load("blue_lazer.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        #update the bullet
        self.rect.y -= self.velocity

        #If the bullet is off the screen, kill it
        if self.rect.bottom < 0:
            self.kill()

#Create bullet group
my_player_bullet_group = pygame.sprite.Group()

#Create player group and player object
my_player_group = pygame.sprite.Group()
my_player = Player(my_player_bullet_group)
my_player_group.add(my_player)

#Create a comet group
my_comet_group = pygame.sprite.Group()
comet = Comet(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE, 3)
my_comet_group.add(comet)

#Create a bomb group
my_bomb_group = pygame.sprite.Group()
bomb = Bomb(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE, 1)
my_bomb_group.add(bomb)

#Create a game object
my_game = Game(my_player, my_comet_group, my_bomb_group, my_player_bullet_group)
my_game.start_new_round()

#The main game loop
running = True
while running:
    #Check to see if the user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #The player wants to fire
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.fire()
    
    #Fill the display
    display_surface.fill((0,0,100))

    #Update the display all sprite groups
    my_player_group.update()
    my_player_group.draw(display_surface)

    my_comet_group.update()
    my_comet_group.draw(display_surface)

    my_bomb_group.update()
    my_bomb_group.draw(display_surface)

    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)

    #Update and draw game object
    my_game.update()
    my_game.draw()

    #Update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

#End the game
pygame.quit()