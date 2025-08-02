import pygame
import math
import random
from pygame import gfxdraw

pygame.init()

WIDTH, HEIGHT = 900, 700
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
GREEN = (50, 255, 100)
PURPLE = (150, 50, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Defender")

stars = []
for _ in range(200):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.random() * 3,
        random.random() * 0.5 + 0.2
    ])

nebulas = []
for _ in range(5):
    nebulas.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(100, 300),
        (random.randint(0, 100), random.randint(0, 100), random.randint(150, 255), 5),
        random.random() * 0.2
    ])

try:
    buffer = pygame.sndarray.array(pygame.mixer.Sound(buffer=bytes([127] * 4410)))
    for i in range(4410):
        if i < 3000:
            value = int(127 + 127 * math.sin(i * 0.1) * math.exp(-i / 1000))
            buffer[i][0] = value
            buffer[i][1] = value
    shoot_sound = pygame.sndarray.make_sound(buffer)

    buffer = pygame.sndarray.array(pygame.mixer.Sound(buffer=bytes([127] * 22050)))
    for i in range(22050):
        value = int(127 + 127 * random.random() * math.exp(-i / 3000))
        buffer[i][0] = value
        buffer[i][1] = value
    explosion_sound = pygame.sndarray.make_sound(buffer)
except:
    shoot_sound = pygame.mixer.Sound(buffer=bytes([127] * 4410))
    explosion_sound = pygame.mixer.Sound(buffer=bytes([127] * 22050))

title_font = pygame.font.SysFont('Arial', 72, bold=True)
font = pygame.font.SysFont('Arial', 36)
small_font = pygame.font.SysFont('Arial', 24)

game_running = False
particles = []

start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 60)
exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 60)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = random.random() * 4 + 1
        self.color = color
        angle = random.random() * math.pi * 2
        speed = random.random() * 3 + 1
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 60

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size *= 0.95
        return self.life > 0 and self.size > 0.5

    def draw(self):
        alpha = min(255, int(self.life * 4))
        color = (*self.color[:3], alpha)
        pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), int(self.size), color)

def create_explosion(x, y, color, count=30):
    for _ in range(count):
        particles.append(Particle(x, y, color))

def update_background():
    for y in range(0, HEIGHT, 2):
        color_value = int(40 * (1 - y / HEIGHT))
        pygame.draw.line(screen, (color_value, color_value, color_value + 20), (0, y), (WIDTH, y))

    for nebula in nebulas:
        nebula[1] += nebula[4]
        if nebula[1] > HEIGHT + nebula[2]:
            nebula[0] = random.randint(0, WIDTH)
            nebula[1] = -nebula[2]

        surface = pygame.Surface((nebula[2] * 2, nebula[2] * 2), pygame.SRCALPHA)
        for i in range(5):
            size = nebula[2] * (1 - i * 0.2)
            color = (*nebula[3][:3], int(nebula[3][3] * (1 - i * 0.2)))
            pygame.gfxdraw.filled_circle(surface, int(nebula[2]), int(nebula[2]), int(size), color)
        screen.blit(surface, (nebula[0] - nebula[2], nebula[1] - nebula[2]), special_flags=pygame.BLEND_ADD)

    for star in stars:
        star[1] += star[3]
        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0

        size = star[2]
        pygame.gfxdraw.filled_circle(screen, int(star[0]), int(star[1]), int(size), (255, 255, 255))

        if size > 1.5:
            glow_size = size * 3
            glow_surface = pygame.Surface((int(glow_size * 2), int(glow_size * 2)), pygame.SRCALPHA)
            pygame.gfxdraw.filled_circle(glow_surface, int(glow_size), int(glow_size), int(glow_size), (255, 255, 255, 30))
            screen.blit(glow_surface, (int(star[0] - glow_size), int(star[1] - glow_size)), special_flags=pygame.BLEND_ADD)

