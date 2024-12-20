import pygame
import sys
import random

# Pygame'i başlat
pygame.init()

# Oyun ekranı boyutları
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Saat
clock = pygame.time.Clock()
FPS = 60

# Oyun değişkenleri
gravity = 0.5
bird_movement = 0
bird_start_x, bird_start_y = WIDTH // 4, HEIGHT // 2
bird = pygame.Rect(bird_start_x, bird_start_y, 30, 30)

pipe_width = 60
pipe_gap = 150
pipe_speed = 4
pipes = []
score = 0
scored_pipes = set()

# Font
font = pygame.font.Font(None, 40)

# Yeni boru oluşturma fonksiyonu
def create_pipe():
    pipe_height = random.randint(150, HEIGHT - 150)
    bottom_pipe = pygame.Rect(WIDTH, pipe_height, pipe_width, HEIGHT - pipe_height)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, pipe_height - pipe_gap)
    return top_pipe, bottom_pipe

# Boruları hareket ettirme ve ekrandan silme
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return [pipe for pipe in pipes if pipe.right > 0]

# Çarpışma kontrolü
def check_collision(pipes):
    for pipe in pipes:
        if bird.colliderect(pipe):
            return True
    if bird.top <= 0 or bird.bottom >= HEIGHT:
        return True
    return False

# Skor güncelleme
def display_score(score):
    score_surface = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_surface, (10, 10))

# Başlangıç boruları
if not pipes:
    pipes.extend(create_pipe())

# Oyun döngüsü
running = True
while running:
    screen.fill(BLUE)  # Arka plan rengi

    # Etkinlik dinleyicisi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = -8  # Kuşu zıplat

    # Kuş hareketi
    bird_movement += gravity
    bird.centery += bird_movement
    pygame.draw.ellipse(screen, RED, bird)

    # Boruları hareket ettir ve çiz
    pipes = move_pipes(pipes)
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

    # Yeni borular ekle
    if pipes and pipes[-1].centerx < WIDTH // 2:
        pipes.extend(create_pipe())

    # Çarpışma kontrolü
    if check_collision(pipes):
        running = False

    # Skor
    for pipe in pipes:
        if bird.centerx > pipe.centerx and pipe not in scored_pipes and pipe.top == 0:
            score += 1
            scored_pipes.add(pipe)
    display_score(score)

    # Ekranı güncelle
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
