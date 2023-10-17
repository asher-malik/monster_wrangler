import pygame
import random

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PURPLE = (127, 0, 255)
YELLOW = (255, 128, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

#0 is purple, 1 is yellow, 2 is blue, 3 is green
COLORS = [PURPLE, YELLOW, BLUE, GREEN]


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Monster Wrangler")
clock = pygame.time.Clock()


class Game:
    def __init__(self, player, monster_group):
        self.player = player
        self.monster_group = monster_group
        self.round_num = 1
        self.score = 0
        self.round_time = 0
        self.num = 0
        self.num_color = [0, 1, 2, 3]
        self.font = pygame.font.Font("/Users/12345/OneDrive/Documents/Abrushow.ttf", 25)
        self.generate_monster()
        self.target_num = random.choice(self.num_color)

    def update(self):
        self.draw()
        self.check_collisions()
        self.game_over()

    def start_screen(self):
        global run
        start_screen = True
        while start_screen:

            screen.fill(BLACK)

            monster_wrangler = self.font.render("Monster Wrangler", True, WHITE)
            monster_rect = monster_wrangler.get_rect()
            monster_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2-50)

            play_text = self.font.render("Press 'Enter' to play", True, WHITE)
            play_rect = play_text.get_rect()
            play_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    start_screen = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        start_screen = False

            screen.blit(monster_wrangler, monster_rect)
            screen.blit(play_text, play_rect)

            pygame.display.flip()

    def draw(self):
        if self.num == 60:
            self.round_time += 1
            self.num = 0
        else:
            self.num += 1
        self.score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.score_rect = self.score_text.get_rect()
        self.score_rect.topleft = (10, 10)

        self.lives_text = self.font.render(f"Lives: {self.player.lives}", True, WHITE)
        self.lives_rect = self.lives_text.get_rect()
        self.lives_rect.topleft = (10, 35)

        self.current_round_text = self.font.render(f"Current Round: {self.round_num}", True, WHITE)
        self.current_round_rect = self.current_round_text.get_rect()
        self.current_round_rect.topleft = (10, 60)

        self.round_time_text = self.font.render(f"Round Time: {self.round_time}", True, WHITE)
        self.round_time_rect = self.round_time_text.get_rect()
        self.round_time_rect.topright = (1200-10, 10)

        self.warp_text = self.font.render(f"Warps: {self.player.warps}", True, WHITE)
        self.warp_rect = self.warp_text.get_rect()
        self.warp_rect.topright = (1200-10, 35)

        self.current_catch = self.font.render("Current Catch:", True, WHITE)
        self.current_rect = self.current_catch.get_rect()
        self.current_rect.topleft = (400, 35)

        pygame.draw.rect(screen, COLORS[self.target_num], (1, 100, WINDOW_WIDTH, WINDOW_HEIGHT-180), 4)

        screen.blit(self.score_text, self.score_rect)
        screen.blit(self.current_catch, self.current_rect)
        screen.blit(self.lives_text, self.lives_rect)
        screen.blit(self.current_round_text, self.current_round_rect)
        screen.blit(self.round_time_text, self.round_time_rect)
        screen.blit(self.warp_text, self.warp_rect)

    def check_collisions(self):
        collided_monster = pygame.sprite.spritecollideany(self.player, self.monster_group)
        if collided_monster:
            if collided_monster.color == self.target_num:
                self.score += 100*self.round_num
                collided_monster.kill()
                self.num_color.remove(self.target_num)
                if self.num_color:
                    self.target_num = random.choice(self.num_color)
                else:
                    self.start_new_round()
                    self.player.rect.y = WINDOW_HEIGHT - 70
                    self.player.rect.x = WINDOW_WIDTH//2
                    self.target_num = random.choice(self.num_color)
            else:
                self.player.lives -= 1
                self.player.rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT-40)

    def generate_monster(self):
        self.num_color = self.num_color*self.round_num
        for num in self.num_color:
            new_monster = Monster(num)
            self.monster_group.add(new_monster)

    def start_new_round(self):
        if self.num_color == []:
            self.round_num += 1
            self.player.warps += 1
            self.num_color = [0, 1, 2, 3]
            self.generate_monster()
            self.round_time = 0

    def game_over(self):
        if self.player.lives <= 0:
            is_paused = True
            while is_paused:
                screen.fill(BLACK)

                final_score_text = self.font.render(f"final score: {self.score}", True, WHITE)
                final_score_rect = final_score_text.get_rect()
                final_score_rect.center = (WINDOW_WIDTH//2, 300)

                play_again_text = self.font.render("press 'Enter' to play again", True, WHITE)
                play_again_rect = play_again_text.get_rect()
                play_again_rect.center = (WINDOW_WIDTH//2, 400)

                screen.blit(final_score_text, final_score_rect)
                screen.blit(play_again_text, play_again_rect)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.score = 0
                            self.round_num = 1
                            self.player.lives = 5
                            self.round_time = 0
                            self.num = 0
                            self.player.warps = 3
                            self.num_color = [0, 1, 2, 3]
                            self.monster_group.empty()
                            self.generate_monster()
                            is_paused = False
                    if event.type == pygame.QUIT:
                        global running
                        is_paused = False
                        running = False
                pygame.display.update()

    def target_monster(self):
        if self.target_num == 0:
            self.image = pygame.image.load("/Users/12345/OneDrive/Documents/purple_monster.png")
            self.rect = self.image.get_rect()
            self.rect.topleft = (600, 20)
            screen.blit(self.image, self.rect)
        if self.target_num == 1:
            self.image = pygame.image.load("/Users/12345/OneDrive/Documents/yellow_monster.png")
            self.rect = self.image.get_rect()
            self.rect.topleft = (600, 20)
            screen.blit(self.image, self.rect)
        if self.target_num == 2:
            self.image = pygame.image.load("/Users/12345/OneDrive/Documents/blue_monster.png")
            self.rect = self.image.get_rect()
            self.rect.topleft = (600, 20)
            screen.blit(self.image, self.rect)
        if self.target_num == 3:
            self.image = pygame.image.load("/Users/12345/OneDrive/Documents/green_monster.png")
            self.rect = self.image.get_rect()
            self.rect.topleft = (600, 20)
            screen.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.warps = 3
        self.lives = 5
        self.velocity = 7
        self.image = pygame.image.load("/Users/12345/OneDrive/Documents/knight.png")
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT-40)

    def update(self):
        self.move()

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self.rect.top > 105:
                self.rect.y -= self.velocity
        if keys[pygame.K_DOWN]:
            if self.rect.bottom < WINDOW_HEIGHT - 90:
                self.rect.y += self.velocity
        if keys[pygame.K_LEFT]:
            if self.rect.left > 5:
                self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            if self.rect.right < WINDOW_WIDTH:
                self.rect.x += self.velocity

    def warping(self):
        if self.warps > 0:
            self.warps -= 1
            self.rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT-40)

