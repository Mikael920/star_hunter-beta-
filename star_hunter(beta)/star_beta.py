import pygame
import random

# Inicializando o pygame
pygame.init()

# Definindo as dimensões da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Coletor de Estrelas")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Geração das imagens
background_image = pygame.image.load('bg5.jpg')  # Imagem do background
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Redimensiona o background
ship_image = pygame.image.load('6B.png')  # Imagem da nave
star_image = pygame.image.load('star2.png')  # Imagem da estrela
danger_item_image = pygame.image.load('astroid.png')  # Imagem do item perigoso
danger_item_image = pygame.transform.scale(danger_item_image, (60, 60))

# Criando as dimensões
ship_width, ship_height = ship_image.get_size()
star_width, star_height = star_image.get_size()
danger_width, danger_height = danger_item_image.get_size()  # Obtém o tamanho do item perigoso

# Definindo a nave
ship_x = SCREEN_WIDTH // 2 - ship_width // 2
ship_y = SCREEN_HEIGHT - 100
ship_speed = 12

# Variáveis do jogo
stars = []
dangers = []
star_speed = 5
danger_speed = 7
score = 0
missed_stars = 0  # Contador de estrelas perdidas
missed_stars_limit = 3  # Limite de estrelas que podem ser perdidas
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Função para exibir o texto na tela
def display_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

# Função principal do jogo
def game():
    global ship_x, ship_y, score, missed_stars
    running = True
    while running:
        # Desenhar o fundo
        screen.blit(background_image, (0, 0))
        
        # Evento de saída
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Movimentação da nave
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and ship_x > 0:
            ship_x -= ship_speed
        if keys[pygame.K_RIGHT] and ship_x < SCREEN_WIDTH - ship_width:
            ship_x += ship_speed
        if keys[pygame.K_UP] and ship_y > 0:  # Mover para frente
            ship_y -= ship_speed
        if keys[pygame.K_DOWN] and ship_y < SCREEN_HEIGHT - ship_height:  # Mover para trás
            ship_y += ship_speed
        
        # Gerar novas estrelas
        if random.randint(1, 20) == 1:
            star_x = random.randint(0, SCREEN_WIDTH - star_width)
            stars.append([star_x, -star_height])

        # Gerar novos itens perigosos
        if random.randint(1, 50) == 1:  # Chance menor para itens perigosos
            danger_x = random.randint(0, SCREEN_WIDTH - danger_width)
            dangers.append([danger_x, -danger_height])
        
        # Atualizar posição das estrelas
        for star in stars[:]:  # Usando [:] para iterar sobre uma cópia da lista
            star[1] += star_speed
            
            # Colisão com a nave
            if ship_x < star[0] < ship_x + ship_width and ship_y < star[1] < ship_y + ship_height:
                stars.remove(star)
                score += 1
            
            # Remover estrelas que passam da tela
            elif star[1] > SCREEN_HEIGHT:
                stars.remove(star)
                missed_stars += 1  # Incrementa o contador de estrelas perdidas
                if missed_stars >= missed_stars_limit:
                    running = False  # Fim de jogo se o limite for atingido

        # Atualizar posição dos itens perigosos
        for danger in dangers[:]:
            danger[1] += danger_speed

            # Colisão com a nave (game over)
            if ship_x < danger[0] < ship_x + ship_width and ship_y < danger[1] < ship_y + ship_height:
                running = False  # Fim de jogo em caso de colisão
            
            # Remover itens perigosos que passam da tela
            elif danger[1] > SCREEN_HEIGHT:
                dangers.remove(danger)
        
        # Modelagem da nave e das estrelas
        screen.blit(ship_image, (ship_x, ship_y))
        for star in stars:
            screen.blit(star_image, (star[0], star[1]))
        for danger in dangers:
            screen.blit(danger_item_image, (danger[0], danger[1]))

        # Exibir pontuação e estrelas perdidas
        display_text(f"Pontuação: {score}", 10, 10)
        display_text(f"Perdidas: {missed_stars}/{missed_stars_limit}", 10, 50)
        
        # Atualizar a tela
        pygame.display.flip()
        clock.tick(30)

    # Tela de Fim de Jogo
    screen.fill(BLACK)
    display_text("Fim de Jogo", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 30)
    display_text(f"Pontuação Final: {score}", SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 10)
    pygame.display.flip()
    pygame.time.wait(3000)

# Rodar o jogo
game()
pygame.quit()
