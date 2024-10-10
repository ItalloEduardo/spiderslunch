import pygame
import networkx as nx
import random
import time

# Configurações do jogo
WIDTH, HEIGHT = 800, 600
NODE_RADIUS = 20
FPS = 60
STAMINA_DECREASE = 1
STAMINA_INCREASE = 8
MOSCA_INTERVAL = 5  # Segundos

# Inicializa o pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Qiqi e a Teia")

# Fontes
font = pygame.font.Font(None, 36)

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Classe para a Aranha Qiqi
class Qiqi:
    def __init__(self, node):
        self.node = node
        self.stamina = 5
        self.moscas_comidas = 0

    def move(self, target_node):
        if self.stamina > 0:
            # Gasta 1 de Stamina por movimento
            self.stamina -= STAMINA_DECREASE
            self.node = target_node

    def eat_mosca(self):
        self.stamina = min(20, self.stamina + STAMINA_INCREASE)
        self.moscas_comidas += 1

# Função para desenhar o grafo (teia)
def draw_graph(G, pos, qiqi, mosca_node):
    screen.fill(WHITE)
    
    # Desenha as arestas
    for edge in G.edges():
        pygame.draw.line(screen, BLACK, pos[edge[0]], pos[edge[1]], 2)
    
    # Desenha os nós
    for node in G.nodes():
        color = BLUE if node == qiqi.node else GREEN if node == mosca_node else BLACK
        pygame.draw.circle(screen, color, pos[node], NODE_RADIUS)
    
    # Desenha a Stamina e o número de moscas comidas
    stamina_text = font.render(f"Stamina: {qiqi.stamina}", True, BLACK)
    moscas_text = font.render(f"Moscas comidas: {qiqi.moscas_comidas}", True, BLACK)
    screen.blit(stamina_text, (10, 10))
    screen.blit(moscas_text, (10, 50))

# Função para desenhar a tela de Game Over
def game_over_screen(qiqi):
    screen.fill(RED)
    game_over_text = font.render("GAME OVER", True, WHITE)
    moscas_text = font.render(f"Moscas comidas: {qiqi.moscas_comidas}", True, WHITE)
    retry_text = font.render("Pressione R para Jogar Novamente", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    screen.blit(moscas_text, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(retry_text, (WIDTH // 2 - 180, HEIGHT // 2 + 50))
    
    pygame.display.update()

# Função principal
def main():
    clock = pygame.time.Clock()
    
    # Cria o grafo
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3), (0, 3), (1, 3), (3, 4)])
    pos = nx.spring_layout(G, scale=2)  # Layout para posicionar os nós
    
    # Converte as posições para coordenadas da tela
    pos = {node: (int(pos[node][0] * WIDTH // 2 + WIDTH // 2), 
                  int(pos[node][1] * HEIGHT // 2 + HEIGHT // 2)) for node in pos}
    
    # Inicializa Qiqi e a mosca
    qiqi = Qiqi(random.choice(list(G.nodes)))
    mosca_node = random.choice(list(G.nodes))
    last_mosca_time = time.time()

    # Estado do jogo
    running = True
    game_over = False
    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                main()  # Reinicia o jogo
            
        if game_over:
            game_over_screen(qiqi)
            continue

        # Movimento da aranha com as teclas direcionais
        keys = pygame.key.get_pressed()
        neighbors = list(G.neighbors(qiqi.node))
        
        if keys[pygame.K_LEFT] and neighbors:
            qiqi.move(neighbors[0])
        elif keys[pygame.K_RIGHT] and neighbors:
            qiqi.move(neighbors[1])

        # Verifica se a Qiqi comeu a mosca
        if qiqi.node == mosca_node:
            qiqi.eat_mosca()
            mosca_node = random.choice(list(G.nodes))  # Nova mosca em posição aleatória
            last_mosca_time = time.time()

        # Checa se é hora de criar uma nova mosca
        if time.time() - last_mosca_time > MOSCA_INTERVAL:
            mosca_node = random.choice(list(G.nodes))
            last_mosca_time = time.time()

        # Verifica se a Stamina chegou a 0
        if qiqi.stamina <= 0:
            game_over = True

        # Desenha o grafo e os status
        draw_graph(G, pos, qiqi, mosca_node)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
