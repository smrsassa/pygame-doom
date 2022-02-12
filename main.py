import pygame, math
from settings import *


class Raycaster:
    def __init__(self) -> None:
        pygame.init()
        self.tela = pygame.display.set_mode(( TELA_LARGURA, TELA_ALTURA ))
        pygame.display.set_caption('Raycaster')
        self.clock = pygame.time.Clock()
        self.tela.fill(pygame.Color(40, 40, 40))
        self.rodando = True

        self.px = self.py = 96
        self.pa = 0
        self.pdx = math.cos(self.pa) * 5
        self.pdy = math.sin(self.pa) * 5

    def drawMap(self) -> None:
        for y in range(0, MAP_Y):
            for x in range(0, MAP_X):
                color = (0,0,0)
                if MAP[y*MAP_X+x] == 1:
                    color = (255,255,255)
                xo=x*MAP_S
                yo=y*MAP_S
                pygame.draw.polygon(self.tela, color, [
                    (xo        +1, yo        +1), 
                    (xo        +1, yo + MAP_S-1), 
                    (xo + MAP_S-1, yo + MAP_S-1), 
                    (xo + MAP_S-1, yo        +1)
                ])

    def drawPlayer(self) -> None:
        pygame.draw.rect(self.tela, (0, 255, 0), ((self.px,self.py), (PLAYERSIZE,PLAYERSIZE)))
        #pygame.draw.line(self.tela, (0, 255, 0), (self.px+PLAYERSIZE/2,self.py+PLAYERSIZE/2), (self.px+self.pdx*5,self.py+self.pdy*5), 2) #visao

    def drawRays2D(self) -> None:
        angle = self.pa + (PI * 1.5 - (PLAYERFOV * (PLAYERFOV/2)))

        for ray in range(QTDRAYS):
            for depth in range(TELA_ALTURA):
                target_x = self.px - math.sin(angle) * depth
                target_y = self.py + math.cos(angle) * depth

                col = int(target_x / MAP_S)
                row = int(target_y / MAP_S)
                
                square = row * MAP_X + col

                if MAP[square] == 1:
                    pygame.draw.line(self.tela, (0, 0, 255), (self.px+PLAYERSIZE/2,self.py+PLAYERSIZE/2), (target_x, target_y))
                                        
                    ca = (self.pa + (PI * 1.5)) - angle
                    if ca < 0:
                        ca += 2*PI
                    if ca > 2*PI:
                        ca -= 2*PI
                    depth *= math.cos(ca)

                    color = 255 / int(2 + depth * depth * 0.0001)

                    wall_height = 21000 / (depth + 0.0001)

                    if wall_height > TELA_ALTURA: wall_height = TELA_ALTURA 

                    pygame.draw.rect(self.tela, (color, color, color), (TELA_ALTURA + ray * ESCALA,(TELA_ALTURA / 2) - wall_height / 2, ESCALA+1, wall_height))
                    break

            angle += PLAYERFOV / 120

    def display(self) -> None:
        self.drawRays2D()
        self.drawPlayer()

    def controles(self) -> None:
        # -=- Teclado -=-
        def movLateral() -> tuple:
            if (self.pdy > 0 and self.pdx < 0):
                return (1, 1)
            if (self.pdy < 0 and self.pdx > 0):
                return (-1, -1)
            if (self.pdy > 0 and self.pdx > 0):
                return (1, -1)
            if (self.pdy < 0 and self.pdx < 0):
                return (-1, 1)

        keys = pygame.key.get_pressed() 

        if keys[pygame.K_ESCAPE]:
            self.rodando = False

        sinal = movLateral()
        if keys[pygame.K_a]:
            self.px += abs(self.pdy) * sinal[0]
            self.py += abs(self.pdx) * sinal[1]
        if keys[pygame.K_d]:
            self.px -= abs(self.pdy) * sinal[0]
            self.py -= abs(self.pdx) * sinal[1]

        if keys[pygame.K_w]:
            self.px += self.pdx
            self.py += self.pdy
        if keys[pygame.K_s]:
            self.px -= self.pdx
            self.py -= self.pdy

        # -=- Mouse -=-
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if mouse_x < TELA_LARGURA/2:
            self.pa -= 0.1
            if self.pa < 0:
                self.pa += 2*PI
            self.pdx = math.cos(self.pa) * 5
            self.pdy = math.sin(self.pa) * 5
        if mouse_x > TELA_LARGURA/2:
            self.pa += 0.1
            if self.pa < (2 * PI):
                self.pa -= 2*PI
            self.pdx = math.cos(self.pa) * 5
            self.pdy = math.sin(self.pa) * 5

        pygame.mouse.set_pos((TELA_LARGURA/2,TELA_ALTURA/2))

    def run(self) -> None:
        pygame.mouse.set_visible(False)

        while self.rodando:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.rodando = False

            self.tela.fill(pygame.Color(40, 40, 40))

            pygame.draw.rect(self.tela, (90, 90, 90), (512, TELA_ALTURA / 2, TELA_ALTURA, TELA_ALTURA))
            pygame.draw.rect(self.tela, (222, 222, 222), (512, - TELA_ALTURA / 2, TELA_ALTURA, TELA_ALTURA))

            self.controles()

            self.drawMap()

            self.display()

            self.clock.tick(MAX_FPS)
            pygame.display.update()

if __name__ == '__main__':
    RayCaster  = Raycaster()
    RayCaster.run()
