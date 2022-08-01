import pygame, math
from settings import *


pygame.init()
infoObject = pygame.display.Info()
TELA_LARGURA = infoObject.current_w
TELA_ALTURA = infoObject.current_h
ESCALA = TELA_LARGURA / QTDRAYS 

class Raycaster:
    def __init__(self) -> None:
        self.tela = pygame.display.set_mode(( TELA_LARGURA, TELA_ALTURA ), pygame.NOFRAME | pygame.FULLSCREEN)
        pygame.display.set_caption('Raycaster')
        self.clock = pygame.time.Clock()
        self.tela.fill(pygame.Color(40, 40, 40))
        self.rodando = True

        self.px = self.py = 96
        self.pa = 0
        self.pdx = math.cos(self.pa) * 5
        self.pdy = math.sin(self.pa) * 5

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
                    ca = (self.pa + (PI * 1.5)) - angle
                    if ca < 0:
                        ca += 2*PI
                    if ca > 2*PI:
                        ca -= 2*PI
                    depth *= math.cos(ca)

                    color = 255 / int(2 + depth * depth * 0.0001)

                    wall_height = 33000 / (depth + 0.0001)

                    if wall_height > TELA_ALTURA: wall_height = TELA_ALTURA 

                    pygame.draw.rect(self.tela, (color, color, color), (
                        ray * ESCALA,
                        (TELA_ALTURA / 2) - wall_height / 2, 
                        ESCALA + 1, 
                        wall_height
                    ))
                    break

            angle += PLAYERFOV / 120

    def display(self) -> None:
        self.drawRays2D()

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

            pygame.draw.rect(self.tela, (222, 222, 222), (0, 0, TELA_LARGURA, TELA_ALTURA/2))
            pygame.draw.rect(self.tela, (90, 90, 90), (0, TELA_ALTURA / 2, TELA_LARGURA, TELA_ALTURA/2))

            self.controles()

            self.display()

            self.clock.tick(MAX_FPS)
            pygame.display.update()

if __name__ == '__main__':
    RayCaster  = Raycaster()
    RayCaster.run()
