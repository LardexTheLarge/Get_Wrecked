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
BUFFER_DISTANCE = random.choice([-100, -200, -300])

BD = random.choice([-100, -200, -300])

#Set colors
WHITE = (255,255,255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
cargo_color = random.choice(["white", "yellow", "purple"])

#Define classes
class Game():
    #A class to help control and update gameplay
    def __init__(self, player, comet_group, bomb_group, player_bullet_group, cargo_group, red_cargo_group, blue_cargo_group):
        #Initialize the game
        self.round_number = 1
        self.target_color = 5
        self.total_cargo_red = 0
        self.total_cargo_blue = 0
        
        self.player = player
        self.comet_group = comet_group
        self.bomb_group = bomb_group
        self.player_bullet_group = player_bullet_group
        self.cargo_group = cargo_group
        self.red_cargo_group = red_cargo_group
        self.blue_cargo_group = blue_cargo_group

        #Set sounds and music
        self.comet_hit = pygame.mixer.Sound("comet_hit.wav")
        self.bomb_hit = pygame.mixer.Sound("bomb.wav")
        self.player_hit = pygame.mixer.Sound("player_hit.wav")
        self.cargo_pickup = pygame.mixer.Sound("cargo_pickup.wav")

        self.cargo_pickup.set_volume(.1)
        self.comet_hit.set_volume(.1)
        self.bomb_hit.set_volume(.1)
        self.player_hit.set_volume(.1)

        #Set font
        self.font = pygame.font.Font("Blacknorth.otf", 32)

    def update(self):
        #Update the game
        self.check_collisions()
        self.check_round_completion()

    def draw(self):
        #Draw the HUD and other information to display
        round_text = self.font.render("Round: " + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (20, 10)

        lives_text = self.font.render("Lives: " + str(self.player.lives), True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (WINDOW_WIDTH - 20, 10)

        red_cargo_text = self.font.render(str(self.total_cargo_red) + " x " + str(self.target_color), True, WHITE)
        red_cargo_rect = red_cargo_text.get_rect()
        red_cargo_rect.center = (WINDOW_WIDTH//2 + 40, 35)

        blue_cargo_text = self.font.render(str(self.total_cargo_blue) + " x " + str(self.target_color), True, WHITE)
        blue_cargo_rect = blue_cargo_text.get_rect()
        blue_cargo_rect.center = (WINDOW_WIDTH//2 - 60, 35)

        #Blit HUD to the display
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text, lives_rect)
        pygame.draw.line(display_surface, WHITE, (0, 65), (WINDOW_WIDTH, 65), 4)
        pygame.draw.line(display_surface, WHITE, (0, WINDOW_HEIGHT - 70), (WINDOW_WIDTH, WINDOW_HEIGHT - 70), 4)
        
        pygame.draw.rect(display_surface, BLUE, (WINDOW_WIDTH//2 - 100, 6, 50, 50))
        display_surface.blit(blue_cargo_text, blue_cargo_rect)

        pygame.draw.rect(display_surface, RED, (WINDOW_WIDTH//2, 6, 50, 50))
        display_surface.blit(red_cargo_text, red_cargo_rect)

    def check_collisions(self):
        #check for collisions
        
        #See if any bullet in the player bullet group hits a comet in comet group
        comet_collide = pygame.sprite.groupcollide(self.player_bullet_group, self.comet_group, True, True)
        #See if any bullet in the player bullet group hits a bomb in bomb group
        bomb_collide = pygame.sprite.groupcollide(self.player_bullet_group, self.bomb_group, True, True)
        if bomb_collide or comet_collide:
            self.player_hit.play()
            for collide in bomb_collide:
                bomb = Bomb(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE, 1)
                my_bomb_group.add(bomb)
            
            for collide in comet_collide:
                comet = Comet(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE, 3)
                my_comet_group.add(comet)

        #see if any comet collides with player and respawn comet
        player_comet_collide = pygame.sprite.spritecollide(self.player, self.comet_group, True)
        if player_comet_collide:
            self.comet_hit.play()
            self.player.lives -= 1
            self.total_cargo_blue -= 1
            self.total_cargo_red -= 1
            self.player.velocity += 1

            for collide in player_comet_collide:
                comet = Comet(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE, 3)
                my_comet_group.add(comet)

            self.check_game_status("You've been hit, lost 2 cargo", "Press 'ENTER' to continue")

        #see if any bomb collides with player and respawn bomb
        player_bomb_collide = pygame.sprite.spritecollide(self.player, self.bomb_group, True)
        if player_bomb_collide:
            self.bomb_hit.play()
            #add complete reset when bomb collides with player
            self.total_cargo_blue = 0
            self.total_cargo_red = 0

            self.player.velocity = 8

            for collide in player_bomb_collide:
                bomb = Bomb(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE, 1)
                my_bomb_group.add(bomb)

            self.check_game_status("You've been hit, lost all cargo", "Press 'ENTER' to continue")

        #See if different colored cargo collides with the players rect and holds the cargo
        player_cargo_collide = pygame.sprite.spritecollide(self.player, self.cargo_group, True)
        if player_cargo_collide:
            self.cargo_pickup.play()
            self.player.velocity -= .5

            for collide in player_cargo_collide:
                cargo = Cargo(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE, cargo_color)
                my_cargo_group.add(cargo)

        #see if red cargo collides with the player rect and adds to the red cargo counter
        player_red_cargo_collide = pygame.sprite.spritecollide(self.player, self.red_cargo_group, True)
        if player_red_cargo_collide:
            self.cargo_pickup.play()
            self.total_cargo_red += 1
            self.player.velocity -= .5

            for collide in player_red_cargo_collide:
                red_cargo = RedCargo(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE)
                my_red_cargo_group.add(red_cargo)

        #see if blue cargo collides with the player rect and adds to the blue cargo counter
        player_blue_cargo_collide = pygame.sprite.spritecollide(self.player, self.blue_cargo_group, True)
        if player_blue_cargo_collide:
            self.cargo_pickup.play()
            self.total_cargo_blue += 1
            self.player.velocity -= .5

            for collide in player_blue_cargo_collide:
                blue_cargo = BlueCargo(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE)
                my_blue_cargo_group.add(blue_cargo)

    def check_round_completion(self):
        #Check to see if a player has completed a single round
        if (self.total_cargo_red == 5 and self.total_cargo_blue == 5):
            self.round_number += 1

            self.start_new_round()

    def start_new_round(self):
        #Start a new round

        #Create all comet, bomb, and cargo
        comet = Comet(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE, 3)
        self.comet_group.add(comet)

        bomb = Bomb(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE, 1)
        self.bomb_group.add(bomb)

        cargo = Cargo(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE, cargo_color)
        self.cargo_group.add(cargo)

        red_cargo = RedCargo(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE)
        self.red_cargo_group.add(red_cargo)

        blue_cargo = BlueCargo(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE)
        self.blue_cargo_group.add(blue_cargo)

        #Pause the game and prompt the user to start
        self.pause_game("Get Wrecked Round " + str(self.round_number), "Press 'ENTER' to begin")
    
    def check_game_status(self, main_text, sub_text):
        #Check to see the status of the game and how the player died
        self.player_bullet_group.empty()
        self.player.reset()

        #Check if the game is over or a simple round reset
        if self.player.lives == 0:
            self.reset_game()
        else:
            self.pause_game(main_text, sub_text)

    def pause_game(self, main_text, sub_text):
        #pause the game
        global running

        #Create main pause text
        main_text = self.font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        #Create sub pause text
        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

        #Blit the pause text
        display_surface.fill ((0,0,100))
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                #The user wants to play again
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                #The user wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    def reset_game(self):
        #Reset the game
        self.pause_game("Final Results: " + str(self.round_number), "Press 'ENTER' to play again")

        #Reset game values
        self.round_number = 1
        self.total_cargo_blue = 0
        self.total_cargo_red = 0

        self.player.lives = 5
        self.player.velocity = 8

        #Empty groups
        self.bomb_group.empty()
        self.comet_group.empty()
        self.cargo_group.empty()
        self.red_cargo_group.empty()
        self.blue_cargo_group.empty()
        self.player_bullet_group.empty()

        #Start a new game
        self.start_new_round()

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
            self.rect.y = BUFFER_DISTANCE
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

class RedCargo(pygame.sprite.Sprite):
    #A class to model a color for the ship to catch in insert into the players rect

    def __init__(self, x, y):
    #     Initialize the Square
        super().__init__()
        self.BUFFER_DISTANCE = random.choice([-100, -200, -300])
        self.image = pygame.image.load("red_sqr.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity = 5
        
    def update(self):
        #Update the cargo
        if self.rect.y > WINDOW_HEIGHT:
            self.kill()
            red_cargo = RedCargo(random.randint(64, WINDOW_WIDTH - 48), self.BUFFER_DISTANCE)
            my_red_cargo_group.add(red_cargo)
        else:
            self.rect.y += self.velocity

class BlueCargo(pygame.sprite.Sprite):
    #A class to model a color for the ship to catch in insert into the players rect

    def __init__(self, x, y):
    #     Initialize the Square
        super().__init__()
        self.BUFFER_DISTANCE = random.choice([-100, -200, -300])
        self.image = pygame.image.load("blue_sqr.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity = 5
        
    def update(self):
        #Update the cargo
        if self.rect.y > WINDOW_HEIGHT:
            self.kill()
            blue_cargo = BlueCargo(random.randint(64, WINDOW_WIDTH - 48), self.BUFFER_DISTANCE)
            my_blue_cargo_group.add(blue_cargo)
        else:
            self.rect.y += self.velocity

class Cargo(pygame.sprite.Sprite):
    #A class to model a color for the ship to catch in insert into the players rect

    def __init__(self, x, y, color):
    #     Initialize the Square
        super().__init__()
        self.BUFFER_DISTANCE = random.choice([-100, -200, -300])
        self.cargo_color = random.choice(["white", "yellow", "purple"])
        self.image = pygame.image.load(str(self.cargo_color) + "_sqr.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity = 5
        
    def update(self):
        #Update the cargo
        if self.rect.y > WINDOW_HEIGHT:
            self.kill()
            cargo = Cargo(random.randint(64, WINDOW_WIDTH - 48), self.BUFFER_DISTANCE, self.cargo_color)
            my_cargo_group.add(cargo)
        else:
            self.rect.y += self.velocity


#Create bullet group
my_player_bullet_group = pygame.sprite.Group()

#Create player group and player object
my_player_group = pygame.sprite.Group()
my_player = Player(my_player_bullet_group)
my_player_group.add(my_player)

#Create players cargo
my_cargo_group = pygame.sprite.Group()
my_cargo = Cargo(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE, cargo_color)
my_cargo_group.add(my_cargo)

my_red_cargo_group = pygame.sprite.Group()
my_red_cargo = RedCargo(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE)
my_red_cargo_group.add(my_red_cargo)

my_blue_cargo_group = pygame.sprite.Group()
my_blue_cargo = BlueCargo(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE)
my_blue_cargo_group.add(my_blue_cargo)

#Create a comet group
my_comet_group = pygame.sprite.Group()
comet = Comet(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE, 3)
my_comet_group.add(comet)

#Create a bomb group
my_bomb_group = pygame.sprite.Group()
bomb = Bomb(random.randint(64, WINDOW_WIDTH - 48), BUFFER_DISTANCE, 1)
my_bomb_group.add(bomb)

#Create a game object
my_game = Game(my_player, my_comet_group, my_bomb_group, my_player_bullet_group, my_cargo_group, my_red_cargo_group, my_blue_cargo_group)

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

    my_cargo_group.update()
    my_cargo_group.draw(display_surface)

    my_red_cargo_group.update()
    my_red_cargo_group.draw(display_surface)

    my_blue_cargo_group.update()
    my_blue_cargo_group.draw(display_surface)

    my_bomb_group.update()
    my_bomb_group.draw(display_surface)

    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)

    my_comet_group.update()
    my_comet_group.draw(display_surface)

    #Update and draw game object
    my_game.update()
    my_game.draw()

    #Update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

#End the game
pygame.quit()