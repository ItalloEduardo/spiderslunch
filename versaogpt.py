import pygame
import random

# Inicializa o pygame
pygame.init()

# Dimensões da tela
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Aranha")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fontes
font = pygame.font.SysFont(None, 40)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Posições dos pontos da teia
points = [(100, 100), (500, 100), (300, 200), (100, 300), (500, 300), (300, 400)]

# Função para desenhar a teia
def draw_web():
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            pygame.draw.line(screen, WHITE, points[i], points[j], 2)

# Função para exibir texto na tela
def draw_text(text, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])

# Classe Aranha
class Spider:
    def __init__(self):
        self.position = 0  # Começa no primeiro ponto da teia
        self.stamina = 10
    
    def move(self, direction):
        new_position = self.position
        if direction == 'up' and new_position - 2 >= 0:
            new_position -= 2
        elif direction == 'down' and new_position + 2 < len(points):
            new_position += 2
        elif direction == 'left' and new_position - 1 >= 0:
            new_position -= 1
        elif direction == 'right' and new_position + 1 < len(points):
            new_position += 1

        if new_position != self.position:
            self.stamina -= 1
            self.position = new_position

    def draw(self):
        pygame.draw.circle(screen, BLUE, points[self.position], 15)

# Classe Mosca
class Fly:
    def __init__(self):
        self.position = random.randint(0, len(points) - 1)
    
    def respawn(self):
        self.position = random.randint(0, len(points) - 1)
    
    def draw(self):
        pygame.draw.circle(screen, GREEN, points[self.position], 10)

# Função principal do jogo
def game():
    spider = Spider()
    fly = Fly()

    game_over = False

    while not game_over:
        screen.fill(BLACK)
        draw_web()
        spider.draw()
        fly.draw()
        
        # Verifica se a aranha alcançou a mosca
        if spider.position == fly.position:
            fly.respawn()
            spider.stamina += 8
        
        # Exibe a stamina
        draw_text(f"Stamina: {spider.stamina}", WHITE, 10, 10)

        # Verifica se a stamina acabou
        if spider.stamina <= 0:
            game_over = True

        # Eventos e movimentação por toque de tecla
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    spider.move('up')
                if event.key == pygame.K_DOWN:
                    spider.move('down')
                if event.key == pygame.K_LEFT:
                    spider.move('left')
                if event.key == pygame.K_RIGHT:
                    spider.move('right')

        pygame.display.update()
        clock.tick(FPS)

    # Tela de derrota
    while game_over:
        screen.fill(BLACK)
        draw_text("GAME OVER", RED, WIDTH // 2 - 100, HEIGHT // 2 - 50)
        draw_text("Pressione R para reiniciar", WHITE, WIDTH // 2 - 150, HEIGHT // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game()

# Inicia o jogo
game()
