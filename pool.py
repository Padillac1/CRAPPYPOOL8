#The png files where created by a friend and university classmate.
#

import pygame
import cmath
import sys
from math import *

screen_width = 1600
screen_height = 900
table_width = 1400
table_height = 700
border_y = 45
border_x = 60
blanca_inicio = (200,200)

#Clases
class Bola(pygame.sprite.Sprite):
    def __init__(self,imdir, position, coeffriccion = 0.03):
        super().__init__()
        self.image = pygame.image.load(imdir).convert_alpha()
        self.rect = self.image.get_rect(center = position)
        self.coef = coeffriccion
        self.vel = 0
        self.dir = 0

    def mover(self): #1284,600
        if self.rect.left <= 0:
            self.rect.left = 0
            self.dir = -self.dir  - pi
        if self.rect.right >= 1284:
            self.rect.right = 1284
            self.dir = -self.dir  - pi
        if self.rect.top <= 0:
            self.rect.top = 0
            self.dir *= -1
        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.dir *= -1
        if self.vel  <=0: 
            self.vel = 0
        else:           
            a = self.rect.center
            self.rect.centerx =int(self.rect.centerx + self.vel*cos(self.dir))
            self.rect.centery = int(self.rect.centery + self.vel*sin(self.dir))
            self.vel = self.vel - self.coef
    
    #Uso complejos para simular la fisica del choque de las bolas, creo que es mas sencillo que el metodo de la matrix de rotacion. 
    #Sorry por accesar a directamente a los atributos de otro xD.  Lo cambiaré luego :v
    def colicionar(self,otro):
        v1 = cmath.rect(self.vel,self.dir) 
        v2 = cmath.rect(otro.vel,otro.dir) 
        theta = atan2(self.rect.center[1] - otro.rect.center[1],self.rect.center[0] - otro.rect.center[0])  
        u1 = v1 * (cmath.rect(1,-theta)) 
        u2 = v2 * (cmath.rect(1,-theta)) 
        z1 = u2.real + u1.imag * 1j
        z2 = u1.real + u2.imag * 1j  
        w1 = z1 * (cmath.rect(1,theta))  
        w2 = z2 * (cmath.rect(1,theta))
        self.vel = cmath.polar(w1)[0]  
        self.dir = cmath.polar(w1)[1]  
        otro.vel = cmath.polar(w2)[0]
        otro.dir = cmath.polar(w2)[1]
        d = 1.1*(2.0 * 24 - sqrt((self.rect.center[1] - otro.rect.center[1]) ** 2 + (self.rect.center[0] - otro.rect.center[0]) ** 2)) / 2.0  
        self.rect.center = (self.rect.center[0] + d * cos(self.dir), self.rect.center[1] + d * sin(self.dir))
        otro.rect.center = (otro.rect.center[0] + d * cos(otro.dir), otro.rect.center[1] + d * sin(otro.dir))

class Saco:
    def __init__(self,x,y,radio = 40):
        self.x = x  # float
        self.y = y  # float
        self.rad = radio  # float
        self.bolas = []  # float

#funciones
def draw1():
    screen.fill((150,150,255))
    area = pygame.Surface((1284,600),pygame.SRCALPHA)
    balls.draw(area)
    screen.blit(table, (100,100))
    screen.blit(area, (164,150))

def draw2(i=0):
    if i==0: color = 'Red'
    else: color = 'Green'
    screen.fill((150,150,255))
    area = pygame.Surface((1284,600),pygame.SRCALPHA)
    balls.draw(area)
    screen.blit(table, ((100,100)))
    screen.blit(area, (164,150))
    x,y = balls.sprites()[0].rect.center
    pygame.draw.line(screen,color, pygame.mouse.get_pos(), (x+164,y+150), 5)

