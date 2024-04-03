import pygame, sys
from pygame.locals import *

# Basic setup
pygame.init()
clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Love Ballad")

# Upload images
title_screen_image = pygame.image.load("images/background/title.png").convert_alpha()
main_screen_image = pygame.image.load("images/background/main_screen.png").convert_alpha()
ending = pygame.image.load("images/background/ending.png").convert_alpha()

start_img = pygame.image.load('images/button/start_btn.png').convert_alpha()
exit_img = pygame.image.load('images/button/exit_btn.png').convert_alpha()
restart_img = pygame.image.load("images/button/restart_btn.png").convert_alpha()

title_txt = pygame.image.load("images/text/title.png").convert_alpha()
instruction_txt = pygame.image.load("images/text/instruction.png").convert_alpha()
fail_txt = pygame.image.load("images/text/shots_failed.png").convert_alpha()
level_txt = pygame.image.load("images/text/level.png").convert_alpha()
thank_txt = pygame.image.load("images/text/thank.png").convert_alpha()
result_txt = pygame.image.load("images/text/result.png").convert_alpha()
stupid_txt = pygame.image.load("images/text/stupid.png").convert_alpha()
live_txt = pygame.image.load("images/text/live.png").convert_alpha()
deed_txt = pygame.image.load("images/text/deed.png").convert_alpha()

# Music/ Sound
bg_music = pygame.mixer.Sound("sound/love_ballad.mp3")
bg_music.set_volume(0.5)
bg_music.play(-1)

arrow_sound = pygame.mixer.Sound("sound/arrow_shot.mp3")
arrow_sound.set_volume(1000000)

button_sound = pygame.mixer.Sound("sound/button.mp3")
button_sound.set_volume(0.3)

checkpoint_sound = pygame.mixer.Sound("sound/checkpoint.mp3")
checkpoint_sound.set_volume(0.9)

fireball_sound = pygame.mixer.Sound("sound/fireball.mp3")
fireball_sound.set_volume(1.5)

game_over_sound = pygame.mixer.Sound("sound/game_over.mp3")
game_over_sound.set_volume(1000000)

heart_popped_sound = pygame.mixer.Sound("sound/heart_popped.mp3")

reload_sound = pygame.mixer.Sound("sound/reload.mp3")
reload_sound.set_volume(0.7)

ring_shine_sound = pygame.mixer.Sound("sound/ring_shine.mp3")
ring_shine_sound.set_volume(0.6)

satan_popped_sound = pygame.mixer.Sound("sound/satan_popped.mp3")
satan_popped_sound.set_volume(1.3)

# Game Variables
current_level = 1
MAX_LEVEL = 10
game_over = 0
fail = 0

# Draw text
font = pygame.font.SysFont('Futura', 55)
score_font = pygame.font.SysFont('Futura', 100)
def draw_text(text, font, color, x, y):
	img = font.render(text, True, color)
	screen.blit(img, (x, y)) 
# Bow
class Player(pygame.sprite.Sprite): 
    def __init__(self, x, y, scale):
        super().__init__()
        self.image = pygame.image.load("images/object/bow.png").convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(scale * width), int(scale * height)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)

    def movement(self):
        dx = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx -= 7
        if key[pygame.K_RIGHT]:
            dx += 7
        if self.rect.left + dx <= 0 or self.rect.right + dx >= SCREEN_WIDTH:
            dx = 0

        self.rect.x += dx

    def update(self):
        self.draw()
        self.movement()

