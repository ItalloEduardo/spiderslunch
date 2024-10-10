import pygame
import networkx as nx
import random
from teiaAranha import lista_adj

#constantes
LARGURA, ALTURA = 800, 800
RAIO_VERTICE = 10
FPS = 60
PESO_ARESTA = 1
BONUS_MOSCA = 8

#variaveis globais
angulo_mosca = 0
direcao_mosca = 1 #1 para direita, -1 para esquerda

#cores RGB
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
DOURADO = (218, 165, 32)

#starta o pygame
pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Spider's Lunch v0.1.3")

#imagens
bg_jogo = pygame.image.load("assets/images/luar4.jpg")
bg_jogo = pygame.transform.scale(bg_jogo, (LARGURA, ALTURA))
menu_bg = pygame.image.load("assets/images/menu2.png")
menu_bg = pygame.transform.scale(menu_bg, (LARGURA, ALTURA))
gover_dg = pygame.image.load("assets/images/gameover1.jpg")
gover_dg = pygame.transform.scale(gover_dg, (LARGURA, ALTURA))
placa = pygame.image.load("assets/images/placa.png").convert_alpha()
placa = pygame.transform.scale(placa, (280, 70))
aranha_sprite = pygame.image.load("assets/images/aranhazinha.png").convert_alpha()
aranha_sprite = pygame.transform.scale(aranha_sprite, (RAIO_VERTICE * 8, RAIO_VERTICE * 8))
mosca_sprite = pygame.image.load("assets/images/Mosca.png").convert_alpha()
mosca_sprite = pygame.transform.scale(mosca_sprite, (RAIO_VERTICE * 8, RAIO_VERTICE * 8))

#fontes
f_alagard = pygame.font.Font("assets/fonts/alagard.ttf", 25)
f_arcade = pygame.font.Font("assets/fonts/upheavtt.ttf", 25)
f_score = pygame.font.Font("assets/fonts/upheavtt.ttf", 20)
f_spider = pygame.font.Font("assets/fonts/Spider.otf", 90)

#musicas e sons
som_passo = pygame.mixer.Sound("assets/sounds/passoAranha.mp3") 
som_notPasso = pygame.mixer.Sound("assets/sounds/notpassoAranha.mp3") 
som_morteAranha = pygame.mixer.Sound("assets/sounds/morteAranha.mp3") 
som_comerMosca = pygame.mixer.Sound("assets/sounds/moscaAranha.mp3") 
#volumes
som_notPasso.set_volume(0.01)
som_passo.set_volume(0.5)
som_morteAranha.set_volume(0.1)
som_comerMosca.set_volume(1)

#classes
class Botao:
  def __init__(self, x, y, texto):
    self.x = x
    self.y = y
    self.texto = texto
    self.is_hovered = False

  def desenhar(self, tela):
    cor = DOURADO if self.is_hovered else BRANCO
    texto = f_arcade.render(self.texto, True, cor)
    hitbox = texto.get_rect(center=(self.x, self.y))
    tela.blit(texto, hitbox)
  
  def check_hover(self, mouse_pos):
    texto = f_arcade.render(self.texto, True, BRANCO)
    hitbox = texto.get_rect(center=(self.x, self.y))
    self.is_hovered = hitbox.collidepoint(mouse_pos)
  
  def clicou(self, pos):
    texto = f_arcade.render(self.texto, True, BRANCO)
    hitbox = texto.get_rect(center=(self.x, self.y))
    return hitbox.collidepoint(pos)

  # movimento da aranha
  # captura de moscas
class Aranha:
  def __init__(self, vertice):
    self.vertice = vertice
    self.stamina = 50
    self.moscas_comidas = 0
  
  def move(self, vertice_alvo):
    if self.stamina > 0:
      self.stamina -= PESO_ARESTA
      self.vertice = vertice_alvo
      som_passo.play()
  
  def comer(self):
    self.stamina = min(200, self.stamina + BONUS_MOSCA)
    self.moscas_comidas += 1
    som_comerMosca.play()

#desenha a tela inicial
def tela_inicial():
  pygame.mixer.music.load("assets/sounds/fundoMenu.mp3")  # carrega a musica da tela inicial
  pygame.mixer.music.play(-1)                             # toca a musica em looping
  pygame.mixer.music.set_volume(0.1)                      # controla o volume do audio
  tela.blit(menu_bg, (0,0))  #DESENHA O BACKGROUND

  nome_spider = f_spider.render("SPIDERS", True, BRANCO)
  nome_lunch = f_spider.render("LUNCH", True, BRANCO)

  start_btn = Botao(LARGURA * 0.1, ALTURA * 0.9, "Jogar")
  quit_btn = Botao(LARGURA * 0.1 - 8, ALTURA * 0.9 + 25, "Sair")

  tela.blit(nome_spider, (LARGURA * 0.05, ALTURA * 0.08))
  tela.blit(nome_lunch, (LARGURA * 0.05, ALTURA * 0.08 + 80))

  #event listenner
  esperando = True
  while esperando:
    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        pygame.quit()
        exit()

      if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
        esperando = False
        pygame.mixer.music.stop()   #encerra a musica
        rodar_jogo()

      if evento.type == pygame.MOUSEBUTTONDOWN:
        if evento.button == 1:
          if start_btn.clicou(evento.pos):
            esperando = False
            pygame.mixer.music.stop() #encerra a musica
            rodar_jogo()
          if quit_btn.clicou(evento.pos):
            pygame.quit()
            exit()

      if evento.type == pygame.MOUSEMOTION:
        start_btn.check_hover(evento.pos)
        quit_btn.check_hover(evento.pos)
    
      start_btn.desenhar(tela)
      quit_btn.desenhar(tela)
      
      pygame.display.update()

def rodar_jogo():
  pygame.mixer.music.load("assets/sounds/fundoJogo.mp3")
  pygame.mixer.music.play(-1)
  pygame.mixer.music.set_volume(0.1)

  #cria o grafo e define a posição na tela

  #inicializa a aranha e as moscas

  #botão de voltar ao menu
  voltar_btn = Botao(LARGURA - 60, 20, "Voltar")
  
  rodando = True
  derrota = False

  #loop infinito
  while rodando:
    tela.blit(bg_jogo, (0,0)) #desenha e atualiza os objetos na tela
    desenhar_fase()
    #animação da mosca se debatendo na teia

    #game over

    #mapeamento de teclas e vizinhos
    
    #movimentação da aranha com as setas

    #verifica se a aranha comeu uma mosca
    
    #escutador de eventos
    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        rodando = False #sair do jogo
      
      if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
        rodando = False
        tela_inicial()

      if evento.type == pygame.MOUSEMOTION: #hover
        voltar_btn.check_hover(evento.pos)
      if evento.type == pygame.MOUSEBUTTONDOWN: #click
        if evento.button == 1:
          if voltar_btn.clicou(evento.pos):
            rodando = False
            tela_inicial()
    
    voltar_btn.desenhar(tela)
    pygame.display.update()
    #chamada da tela de derrota

tela_inicial()