def draw_menu():
    screen.fill(BLACK)
    update_background()

    title = "COSMIC DEFENDER"
    current_time = pygame.time.get_ticks() / 1000

    total_width = 0
    char_surfaces = []
    for char in title:
        char_surface = title_font.render(char, True, WHITE)
        char_surfaces.append(char_surface)
        total_width += char_surface.get_width()

    x_pos = WIDTH // 2 - total_width // 2
    y_base = HEIGHT // 4

    for i, char in enumerate(title):
        hue = (current_time * 0.5 + i * 0.1) % 1.0
        char_color = pygame.Color(0)
        char_color.hsva = (hue * 360, 100, 100, 100)

        offset_y = math.sin(current_time * 3 + i * 0.5) * 8
        offset_x = math.cos(current_time * 2 + i * 0.3) * 3

        char_surface = title_font.render(char, True, char_color)
        screen.blit(char_surface, (x_pos + offset_x, y_base + offset_y))

        glow_surface = pygame.Surface((char_surface.get_width() + 20, char_surface.get_height() + 20), pygame.SRCALPHA)
        pygame.gfxdraw.filled_circle(glow_surface, char_surface.get_width() // 2 + 10, char_surface.get_height() // 2 + 10, char_surface.get_height() // 2 + 5, (*char_color[:3], 30))
        screen.blit(glow_surface, (x_pos - 10 + offset_x, y_base - 10 + offset_y), special_flags=pygame.BLEND_ADD)

        x_pos += char_surface.get_width()

    pygame.draw.rect(screen, BLUE, start_button, border_radius=15)
    pygame.draw.rect(screen, RED, exit_button, border_radius=15)
    pygame.draw.rect(screen, WHITE, start_button, 3, border_radius=15)
    pygame.draw.rect(screen, WHITE, exit_button, 3, border_radius=15)

    start_text = font.render("START", True, WHITE)
    exit_text = font.render("EXIT", True, WHITE)
    screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2, start_button.centery - start_text.get_height() // 2))
    screen.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2, exit_button.centery - exit_text.get_height() // 2))

    subtitle = small_font.render("Navigate with Arrow Keys • Fire with Space", True, CYAN)
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2 + 120))

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.width = 60
        self.height = 80
        self.speed = 7
        self.lives = 3
        self.thrust = 0
        self.shield_active = False
        self.shield_timer = 0

    def move(self, direction):
        if direction == "LEFT" and self.x > 0:
            self.x -= self.speed
        if direction == "RIGHT" and self.x < WIDTH - self.width:
            self.x += self.speed
        self.thrust = min(1.0, self.thrust + 0.1)

    def activate_shield(self):
        self.shield_active = True
        self.shield_timer = 60

    def update(self):
        self.thrust = max(0, self.thrust - 0.05)
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False

    def draw(self):
        ship_points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width // 2, self.y + self.height - 20),
            (self.x + self.width, self.y + self.height),
        ]
        pygame.gfxdraw.aapolygon(screen, ship_points, BLUE)
        pygame.gfxdraw.filled_polygon(screen, ship_points, BLUE)

        wing_points = [
            (self.x + 10, self.y + 20),
            (self.x - 10, self.y + 40),
            (self.x + 10, self.y + 60),
        ]
        pygame.gfxdraw.aapolygon(screen, wing_points, CYAN)
        pygame.gfxdraw.filled_polygon(screen, wing_points, CYAN)

        wing_points = [
            (self.x + self.width - 10, self.y + 20),
            (self.x + self.width + 10, self.y + 40),
            (self.x + self.width - 10, self.y + 60),
        ]
        pygame.gfxdraw.aapolygon(screen, wing_points, CYAN)
        pygame.gfxdraw.filled_polygon(screen, wing_points, CYAN)

        pygame.gfxdraw.filled_circle(screen, self.x + self.width // 2, self.y + 30, 10, YELLOW)
        pygame.gfxdraw.aacircle(screen, self.x + self.width // 2, self.y + 30, 10, WHITE)

        if self.thrust > 0:
            thrust_points = [
                (self.x + 20, self.y + self.height - 10),
                (self.x + self.width // 2, self.y + self.height + 20 * self.thrust),
                (self.x + self.width - 20, self.y + self.height - 10),
            ]
            thrust_color = (255, int(100 + 155 * self.thrust), 50)
            pygame.gfxdraw.filled_polygon(screen, thrust_points, thrust_color)
            pygame.gfxdraw.aapolygon(screen, thrust_points, WHITE)

            glow_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            glow_radius = int(20 * self.thrust)
            pygame.gfxdraw.filled_circle(glow_surface, 50, 30, glow_radius, (*thrust_color, 50))
            screen.blit(glow_surface, (self.x + self.width // 2 - 50, self.y + self.height - 30), special_flags=pygame.BLEND_ADD)

        if self.shield_active:
            shield_alpha = int(100 * (self.shield_timer / 60))
            shield_surface = pygame.Surface((self.width + 40, self.height + 40), pygame.SRCALPHA)
            pygame.gfxdraw.filled_circle(shield_surface, self.width // 2 + 20, self.height // 2 + 20, self.width // 2 + 10, (100, 200, 255, shield_alpha))
            pygame.gfxdraw.aacircle(shield_surface, self.width // 2 + 20, self.height // 2 + 20, self.width // 2 + 10, (255, 255, 255, shield_alpha + 50))
            screen.blit(shield_surface, (self.x - 20, self.y - 20), special_flags=pygame.BLEND_ADD)

class Enemy:
    def __init__(self):
        self.type = random.choice(["scout", "fighter", "bomber"])
        self.x = random.randint(50, WIDTH - 100)
        self.y = random.randint(-200, -50)

        if self.type == "scout":
            self.size = 40
            self.speed = random.uniform(3, 5)
            self.color = GREEN
            self.health = 1
            self.points = 10
        elif self.type == "fighter":
            self.size = 50
            self.speed = random.uniform(2, 3.5)
            self.color = PURPLE
            self.health = 2
            self.points = 20
        else:
            self.size = 60
            self.speed = random.uniform(1.5, 2.5)
            self.color = RED
            self.health = 3
            self.points = 30

        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)

    def move(self):
        self.y += self.speed
        self.rotation = (self.rotation + self.rotation_speed) % 360

        if self.type != "scout" and random.random() < 0.02:
            self.x += random.randint(-5, 5)
            self.x = max(self.size, min(WIDTH - self.size, self.x))

        if self.y > HEIGHT:
            return True
        return False

    def hit(self):
        self.health -= 1
        return self.health <= 0

    def draw(self):
        if self.type == "scout":
            pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), int(self.size / 2), self.color)
            pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), int(self.size / 2), WHITE)

            pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y - self.size / 4), int(self.size / 4), BLUE)
            pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y - self.size / 4), int(self.size / 4), WHITE)

        elif self.type == "fighter":
            points = []
            for angle in range(0, 360, 72):
                rad = math.radians(angle + self.rotation)
                points.append((self.x + math.cos(rad) * self.size / 2, self.y + math.sin(rad) * self.size / 2))
                rad = math.radians(angle + 36 + self.rotation)
                points.append((self.x + math.cos(rad) * self.size / 4, self.y + math.sin(rad) * self.size / 4))

            pygame.gfxdraw.filled_polygon(screen, points, self.color)
            pygame.gfxdraw.aapolygon(screen, points, WHITE)

            pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), int(self.size / 6), YELLOW)

        else:
            points = []
            for angle in range(0, 360, 45):
                rad = math.radians(angle + self.rotation)
                points.append((self.x + math.cos(rad) * self.size / 2, self.y + math.sin(rad) * self.size / 2))

            pygame.gfxdraw.filled_polygon(screen, points, self.color)
            pygame.gfxdraw.aapolygon(screen, points, WHITE)

            pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), int(self.size / 3), YELLOW)
            pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), int(self.size / 3), WHITE)

            for i in range(self.health):
                angle = i * 120 + self.rotation
                rad = math.radians(angle)
                health_x = self.x + math.cos(rad) * self.size / 4
                health_y = self.y + math.sin(rad) * self.size / 4
                pygame.gfxdraw.filled_circle(screen, int(health_x), int(health_y), 5, GREEN)

        glow_surface = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
        glow_color = (*self.color[:3], 30)
        pygame.gfxdraw.filled_circle(glow_surface, int(self.size * 1.5), int(self.size * 1.5), int(self.size / 2), glow_color)
        screen.blit(glow_surface, (int(self.x - self.size * 1.5), int(self.y - self.size * 1.5)), special_flags=pygame.BLEND_ADD)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 20
        self.speed = 10
        self.active = True
        self.color = CYAN
        self.trail = []

    def move(self):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)

        self.y -= self.speed
        if self.y < -self.height:
            self.active = False

    def draw(self):
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = int(255 * i / len(self.trail))
            trail_color = (*self.color[:3], alpha // 3)
            trail_size = int(self.width * (0.5 + i / len(self.trail) / 2))
            pygame.gfxdraw.filled_circle(screen, int(trail_x), int(trail_y + self.height // 2), trail_size, trail_color)

        bullet_surface = pygame.Surface((self.width * 4, self.height), pygame.SRCALPHA)
        pygame.gfxdraw.filled_ellipse(bullet_surface, self.width * 2, self.height // 2, self.width, self.height // 2, self.color)
        glow_color = (*self.color[:3], 50)
        pygame.gfxdraw.filled_ellipse(bullet_surface, self.width * 2, self.height // 2, self.width * 2, self.height, glow_color)
        screen.blit(bullet_surface, (int(self.x - self.width * 2), int(self.y)))

class PowerUp:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = -50
        self.size = 20
        self.speed = 2
        self.type = random.choice(["shield", "life", "speed"])
        self.color = BLUE if self.type == "shield" else RED if self.type == "life" else YELLOW
        self.rotation = 0

    def move(self):
        self.y += self.speed
        self.rotation = (self.rotation + 2) % 360
        return self.y > HEIGHT

    def draw(self):
        points = []
        for i in range(8):
            angle = i * 45 + self.rotation
            rad = math.radians(angle)
            radius = self.size if i % 2 == 0 else self.size / 2
            points.append((self.x + math.cos(rad) * radius, self.y + math.sin(rad) * radius))

        pygame.gfxdraw.filled_polygon(screen, points, self.color)
        pygame.gfxdraw.aapolygon(screen, points, WHITE)

        if self.type == "shield":
            pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), int(self.size / 3), WHITE)
        elif self.type == "life":
            pygame.draw.rect(screen, WHITE, (self.x - 3, self.y - 3, 6, 6))
            pygame.draw.rect(screen, WHITE, (self.x + 3, self.y - 3, 6, 6))
            pygame.draw.polygon(screen, WHITE, [(self.x, self.y + 8), (self.x - 9, self.y - 1), (self.x + 9, self.y - 1)])
        else:
            pygame.draw.polygon(screen, WHITE, [
                (self.x - 5, self.y - 7),
                (self.x + 2, self.y - 7),
                (self.x - 2, self.y + 7),
                (self.x + 5, self.y + 7)
            ])

        glow_surface = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
        glow_color = (*self.color[:3], 50)
        pygame.gfxdraw.filled_circle(glow_surface, int(self.size * 2), int(self.size * 2), int(self.size), glow_color)
        screen.blit(glow_surface, (int(self.x - self.size * 2), int(self.y - self.size * 2)), special_flags=pygame.BLEND_ADD)

def game_loop():
    global game_running, particles
    clock = pygame.time.Clock()
    player = Player()
    enemies = [Enemy() for _ in range(5)]
    bullets = []
    power_ups = []
    particles = []
    score = 0
    next_powerup = random.randint(500, 1000)
    last_bullet_time = 0
    bullet_cooldown = 300

    while game_running:
        current_time = pygame.time.get_ticks()
        screen.fill(BLACK)
        update_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False
                    return None

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move("LEFT")
        if keys[pygame.K_RIGHT]:
            player.move("RIGHT")
        if keys[pygame.K_SPACE] and current_time - last_bullet_time > bullet_cooldown:
            bullets.append(Bullet(player.x + player.width // 2 - 2, player.y))
            shoot_sound.play()
            last_bullet_time = current_time

        for particle in particles[:]:
            if not particle.update():
                particles.remove(particle)
            else:
                particle.draw()

        next_powerup -= 1
        if next_powerup <= 0:
            power_ups.append(PowerUp())
            next_powerup = random.randint(500, 1000)

        for power_up in power_ups[:]:
            if power_up.move():
                power_ups.remove(power_up)
            else:
                power_up.draw()

                distance = math.sqrt((power_up.x - (player.x + player.width / 2)) ** 2 + (power_up.y - (player.y + player.height / 2)) ** 2)
                if distance < power_up.size + player.width / 2:
                    if power_up.type == "shield":
                        player.activate_shield()
                    elif power_up.type == "life":
                        player.lives = min(5, player.lives + 1)
                    else:
                        player.speed = min(12, player.speed + 1)

                    create_explosion(power_up.x, power_up.y, power_up.color, 20)
                    power_ups.remove(power_up)
                    continue

        player.update()

        for bullet in bullets[:]:
            bullet.move()
            bullet.draw()
            if not bullet.active:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            if enemy.move():
                if not player.shield_active:
                    player.lives -= 1
                    create_explosion(player.x + player.width // 2, player.y + player.height // 2, RED, 20)
                    if player.lives == 0:
                        game_running = False
                        return score
                else:
                    player.shield_active = False
                enemies.remove(enemy)
                enemies.append(Enemy())
            enemy.draw()

        for bullet in bullets[:]:
            for enemy in enemies[:]:
                distance = math.sqrt((bullet.x - enemy.x) ** 2 + (bullet.y - enemy.y) ** 2)
                if distance < enemy.size / 2 + bullet.width:
                    if bullet in bullets:
                        bullets.remove(bullet)

                    create_explosion(enemy.x, enemy.y, enemy.color, 20)
                    explosion_sound.play()

                    if enemy.hit():
                        score += enemy.points
                        enemies.remove(enemy)
                        enemies.append(Enemy())
                    break

        player.draw()

        score_text = font.render(f"SCORE: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))

        for i in range(player.lives):
            mini_ship_points = [
                (30 + i * 30, 80),
                (20 + i * 30, 100),
                (40 + i * 30, 100)
            ]
            pygame.gfxdraw.filled_polygon(screen, mini_ship_points, BLUE)
            pygame.gfxdraw.aapolygon(screen, mini_ship_points, WHITE)

        pygame.draw.rect(screen, (30, 30, 50), (0, HEIGHT - 40, WIDTH, 40))

        shield_text = small_font.render("SHIELD:", True, CYAN)
        screen.blit(shield_text, (20, HEIGHT - 30))
        shield_status = "ACTIVE" if player.shield_active else "INACTIVE"
        shield_color = BLUE if player.shield_active else RED
        shield_status_text = small_font.render(shield_status, True, shield_color)
        screen.blit(shield_status_text, (100, HEIGHT - 30))

        speed_text = small_font.render(f"SPEED: {player.speed}", True, YELLOW)
        screen.blit(speed_text, (250, HEIGHT - 30))

        pygame.display.flip()
        clock.tick(FPS)

    return None

def game_over_screen(score):
    global game_running
    waiting = True

    while waiting:
        screen.fill(BLACK)
        update_background()

        game_over_text = title_font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))

        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))

        retry_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60)
        pygame.draw.rect(screen, GREEN, retry_button, border_radius=15)
        pygame.draw.rect(screen, WHITE, retry_button, 3, border_radius=15)

        retry_text = font.render("RETRY", True, WHITE)
        screen.blit(retry_text, (retry_button.centerx - retry_text.get_width() // 2, retry_button.centery - retry_text.get_height() // 2))

        menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 130, 200, 60)
        pygame.draw.rect(screen, BLUE, menu_button, border_radius=15)
        pygame.draw.rect(screen, WHITE, menu_button, 3, border_radius=15)

        menu_text = font.render("MENU", True, WHITE)
        screen.blit(menu_text, (menu_button.centerx - menu_text.get_width() // 2, menu_button.centery - menu_text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    game_running = True
                    return True
                elif menu_button.collidepoint(event.pos):
                    return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_RETURN:
                    game_running = True
                    return True

        pygame.display.flip()

def main():
    global game_running, particles
    running = True

    while running:
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_running = True
                    particles = []
                    final_score = game_loop()
                    if final_score is not None:
                        retry = game_over_screen(final_score)
                        if not retry:
                            game_running = False
                elif exit_button.collidepoint(event.pos):
                    running = False
                    pygame.quit()
                    return

        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()
