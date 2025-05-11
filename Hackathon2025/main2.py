import pygame
from pygame import *
from random import randint

pygame.init()
win_width = 1280
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption("ghost")

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()

    def reset(self):
        window.blit(self.image, self.rect.topleft)

class Player(GameSprite):
    def __init__(self, size_x, size_y):
        self.images = {
            "up": transform.scale(image.load("images/creature.2.png"), (size_x, size_y)),
            "down": transform.scale(image.load("images/creature.3.png"), (size_x, size_y)),
            "left": transform.scale(image.load("images/creature.4.png"), (size_x, size_y)),
            "right": transform.scale(image.load("images/creature.1.png"), (size_x, size_y))
        }
        self.direction = "down"
        super().__init__("images/creature.3.png", size_x, size_y)
        self.x_speed = 0
        self.y_speed = 0

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.rect.clamp_ip(window.get_rect())
        self.image = self.images[self.direction]

class Bullet(sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        base_image = transform.scale(image.load("images/01.png"), (50, 50))
        angle = {"right": 0, "left": 180, "up": 90, "down": -90}[direction]
        self.image = transform.rotate(base_image, angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 12
        self.direction = direction

    def update(self):
        if self.direction == "right": self.rect.x += self.speed
        elif self.direction == "left": self.rect.x -= self.speed
        elif self.direction == "up": self.rect.y -= self.speed
        elif self.direction == "down": self.rect.y += self.speed

        if a == "lvl1":
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    enemy.kill()
                    bullets.remove(self)
                    global score
                    score += 1
                    break

        if a == "lvl3":
            for enemy in enemies_lvl3:
                if self.rect.colliderect(enemy.rect):
                    enemy.kill()
                    bullets.remove(self)
                    score += 1
                    break

        if not window.get_rect().colliderect(self.rect): self.kill()

        if boss and self.rect.colliderect(boss.rect):
            boss.hp -= 5
            self.kill()
        if boss2 and self.rect.colliderect(boss2.rect):
            boss2.hp -= 5
            self.kill()
        if boss3 and self.rect.colliderect(boss3.rect):
            boss3.hp -= 5
            self.kill()

class IceShard(sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = transform.scale(image.load("images/02.png"), (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7
        self.direction = direction

    def update(self):
        if self.direction == "right": self.rect.x += self.speed
        elif self.direction == "left": self.rect.x -= self.speed
        elif self.direction == "up": self.rect.y -= self.speed
        elif self.direction == "down": self.rect.y += self.speed

        if not window.get_rect().colliderect(self.rect):
            self.kill()

class Enemy(GameSprite):
    def __init__(self, image_path, size_x, size_y):
        super().__init__(image_path, size_x, size_y)
        self.rect.x = randint(0, win_width - size_x)
        self.rect.y = randint(0, win_height - size_y)
        self.x_speed = randint(-3, 3)
        self.y_speed = randint(-3, 3)

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.left <= 0 or self.rect.right >= win_width: self.x_speed *= -1
        if self.rect.top <= 0 or self.rect.bottom >= win_height: self.y_speed *= -1

class Enemy2(GameSprite):
    def __init__(self):
        super().__init__("images/enemy2.png", 100, 100)
        self.spawn_at_edge()
        self.x_speed = randint(-4, 4) or 1
        self.y_speed = randint(-4, 4) or 1

    def spawn_at_edge(self):
        edge = randint(1, 4)
        if edge == 1:
            self.rect.x = randint(0, win_width)
            self.rect.y = 0
        elif edge == 2:
            self.rect.x = randint(0, win_width)
            self.rect.y = win_height - self.rect.height
        elif edge == 3:
            self.rect.x = 0
            self.rect.y = randint(0, win_height)
        else:
            self.rect.x = win_width - self.rect.width
            self.rect.y = randint(0, win_height)

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if not window.get_rect().contains(self.rect):
            self.spawn_at_edge()

class Boss(Enemy):
    def __init__(self):
        super().__init__("images/boss.png", 250, 250)
        self.hp = 100

class Boss2(Enemy):
    def __init__(self):
        super().__init__("images/enemy2.png", 250, 250)
        self.hp = 10

class Boss3(GameSprite):
    def __init__(self):
        super().__init__("images/enemy2.png", 250, 250)
        self.spawn_at_edge()
        self.x_speed = 2
        self.y_speed = 2
        self.hp = 1000
        self.last_shot_time = pygame.time.get_ticks()

    def spawn_at_edge(self):
        edge = randint(1, 4)
        if edge == 1:
            self.rect.x = randint(0, win_width)
            self.rect.y = 0
        elif edge == 2:
            self.rect.x = randint(0, win_width)
            self.rect.y = win_height - self.rect.height
        elif edge == 3:
            self.rect.x = 0
            self.rect.y = randint(0, win_height)
        else:
            self.rect.x = win_width - self.rect.width
            self.rect.y = randint(0, win_height)

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if not window.get_rect().contains(self.rect):
            self.spawn_at_edge()

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 1000:
            for dir in ["up", "down", "left", "right"]:
                ice_shards.add(IceShard(self.rect.centerx, self.rect.centery, dir))
            self.last_shot_time = current_time

back_m = transform.scale(image.load("images/menu.png"), (win_width, win_height))
background = transform.scale(image.load("images/floor-tiles.png"), (win_width, win_height))
background_lvl3 = transform.scale(image.load("images/floor.png"), (win_width, win_height))

start_but = GameSprite("images/start.png", 250, 250)
start_but.rect.topleft = (525, -25)
exit_but = GameSprite("images/exit.png", 150, 115)
exit_but.rect.topleft = (570, 425)
music_on_image = transform.scale(image.load("images/song.png"), (100, 100))
music_off_image = transform.scale(image.load("images/no_song.png"), (100, 100))
music_but = GameSprite("images/song.png", 100, 100)
music_but.rect.topleft = (10, 600)

mixer.init()
mixer.music.load("sounds/halloween.wav")
mixer.music.set_volume(0.5)
mixer.music.play(-1)
music_paused = False
music_pos = 0.0

hero = Player(140, 130)
hero.rect.center = (win_width // 2, win_height // 2)

bullets = sprite.Group()
enemies = sprite.Group()
enemies_lvl3 = sprite.Group()
ice_shards = sprite.Group()
for _ in range(20): enemies.add(Enemy("images/enemy.png", 100, 100))

last_shot_time = 0
bullet_cooldown = 0
score = 0
font.init()
font1 = font.SysFont("Arial", 40)
clock = time.Clock()
# ... [весь твой код выше остаётся без изменений]

# ... весь код до run = True остаётся без изменений

boss = None
boss2 = None
boss3 = None
boss3_defeated = False
a = "menu"
dialog_start_time = 0
game_over = False
win = False

run = True
while run:
    window.fill((0, 0, 0))
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == MOUSEBUTTONDOWN and a == "menu":
            if exit_but.rect.collidepoint(e.pos): run = False
            elif start_but.rect.collidepoint(e.pos): a = "lvl1"
            elif music_but.rect.collidepoint(e.pos):
                if music_paused:
                    mixer.music.play(-1, start=music_pos)
                    music_paused = False
                    music_but.image = music_on_image
                else:
                    music_pos = mixer.music.get_pos() / 1000.0
                    mixer.music.stop()
                    music_paused = True
                    music_but.image = music_off_image
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE: a = "menu"
            if a in ("lvl1", "lvl3") and not game_over and not win:
                if e.key == K_LEFT: hero.x_speed = -4; hero.direction = "left"
                if e.key == K_RIGHT: hero.x_speed = 4; hero.direction = "right"
                if e.key == K_UP: hero.y_speed = -4; hero.direction = "up"
                if e.key == K_DOWN: hero.y_speed = 4; hero.direction = "down"
                if e.key == K_SPACE and time.get_ticks() - last_shot_time >= bullet_cooldown:
                    bullets.add(Bullet(hero.rect.centerx, hero.rect.centery, hero.direction))
                    last_shot_time = time.get_ticks()
        elif e.type == KEYUP and a in ("lvl1", "lvl3"):
            if e.key in (K_LEFT, K_RIGHT): hero.x_speed = 0
            if e.key in (K_UP, K_DOWN): hero.y_speed = 0

    if a == "menu":
        window.blit(back_m, (0, 0))
        start_but.reset()
        exit_but.reset()
        music_but.reset()

    elif a == "lvl1":
        window.blit(background, (0, 0))
        hero.update()
        hero.reset()
        enemies.update()
        enemies.draw(window)
        bullets.update()
        bullets.draw(window)

        if not boss and score >= 20: boss = Boss()
        if boss:
            boss.update()
            window.blit(boss.image, boss.rect.topleft)
            pygame.draw.rect(window, (255, 0, 0), (440, 10, 400, 25))
            pygame.draw.rect(window, (0, 255, 0), (440, 10, max(0, int(boss.hp / 100 * 400)), 25))

        if not boss2 and score >= 40: boss2 = Boss2()
        if boss2:
            boss2.update()
            window.blit(boss2.image, boss2.rect.topleft)
            pygame.draw.rect(window, (255, 0, 0), (440, 50, 400, 25))
            pygame.draw.rect(window, (0, 255, 0), (440, 50, max(0, int(boss2.hp / 100 * 400)), 25))

        if boss and boss.hp <= 0:
            boss = None
            a = "dialog"

        if boss2 and boss2.hp <= 0:
            boss2 = None
            dialog_start_time = pygame.time.get_ticks()

        if not game_over:
            if (boss and hero.rect.colliderect(boss.rect)) or (boss2 and hero.rect.colliderect(boss2.rect)):
                game_over = True

        if game_over:
            text = font1.render("Ты проиграл", True, (255, 0, 0))
            window.blit(text, (win_width // 2 - text.get_width() // 2, win_height // 2))

        text = font1.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(text, (10, 650))

    elif a == "dialog":
        window.blit(background, (0, 0))
        creature = GameSprite("images/учоный.png", 200, 200)
        creature.rect.center = (win_width // 2, win_height // 2 - 100)
        creature.reset()
        dialog_text = font1.render("Пока тебя не было, мы разработали новое устройство...", True, (255, 255, 255))
        window.blit(dialog_text, (win_width // 2 - dialog_text.get_width() // 2, win_height // 2 + 50))
        if pygame.time.get_ticks() - dialog_start_time > 5000:
            a = "lvl2"
            dialog_start_time = 0

    elif a == "lvl2":
        if dialog_start_time == 0:
            dialog_start_time = pygame.time.get_ticks()
        window.fill((20, 20, 20))
        text = font1.render("loading", True, (255, 255, 255))
        window.blit(text, (win_width // 2 - text.get_width() // 2, win_height // 2))
        if pygame.time.get_ticks() - dialog_start_time > 5000:
            a = "lvl3"
            dialog_start_time = 0
            for _ in range(20):
                enemies_lvl3.add(Enemy2())

    elif a == "lvl3":
        window.blit(background_lvl3, (0, 0))
        if not game_over and not win:
            hero.update()
        hero.reset()
        enemies_lvl3.update()
        enemies_lvl3.draw(window)
        bullets.update()
        bullets.draw(window)
        ice_shards.update()
        ice_shards.draw(window)

        if not boss3 and not boss3_defeated and len(enemies_lvl3) == 0:
            boss3 = Boss3()
        if boss3:
            boss3.update()
            window.blit(boss3.image, boss3.rect.topleft)
            pygame.draw.rect(window, (255, 0, 0), (440, 10, 400, 25))
            pygame.draw.rect(window, (0, 255, 0), (440, 10, max(0, int(boss3.hp / 1000 * 400)), 25))

            if boss3.hp <= 0:
                boss3 = None
                boss3_defeated = True
                win = True

        if not game_over:
            if (boss3 and hero.rect.colliderect(boss3.rect)) or any(shard.rect.colliderect(hero.rect) for shard in ice_shards):
                game_over = True

        if win:
            text = font1.render("Ты победил", True, (0, 255, 0))
            window.blit(text, (win_width // 2 - text.get_width() // 2, win_height // 2))
        elif game_over:
            text = font1.render("Ты проиграл", True, (255, 0, 0))
            window.blit(text, (win_width // 2 - text.get_width() // 2, win_height // 2))

        text = font1.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(text, (10, 650))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