def checkcoliciones(list):
    t = 0
    for i in range(len(list)):
        for j in range(i + 1,len(list)):
            if sqrt((list[i].rect.center[1] - list[j].rect.center[1]) ** 2 + (list[i].rect.center[0] - list[j].rect.center[0]) ** 2) < 24*2:
                list[i].colicionar(list[j])
                t += 1
    if t > 0:
        pygame.mixer.music.load('choque1.mp3')
        pygame.mixer.music.play()
    return t

def golpearblanca():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    bt_x,bt_y = balls.sprites()[0].rect.centerx+164,balls.sprites()[0].rect.centery+150
    balls.sprites()[0].dir = atan2(mouse_y - bt_y,mouse_x - bt_x) + pi
    balls.sprites()[0].vel = 0.03*sqrt((mouse_y - bt_y)**2+(mouse_x - bt_x)**2) 

def bolas_en_saco_8(saco,group):
    L = []
    foundblanca = False
    for i in group.sprites():
        if dist((saco.x,saco.y), i.rect.center) < 24+saco.rad:
            if i is blanca:
                foundblanca = True
            elif i is bola8:
                for j in L:
                    j.remove()
                print("FUNN")
                return 'bola8_en_saco'
            else:
                L.append(i)
                saco.bolas.append(i)
    for j in L:
        j.vel = 0
        j.remove(group)
    if foundblanca:
        return 'blanca_en_saco'
    return str(len(L)) 

def bolas_en_sacos_8(listadesacos, group):
    bes = False
    cont = 0
    for i in listadesacos:
        ce = bolas_en_saco_8(i, group)
        if ce == 'bola8_en_saco':
            print('YEAH')
            return 'bola8_en_saco'
        elif ce == 'blanca_en_saco':
            bes = True
        else: 
            cont += int(ce)
    if bes:
        return 'blanca_en_saco'
    return str(cont)
            
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('BILLAR')
screen = pygame.display.set_mode((screen_width,screen_height))
table = pygame.image.load('IMG/mesa2.png').convert_alpha()

#Creating objects
positions = [(900, 350), (949, 324), (949, 376), (998, 350), (998, 401), (998, 299), (1047, 376), (1047, 324), ( 1047,427), (1047, 273), (1096, 350), (1096, 401), (1096, 299), (1096, 452), (1096, 248)]
balls = pygame.sprite.Group()
blanca = Bola('IMG/blanca.png', (200,200))
balls.add(blanca)
for i in range(1,16):
    balls.add(Bola(f'IMG/{i}.png', positions[i-1]))

s1 = Saco(0,0)
s2 = Saco(642,0)
s3 = Saco(1284,0)
s4 = Saco(0,600)
s5 = Saco(642,600)
s6 = Saco(1284,600)
sacos = [s1,s2,s3,s4,s5,s6]
bola8 = balls.sprites()[8]

winner = 'NONE'
player_turn = 0
game_state = 'moving'
change_player = False
contador = 0
while True: 
    clickeo = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN: clickeo = True

    if game_state == 'moving':
        checkcoliciones(balls.sprites())
        estado = bolas_en_sacos_8(sacos, balls)
        for i in balls.sprites():
            i.mover()
        draw1()
        if estado == 'bola8_en_saco':
            game_state = 'gameover'
            winner = (player_turn+1)%2
            continue
        elif estado == 'blanca_en_saco':
            change_player = True
        else: 
            contador += int(estado)
        if [i.vel <=0 for i in balls.sprites()] == [True]*len(balls.sprites()):
            game_state = 'hitting'
            if contador == 0:
                change_player = True
            if change_player:
                player_turn = (player_turn+1)%2
                change_player = False
                print("CHANGING")
            else:
                contador = 0
    elif game_state == 'hitting':
        draw2(player_turn)
        if clickeo:
            game_state = 'moving'
            golpearblanca()
    elif game_state == 'gameover':
        print(f'the winner is {winner}') #ARREGLAR quien es el ganador :v
        
    pygame.display.flip()
    clock.tick(60)  






