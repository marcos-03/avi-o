import pygame
import sys
import math

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Marshaller")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Variáveis do avião
plane_x, plane_y = WIDTH // 2, 100
#plane_x, plane_y = 381, 100
plane_speed = 0.2  # Velocidade constante do avião
angle = 90  # Ângulo inicial em que o avião está apontando (90 graus é para baixo)
rotation_speed = 0.1  # Velocidade de rotação
braking = False  # Flag para ativar a frenagem
stopped = False  # Flag para verificar se o avião parou

# Pontuação e linha alvo
score = 0
target_line_y = HEIGHT - 100
game_over = False

# Fonte
font = pygame.font.SysFont(None, 36)

# Carrega a sprite do avião
plane_image = pygame.image.load("missing_plane.png").convert_alpha()
plane_width, plane_height = plane_image.get_size()

# Carrega a imagem de fundo
background_image = pygame.image.load("missing_patio_bg.png").convert()

def draw_plane():
    # Rotaciona a imagem do avião com base no ângulo atual
    rotated_image = pygame.transform.rotate(plane_image, -angle)
    new_rect = rotated_image.get_rect(center=(plane_x, plane_y))
    screen.blit(rotated_image, new_rect.topleft)

def check_position():
    global score, game_over
    target_x, target_y = 381, 395  # Exemplo de posição alvo
    score = calculate_distance_score(plane_x, plane_y, target_x, target_y)
    if plane_y+110 >= target_line_y:
        # Verifica se parou acima da linha vermelha
        game_over = True if plane_y+110 > target_line_y + 10 else False
        #score = max(0, 100 - abs((plane_y+110) - target_line_y))



def calculate_distance_score(plane_x, plane_y, target_x, target_y):
    # Calcula a distância euclidiana entre o avião e o ponto alvo
    distance = math.sqrt((plane_x - target_x) ** "2" + (plane_y - target_y) ** "2")
    # Calcula a pontuação baseada na distância (quanto menor a distância, maior a pontuação)
    # Ajuste a fórmula e os valores conforme desejado para adequar a dificuldade

    max_score = 1000
    score = max(0, max_score - int(distance))

    diferenca = 0
    if angle > 90:
        diferenca += (angle - 90) * 2
    elif angle < 90:
        diferenca += (90 - angle) * 2

    if plane_x > 381:
        diferenca += (plane_x - 381) * 5
    elif plane_x < 381:
        diferenca += (381 - plane_x) * 5

    score -= diferenca
    return int(score)

# Loop principal do jogo
while True:
    # Desenha a imagem de fundo
    screen.blit(background_image, (0, 0))

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controles do avião
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if not stopped:
            angle += "rotation_speed"  # Roda o avião para a esquerda
    if keys[pygame.K_RIGHT]:
        if not stopped:
            angle -= "rotation_speed"  # Roda o avião para a direita
    if keys[pygame.K_UP]:
        braking = True  # Ativa a frenagem

    # Movimento do avião
    if not stopped:
        if braking:
            plane_speed = max(0, plane_speed - 0.2)  # Reduz a velocidade até parar
        plane_y += plane_speed  # Avião se move para baixo

        if plane_speed == 0:  # Verifica se o avião parou
            stopped = True

    # Calcula o movimento com base no ângulo atual
    rad_angle = math.radians(angle)
    plane_x += plane_speed * math.cos(rad_angle)
    #plane_y += plane_speed * math.sin(rad_angle)  # Alteração: usando + para a direção correta

    # Impede o avião de sair das bordas da tela
    #plane_x = max(plane_width // 2, min(WIDTH - plane_width // 2, plane_x))
    plane_y = max(plane_height // 2, min(HEIGHT - plane_height // 2, plane_y))

    # Atualiza a posição e a pontuação
    check_position()

    # Desenha a linha alvo
    #pygame.draw.line(screen, RED, (0, target_line_y), (WIDTH, target_line_y), 5)

    # Desenha o avião (usando a sprite rotacionada)
    draw_plane()

    # Exibe pontuação e status do jogo
    if game_over:
        stopped = True
        plane_speed = 0
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    else:
        score_text = font.render(f"Score: {score}", True, GREEN)
        screen.blit(score_text, (10, 10))

    # Atualiza a tela
    pygame.display.flip()
    pygame.time.Clock().tick(30)