# Bullet/ Arrow
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, direction):
        super().__init__()
        self.image = pygame.image.load("images/object/arrow.png").convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(scale * width), int(scale * height)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.trigger = False
        self.play_sound = False

    def draw(self):
        screen.blit(self.image, self.rect)
        
    def movement(self):
        dx = 0
        dy = 0
        key = pygame.key.get_pressed()
        if not self.trigger:
            if key[pygame.K_LEFT]:
                dx = -7
            if key[pygame.K_RIGHT]:
                dx += 7
            if self.rect.left + dx <= 35 or self.rect.right + dx >= SCREEN_WIDTH - 35:
                dx = 0
                    
            # Arrows shot
            if key[pygame.K_SPACE]:
                self.trigger = True
                self.play_sound = True
                
                if self.play_sound:
                        arrow_sound.play()
        
        else:
            dy -= 6 * self.direction
                
        self.rect.x += dx
        self.rect.y += dy

    def check_collision(self):
        for heart in heart_group:
            if pygame.sprite.spritecollide(heart, arrow_single, False) and heart.alive:
                heart.kill()
                heart_popped_sound.play()

        for angel_ring in angel_ring_group:
            if pygame.sprite.spritecollide(angel_ring, arrow_single, False):
                angel_ring.kill()
                self.direction = -1
                ring_shine_sound.play()
            
    def update(self):
        self.draw()
        self.check_collision()
        self.movement()

# Static/ Horizontal Movement
class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_direction, duration):
        super().__init__()
        self.image = pygame.image.load("images/object/heart.png").convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(0.15 * width), int(0.15 * height)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.move_counter = 0
        self.move_direction = move_direction
        self.move_x = move_x
        self.duration = duration

    def draw(self):
        screen.blit(self.image, self.rect)

    def movement(self):
        self.rect.x += self.move_direction * self.move_x
        self.move_counter += 1
        if self.move_counter > self.duration:
            self.move_direction *= -1
            self.move_counter *= -1

    def update(self):
        self.draw()
        self.movement()

# Static/ Horizontal Movement
class Cupido(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_direction, duration):
        super().__init__()
        self.image = pygame.image.load("images/object/cupido.png").convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(0.1 * width), int(0.1 * height)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.move_counter = 0
        self.move_direction = move_direction
        self.move_x = move_x
        self.duration = duration
        self.flip = False

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def movement(self):
        self.rect.x += self.move_direction * self.move_x
        self.move_counter += 1
        if self.move_counter > self.duration:
            self.move_direction *= -1
            self.move_counter *= -1
        if self.move_direction == 1:
            self.flip = False
        if self.move_direction == -1:
            self.flip = True

    def update(self):
        self.draw()
        self.movement()