class Monster(pygame.sprite.Sprite):
    def __init__(self, color):
        super(Monster, self).__init__()
        self.color = color
        self.monster_type = []
        self.velocity = random.randint(1, 4)
        self.direction = [-1, 1]
        self.dx = random.choice(self.direction)
        self.dy = random.choice(self.direction)
        blue_monster = pygame.image.load("/Users/12345/OneDrive/Documents/blue_monster.png")
        green_monster = pygame.image.load("/Users/12345/OneDrive/Documents/green_monster.png")
        purple_monster = pygame.image.load("/Users/12345/OneDrive/Documents/purple_monster.png")
        yellow_monster = pygame.image.load("/Users/12345/OneDrive/Documents/yellow_monster.png")
        self.monster_type.append(purple_monster)
        self.monster_type.append(yellow_monster)
        self.monster_type.append(blue_monster)
        self.monster_type.append(green_monster)
        if self.color == 0:
            self.image = self.monster_type[0]
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(32, 1200-32), random.randint(120, 700-150))
        if self.color == 1:
            self.image = self.monster_type[1]
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(32, 1200-32), random.randint(120, 700-150))
        if self.color == 2:
            self.image = self.monster_type[2]
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(32, 1200-32), random.randint(120, 700-150))
        if self.color == 3:
            self.image = self.monster_type[3]
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(32, 1200-32), random.randint(120, 700-150))

    def update(self):
        self.move()

    def move(self):
        self.rect.x += self.velocity*self.dx
        self.rect.y += self.velocity*self.dy
        if self.rect.x <= 0:
            self.dx = 1
        if self.rect.right >= WINDOW_WIDTH:
            self.dx = -1
        if self.rect.y <= 110:
            self.dy = 1
        if self.rect.y >= WINDOW_HEIGHT - 150:
            self.dy = -1

my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

my_monster_group = pygame.sprite.Group()

my_game = Game(my_player, my_monster_group)

run = True
my_game.start_screen()

running = True
while running and run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.warping()
    screen.fill(BLACK)

    my_player_group.update()
    my_player_group.draw(screen)

    my_monster_group.update()
    my_monster_group.draw(screen)

    my_game.update()
    my_game.target_monster()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
