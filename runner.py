import pygame
from sys import exit
from random import randint, choice

# Ele esta herdando uma classe do pygame 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Variavel que o personagem anda
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        # Criando a variavel da classe que e uma lista que anda e tem 2 animacoes
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        
        # Personagem agachado
        self.player_crawled = pygame.image.load('graphics/player/player_head.png').convert_alpha()
        self.player_crawled_act = False
        
        # A imagem do player é a lista do player de andar na posicao do index
        self.image = self.player_walk[self.player_index]
        # Criando um retangulo com base na variavel da imagem
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
        
    def player_input(self):
        # Recebe a tecla que foi pressionada
        keys = pygame.key.get_pressed()
        # Se a tecla é espaco e o retangulo do personagem estive me uma margem
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            # faz a gravidade valer - 20 entao ele vai subir
            self.gravity = -20
            # Toca o som 
            self.jump_sound.play()
        if keys[pygame.K_s]:
            self.player_crawled_act = True
        if keys[pygame.K_w]:
            self.player_crawled_act = False
            
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            # arruma o personagem caso ele fique de baixo da terra
            self.rect.bottom = 300
        
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        elif self.player_crawled_act:
            self.image = self.player_crawled
            self.rect.bottom = 330       
        else:
            self.player_index += 0.1
            # se ele for 2 ou maior que 2
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            # A imagem é a posicao da lista dos sprints em int
            self.image = self.player_walk[int(self.player_index)]
            
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        
    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 240
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
        
        
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()   
    
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
                


def display_score():
    # Aqui ele pega o tempo corrente que vira a pontuacao 
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    # Criando a superficie da pontuacao 
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    # Criando um retangulo dessa pontuacao
    score_rect = score_surf.get_rect(center = (400,50))
    # Coloca na tela a o texto e o retangulo
    screen.blit(score_surf, score_rect)
    # Retornar o tmepo corrente a pontuacao
    return current_time

# Aqui acredito que ele esteja chegando se tem algum colisor na tela
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True
    

#### Iniciando o pygame
pygame.init()
# Criando a tela 
screen = pygame.display.set_mode((800,400))
# O nome do jogo
pygame.display.set_caption('Runner')
# Criando relogio do pygame
clock = pygame.time.Clock()
# Pegando a font baixada do arquivo
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)


####Groups
# Pelo o que eu entendi ele cria uma classe do pygame
player = pygame.sprite.GroupSingle()
# E aqui add a classe Player que eu fiz a ela
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()


#### Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
# Aqui aparentemente ele esta dando um zoom na imagem
player_stand = pygame.transform.rotozoom(player_stand,0,2)
# Criando o retangulo com base na imagem e centralizando
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Runner', False, (110,190,170))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = test_font.render('Press space to run', False, (110,200,170))
game_message_rect = game_message.get_rect(center = (400, 330))

### Timer
# Nao entendi tao bem esta parte
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)


while True:
    for event in pygame.event.get():
        # Aqui ele verifica se é para fechar o jogo
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if game_active:
            if event.type == obstacle_timer:
                # Aqui ele adiciona um obstaculo, o inimigo, e escolhe aleatoriamente, mas tem maior chance de vir uma cobra
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
                
        else:
            # se presionou a tecla ea tecla é espaco
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
            
    # se o jogo começou
    if game_active:
        # Colocar a imagem na tela
        screen.blit(sky_surface, (0,0))
        # Colocar o chao na tela
        screen.blit(ground_surface,(0,300))
        # Essa funcao pega o tempo, colocar como pontuacao, desenha e coloca na tela e retorna a pontuacao
        score = display_score()
        
        # Desenha o jogador na tela e depois fica atualizando
        player.draw(screen)
        player.update()
        
        # Desenha o inimigo e atualiza 
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        # se colidiu Recebe falso
        game_active = collision_sprite()
        
    
    else:
        screen.fill((94,129,160))
        screen.blit(player_stand, player_stand_rect)
        
        score_message = test_font.render(f'Your score: {score}',False,(110,200,170))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name, game_name_rect)
        
        # Aqui ele faz a logica de a pontuacao for 0, imprimi a tela inicial se nao o socre
        if score == 0: 
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)
        

    # Coisa basica do pygame
    pygame.display.update()
    clock.tick(60)