class Angel_ring(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/object/angel_ring.png").convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(0.18 * width), int(0.18 * height)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        screen.blit(self.image, self.rect)

# Diagonal Movement        
class Rose(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y, move_direction, duration):
        super().__init__()
        self.image = pygame.image.load("images/object/black_rose.png").convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(0.125 * width), int(0.125 * height)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.move_counter = 0
        self.move_direction = move_direction
        self.move_x = move_x
        self.move_y = move_y
        self.duration = duration

    def draw(self):
        screen.blit(self.image, self.rect)

    def movement(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if self.move_counter > self.duration:
            self.move_direction *= -1
            self.move_counter *= -1

    def update(self):
        self.draw()
        self.movement()

# PK that throws fireball
class Satan(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_direction, duration):
        super().__init__()
        self.image = pygame.image.load("images/object/satan.png").convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(0.25 * width), int(0.25 * height)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.move_counter = 0
        self.move_direction = move_direction
        self.move_x = move_x
        self.duration = duration
        self.flip = False
        self.attack = False
        self.trigger_cooldown = 0

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def movement(self):
        self.rect.x += self.move_direction * self.move_x
        self.move_counter += 1
        if self.move_counter > self.duration:
            self.move_direction *= -1
            self.move_counter *= -1
        if self.move_direction == 1:
            self.flip = False
        if self.move_direction == -1:
            self.flip = True

    def detection(self):
        if abs(self.rect.centerx - arrow.rect.centerx) < 100:
            self.attack = True
        else:
            self.attack = False

    def shooting(self):
        if self.attack:
            if self.trigger_cooldown == 0:
                self.trigger_cooldown = 100
                fireball = Fireball(self.rect.centerx, self.rect.centery + 20)
                fireball_group.add(fireball)
                fireball_sound.play()
            elif self.trigger_cooldown > 0:
                self.trigger_cooldown -= 1

    def update(self):
        self.draw()
        self.movement()
        self.detection()
        self.shooting()

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/object/fireball.png").convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(0.05 * width), int(0.05 * height)))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)

    def movement(self):
        self.rect.y += 6
        if self.rect.top > SCREEN_HEIGHT + 60:
            self.kill()

    def update(self):
        self.draw()
        self.movement()        
        
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and click condition
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False                
            
        # Draw button
        screen.blit(self.image, self.rect)
        
        return action

# Create sprite groups
heart_group = pygame.sprite.Group()
cupido_group = pygame.sprite.Group()
angel_ring_group = pygame.sprite.Group()
rose_group = pygame.sprite.Group()
satan_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
arrow_single = pygame.sprite.GroupSingle()
player_single = pygame.sprite.GroupSingle()

# Instances
player = Player(SCREEN_WIDTH // 2, 550, 0.075)
arrow = Arrow(SCREEN_WIDTH // 2, 550, 0.075, 1)

player_single.add(player)
arrow_single.add(arrow)

# Create buttons
start_button = Button(SCREEN_WIDTH // 2 - 102, SCREEN_HEIGHT // 2 - 100, start_img, 0.75)
exit_button = Button(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 50, exit_img, 0.75)
restart_button = Button(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2, restart_img, 2)

# Loading levels
def load_level(level):
    if level == 1:
        heart1 = Heart(SCREEN_WIDTH // 2, 50, 0, 1, 0)
        heart2 = Heart(SCREEN_WIDTH // 2, 250, 0, 1, 0)
        heart_group.add(heart1, heart2)

    if level == 2:
        heart1 = Heart(400, 90, 2, 1, 160)
        heart2 = Heart(100, 350, 0, 1, 0)
        heart_group.add(heart1, heart2)

    if level == 3:
        angel_ring1 = Angel_ring(50, 70)
        heart1 = Heart(50, 180, 0, 0, 0)
        heart2 = Heart(500, 75, 3, -1, 80)
        heart3 = Heart(450, 320, 2, 1, 120)
        heart_group.add(heart1, heart2, heart3)
        angel_ring_group.add(angel_ring1)
        
    if level == 4:
        angel_ring1 = Angel_ring(SCREEN_WIDTH // 2, 50)
        angel_ring2 = Angel_ring(750, 150)
        heart1 = Heart(100, 100, 0, 1, 0)
        heart2 = Heart(300, 250, 3, 1, 80)
        heart3 = Heart(500, 400, 2, -1, 120)
        heart4 = Heart(750, 225, 0, 0, 0)
        heart_group.add(heart1, heart2, heart3, heart4)
        angel_ring_group.add(angel_ring1, angel_ring2)
            
    if level == 5:
        cupido1 = Cupido(250, 300, 2, -1, 80)
        angel_ring1 = Angel_ring(675, 200)
        heart1 = Heart(250, 100, 2, -1, 80)
        heart2 = Heart(SCREEN_WIDTH // 2, 400, 3, -1, 120)
        heart_group.add(heart1, heart2)
        angel_ring_group.add(angel_ring1)
        cupido_group.add(cupido1)
        
    if level == 6:
        angel_ring1 = Angel_ring(160, 220)
        angel_ring2 = Angel_ring(320, 220)
        angel_ring3 = Angel_ring(480, 220)
        angel_ring4 = Angel_ring(640, 220)
        heart1 = Heart(160, 300, 0, 0, 0)
        heart2 = Heart(320, 300, 0, 0, 0)
        heart3 = Heart(480, 300, 0, 0, 0)
        heart4 = Heart(640, 300, 0, 0, 0)
        heart5 = Heart(SCREEN_WIDTH // 2, 35, 0, 0, 0)
        cupido1 = Cupido(200, 410, 1, -1, 160)
        cupido2 = Cupido(400, 410, 1, -1, 160)
        cupido3 = Cupido(600, 410, 1, -1, 160)
        cupido4 = Cupido(SCREEN_WIDTH // 2, 155, 2, 1, 140)
        heart_group.add(heart1, heart2, heart3, heart4, heart5)
        angel_ring_group.add(angel_ring1, angel_ring2, angel_ring3, angel_ring4)
        cupido_group.add(cupido1, cupido2, cupido3, cupido4)
        
    if level == 7:
        cupido1 = Cupido(200, 400, 2, 1, 80)
        cupido2 = Cupido(600, 400, 2, 1, 80)
        rose1 = Rose(400, 300, 3, 2, 1, 120)
        rose2 = Rose(400, 300, -3, 2, 1, 120)
        angel_ring1 = Angel_ring(730, 150)
        angel_ring2 = Angel_ring(70, 150)
        heart1 = Heart(730, 200, 0, 0, 0)
        heart2 = Heart(SCREEN_WIDTH // 2, 70, 0, 0, 0)
        heart3 = Heart(70, 200, 0, 0, 0)
        heart_group.add(heart1, heart2, heart3)
        angel_ring_group.add(angel_ring1, angel_ring2)
        rose_group.add(rose1, rose2)
        cupido_group.add(cupido1, cupido2)

    if level == 8:
        cupido1 = Cupido(600, 200, 2, 1, 80)
        rose1 = Rose(210, 180, -1, 2, 1, 80)
        rose2 = Rose(370, 300, -1, 2, 1, 80)
        angel_ring1 = Angel_ring(290, 100)
        angel_ring2 = Angel_ring(450, 100)
        angel_ring3 = Angel_ring(610, 100)
        heart1 = Heart(130, 90, 1, 1, 80)
        heart2 = Heart(290, 210, 1, 1, 80)
        heart3 = Heart(450, 330, 1, 1, 80)
        heart4 = Heart(610, 450, 1, 1, 80)
        heart_group.add(heart1, heart2, heart3, heart4)
        angel_ring_group.add(angel_ring1, angel_ring2, angel_ring3)
        rose_group.add(rose1, rose2)
        cupido_group.add(cupido1)

    if level == 9:
        satan1 = Satan(200, 210, 1, 1, 80)
        cupido1 = Cupido(600, 220, 2, -1, 80)
        rose1 = Rose(100, 400, 1, 1, 1, 80)
        rose2 = Rose(600, 300, 2, 2, 1, 80)
        angel_ring1 = Angel_ring(200, 325)
        angel_ring2 = Angel_ring(600, 50)
        heart1 = Heart(200, 100, 0, 0, 0)
        heart2 = Heart(200, 375, 0, 0, 0)
        heart3 = Heart(600, 100, 0, 0, 0)
        satan_group.add(satan1)
        angel_ring_group.add(angel_ring1, angel_ring2)
        heart_group.add(heart1, heart2, heart3)
        cupido_group.add(cupido1)
        rose_group.add(rose1, rose2)
    
    if level == 10:
        satan1 = Satan(600, 90, 0, 0, 0)
        satan2 = Satan(200, 90, 0, 0, 0)
        angel_ring1 = Angel_ring(100, 150)
        angel_ring2 = Angel_ring(700, 150)
        cupido1 = Cupido(400, 300, 2, 1, 160)
        rose1 = Rose(125, 375, -1, 1, 1, 80)
        rose2 = Rose(675, 375, 1, 1, 1, 80)
        heart1 = Heart(100, 200, 0, 0, 0)
        heart2 = Heart(700, 200, 0, 0, 0)
        heart3 = Heart(400, 50, 2, -1, 40)
        heart4 = Heart(400, 450, 3, 1, 80)
        heart5 = Heart(400, 200, 0, 0, 0)
        satan_group.add(satan1, satan2)
        angel_ring_group.add(angel_ring1, angel_ring2)
        rose_group.add(rose1, rose2)
        cupido_group.add(cupido1)
        heart_group.add(heart1, heart2, heart3, heart4, heart5)
    
# Loading level
load_level(current_level)
        
def reset(level):
    heart_group.empty()
    cupido_group.empty()
    angel_ring_group.empty()
    rose_group.empty()
    satan_group.empty()
    fireball_group.empty()
    arrow_single.empty()
    player_single.empty()
    
    player = Player(SCREEN_WIDTH // 2, 550, 0.075)
    arrow = Arrow(SCREEN_WIDTH // 2, 550, 0.075, 1)        
    player_single.add(player)
    arrow_single.add(arrow)
    load_level(level)
    
# Main Game Loop
run = True
game_start = False
while run:
    clock.tick(FPS)
    if not game_start:
        screen.blit(title_screen_image, (0, 0))
        screen.blit(title_txt, (120, 70))
        screen.blit(instruction_txt, (10, 450))
        screen.blit(stupid_txt, (10, 10))
        if start_button.draw():
                game_start = True
                button_sound.play()
            
        if exit_button.draw():
            pygame.quit()
            sys.exit()        
    else:
        screen.blit(main_screen_image, (0, 0))
        screen.blit(live_txt, (515, 540))
        player_single.update()
        heart_group.update()
        angel_ring_group.update()
        rose_group.update()
        satan_group.update()
        cupido_group.update()
        fireball_group.update()

        
        screen.blit(fail_txt, (0, 0))
        screen.blit(level_txt, (645, 0))
        draw_text(str(current_level), font,(27, 18, 18), 750, 5)
        draw_text(str(fail), font, (27, 18, 28), 215, 10)
        
        # Shoot all hearts to proceed to next level
        for arrow in arrow_single:
            arrow.update()
            if game_over == 0 and arrow.trigger:
                if len(heart_group) == 0:
                    game_over = 1
                    checkpoint_sound.play()

                elif len(heart_group) > 0 and arrow.rect.y < -100:
                    game_over = -1
                    fail += 1

                elif arrow.rect.top > SCREEN_HEIGHT + 20:
                    game_over = -1
                    fail += 1
                    
            if arrow.direction == -1:
                for player in player_single:
                    if pygame.sprite.spritecollide(arrow, player_single, False):
                        arrow.trigger = False
                        arrow.direction = 1
                        arrow.rect.center = player.rect.center
                        reload_sound.play()
                        
            if pygame.sprite.spritecollide(arrow, fireball_group, False):
                game_over = -1
                fail += 1
                            
        # Cupido collision                
        for cupido in cupido_group:
            if pygame.sprite.spritecollide(cupido, arrow_single, False):
                cupido.kill()
                game_over = -1
                fail += 1
                
        # Rose collision                
        for rose in rose_group:
            if pygame.sprite.spritecollide(rose, arrow_single, False):
                rose.kill()
                game_over = -1
                fail += 1

        for satan in satan_group:
            if pygame.sprite.spritecollide(satan, arrow_single, False):
                satan.kill()
                satan_popped_sound.play()

        for player in player_single:
            if pygame.sprite.spritecollide(player, fireball_group, False):
                game_over = -1
                fail += 1
                
        if game_over == 1:
                # Win Screen
                if current_level == MAX_LEVEL:
                        screen.blit(ending, (0, 0))
                        screen.blit(thank_txt, (98, 10))
                        screen.blit(result_txt, (10, 450))
                        screen.blit(deed_txt, (130, 550))
                        draw_text(str(fail), score_font, (27, 18, 28), 485, 465)
                        # Restart
                        if restart_button.draw():
                                button_sound.play()
                                current_level = 1
                                reset(current_level)
                                game_over = 0
                                fail = 0
                                    
                else:
                    current_level += 1
                    reset(current_level)
                    game_over = 0

        if game_over == -1:
            reset(current_level)
            arrow.trigger = False
            game_over = 0
            game_over_sound.play()
                    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.flip()
