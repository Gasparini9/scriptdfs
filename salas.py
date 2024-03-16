import pyautogui
from time import sleep
import numpy as np
import time

xx = 0
yy = 0
skill = 0
sala = 0
#1186, 710
INICIAL = {
    1:[(640,380)],
    2:[(822,425)],
    3:[(681,545)],
    4:[(593,621)],
    5:[(275,334)],
    6:[(501,585)],
    7:[(276,241)],
    8:[(275,565)],
    9:[(182,192)]
}

# PERMITIDAS = {
#     1:[(320,400), (320,450), (320,500), (410,500), (500,500), (590,500), (730,570), (730,520), 
#        (730,470), (360,660), (460,660), (545,660), (450,370), (600,400), (510,400), (550,370), 
#        (550,430), (500,440), (550,470), (500,350)],
#     2:[(640,290), (960,350), (870,360), (500,310), (820,470), (550,470), (420,450), (410,590), (460,360)],
#     3:[(420,400), (370,430), (370,470), (370,520), (370,570), (370,610), (910,430), (910, 470), 
#        (960,500), (960,540), (1000, 570), (1000,610), (1000,650), (910,570), (1000,570), (1100,570), 
#        (1190,570), (960,590), (960,640), (410,360), (600,400), (600,450), (600,500), (600,550), 
#        (600,590), (910,370), (910,340), (1000,430), (500,600), (500,680), (780,680), (780,730)],
#     4:[(270,520), (370,520), (460,520), (550,520), (640,520), (730,470), (820,470), (910,470), (1000,470), (640,610), 
#        (740,610), (830,610), (460,560), (460,610)],
#     5:[(550, 470), (640,430), (640,470), (640,520), (190,570), (270,570), (365,570), (460,570), (550,570), 
#        (460,470), (360,470), (270,470), (500,530)],
#     6:[(320,260), (410,260), (500,260), (590,260), (730,290), (780,310), (690,360), (600,360), 
#        (500,130), (500,360), (410,360), (320,450), (410,450), (500,450), (590,450), (680,450), (780,450)  ],
#     7:[(550,100), (550,150), (730,100), (730,150), (90,430), (180,430), (270,430), (360,430), 
#        (90,340), (180,340), (280,340), (370,340), (370,100), (370,150), (370,200) ],
#     8:[(600,260), (770,310), (640,280), (730,330), (600,350) ],
#     9:[(550,200), (550,240), (550,290), (550,340), (460,380), (370,380), (270,380), (180,380)]
# }

class pg:
    # Obtém a largura e altura da tela
    screen_width, screen_height = pyautogui.size()

    def moveTo(self, destination_x, destionation_y):

        # Define as coordenadas de destino para mover o mouse
        destination_x = self.screen_width // 2
        destination_y = self.screen_height // 2
        # Move o mouse para as coordenadas de destino de maneira suave
        pyautogui.moveTo(destination_x, destination_y, duration=1)



class Salas:

    red   = "\033[1;31m"  
    blue  = "\033[1;34m"
    cian  = "\033[1;36m"
    green = "\033[0;32m"
    R = "\033[0;0m"
    B    = "\033[;1m"
    REVERSE = "\033[;7m"

    def calcular_distancia(self, x1, y1, x2, y2):
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def calcular_ponto_medio(self, alvos):
        if len(alvos) == 0:
            return None, None
    
        total_alvos = len(alvos)
        
        soma_x, soma_y = 0, 0
        for alvo in alvos:
            soma_x += alvo[0]  # Coordenada x do alvo
            soma_y += alvo[1]  # Coordenada y do alvo
        
        x_medio = soma_x / total_alvos
        y_medio = soma_y / total_alvos
        
        return x_medio, y_medio


    def encontrar_casa_mais_proxima_ponto_medio(self, x_medio, y_medio, listinha):
        casa_mais_proxima = None
        menor_distancia = float('inf')
        casas_permitidas = listinha
        if not x_medio == None:
            for casa in casas_permitidas:
                casa_x, casa_y = casa
                distancia = self.calcular_distancia(x_medio, y_medio, casa_x, casa_y)

                if distancia < menor_distancia:
                    menor_distancia = distancia
                    casa_mais_proxima = casa

            return casa_mais_proxima
        else:
            return casa_mais_proxima


    def distancia_e_meio(self, ponto, retangulos):
         # Acesse a lista de retângulos dentro da lista
         #300,160
        meio_x = 50
        meio_y = 50
        retangulo_mais_proximo = []
        pontos_do_meio = []
        limite_distancia = 200
        if len(retangulos) == 1:
            # Extrai os centros dos retângulos
            centros_retangulos = np.array([(r[0] + r[2] / 2, r[1] + r[3] / 2) for r in retangulos])

            # Calcula as distâncias entre o ponto e os centros dos retângulos
            distancias = np.linalg.norm(centros_retangulos - ponto, axis=1)

            # Encontra o índice do retângulo mais próximo
            indice_retangulo_mais_proximo = np.argmin(distancias)

            # Obtém as informações do retângulo mais próximo
            retangulo_mais_proximo = retangulos[indice_retangulo_mais_proximo]
            
            # Calcula o ponto do meio do retângulo mais próximo
            meio_x = int(retangulo_mais_proximo[0] + retangulo_mais_proximo[2] / 2)
            meio_y = int((retangulo_mais_proximo[1] + retangulo_mais_proximo[3] / 2)+30)
            str(meio_x)
            str(meio_y)
        else:
            if len(retangulos) > 1:
                # Extrai os centros dos retângulos
                centros_retangulos = np.array([(r[0] + r[2] / 2, r[1] + r[3] / 2) for r in retangulos])
                # Calcula as distâncias entre o ponto e os centros dos retângulos
                distancias = np.linalg.norm(centros_retangulos - ponto, axis=1)
                # Encontra os índices dos retângulos dentro do limite de distância
                indices_retangulos_proximos = np.where(distancias <= limite_distancia)[0]
                # Obtém as informações dos retângulos dentro do limite
                for indice in indices_retangulos_proximos:
                    retangulo_mais_proximo.append(retangulos[indice])
                    # Calcula o ponto do meio do retângulo mais próximo
                    meio_x = int(retangulos[indice][0] + retangulos[indice][2] / 2)
                    meio_y = int(retangulos[indice][1] + retangulos[indice][3] / 2) + 30
                    pontos_do_meio.append((meio_x, meio_y))
        return retangulo_mais_proximo, pontos_do_meio
    
    def midmob(self, ponto, retangulos):
         # Acesse a lista de retângulos dentro da lista
        meio_x = 50
        meio_y = 50
        retangulo_mais_proximo = []

        if len(retangulos) > 0:
            # Extrai os centros dos retângulos
            centros_retangulos = np.array([(r[0] + r[2] / 2, r[1] + r[3] / 2) for r in retangulos])

            # Calcula as distâncias entre o ponto e os centros dos retângulos
            distancias = np.linalg.norm(centros_retangulos - ponto, axis=1)

            # Encontra o índice do retângulo mais próximo
            indice_retangulo_mais_proximo = np.argmin(distancias)

            # Obtém as informações do retângulo mais próximo
            retangulo_mais_proximo = retangulos[indice_retangulo_mais_proximo]
            
            # Calcula o ponto do meio do retângulo mais próximo
            meio_x = int(retangulo_mais_proximo[0] + retangulo_mais_proximo[2] / 2)
            meio_y = int((retangulo_mais_proximo[1] + retangulo_mais_proximo[3] / 2)+30)
            str(meio_x)
            str(meio_y)
            return retangulo_mais_proximo, (meio_x, meio_y)
        else:
            return retangulo_mais_proximo, (meio_x, meio_y)
    
    def midmob2(self, ponto, retangulos):
         # Acesse a lista de retângulos dentro da lista
        meio_x = 50
        meio_y = 50
        retangulo_mais_proximo = []
        ponto_do_meio = []
        if len(retangulos) > 0:
            # Extrai os centros dos retângulos
            centros_retangulos = np.array([(r[0] + r[2] / 2, r[1] + r[3] / 2) for r in retangulos])

            # Calcula as distâncias entre o ponto e os centros dos retângulos
            distancias = np.linalg.norm(centros_retangulos - ponto, axis=1)

            # Encontra o índice do retângulo mais próximo
            indice_retangulo_mais_proximo = np.argmin(distancias)

            # Obtém as informações do retângulo mais próximo
            retangulo_mais_proximo = retangulos[indice_retangulo_mais_proximo]
            
            # Calcula o ponto do meio do retângulo mais próximo
            meio_x = int(retangulo_mais_proximo[0] + retangulo_mais_proximo[2] / 2)
            meio_y = int((retangulo_mais_proximo[1] + retangulo_mais_proximo[3] / 2)+30)
            ponto_do_meio.append((meio_x, meio_y))
            return retangulo_mais_proximo, ponto_do_meio
        else:
            return retangulo_mais_proximo, ponto_do_meio


    def atack_bomba(self, xx, yy, skill):
        self.xx = xx
        self.yy = yy
        self.skill = skill
        print(f"Atacando {skill} em {xx, yy}")

        pg.moveTo(xx, yy)
        sleep(0.8)
        pyautogui.press(skill)
        sleep(0.5)
        pyautogui.click()
        pg.moveTo(550,50)

    def atack(self, midpoint, skill):
        self.skill = skill
        if not midpoint == None:
            xx = midpoint[0]
            yy = midpoint[1]
            print(f"Atacando {skill} em {midpoint}")
            pg.moveTo(xx,yy)
        else: 
            pg.moveTo(550,50)
        sleep(0.8)
        pyautogui.press(skill)
        sleep(0.5)
        pyautogui.click()
        pg.moveTo(550,50)

    
    def andando(self, xx, yy):
        print(f"Andando para {xx, yy}")
        self.xx = xx
        self.yy = yy
        pg.moveTo(xx, yy)
        sleep(0.6)
        pyautogui.click()
        sleep(0.5)
        pg.moveTo(550,50)
    
    def andando2(self, pos):
        print(f"Andando para {pos}")
        pg.moveTo(pos)
        sleep(0.6)
        pyautogui.click()
        sleep(0.5)
        pg.moveTo(550,50)

    def buff(self, xx, yy, skill):
        print(f"Buffando {skill} em {xx, yy}")
        self.xx = xx
        self.yy = yy
        self.skill = skill
        pg.moveTo(xx, yy)
        sleep(0.3)
        pyautogui.press(skill)
        sleep(0.6)
        pyautogui.click()
        pg.moveTo(550,50)


    def inicio_turno(self, sala):
        tt = INICIAL[sala]
        tt2 = tt[0]
        xx = tt2[0]
        yy = tt2[1]
        print(f"Inicio da sala {sala}, na posição {xx}, {yy}")
        sleep(0.3)
        pg.moveTo(xx,yy)
        sleep(0.5)
        pyautogui.click()
        sleep(0.3)
        pyautogui.click()
        sleep(0.2)
        pyautogui.press('f1')
        sleep(1)
        pg.moveTo(1186, 710)
        sleep(0.5)
        pyautogui.click()
        sleep(0.5)
        pg.moveTo(550,50)

    def acabou_turno(self):
        pyautogui.press('esc')
    
    def passando_turno(self):
        pyautogui.press('f1')
        sleep(0.5)
        #--------------
        print(f'{self.cian}>>PASSANDO O TURNO<<'+ self.R)
        print(f'{self.cian}!!!!Checando próximo turno!!!!'+ self.R)

        


    def turno(self, sala, turno, opc, captura_, fase, rec, quantidade, listinha, playera):
        if sala == 1:
            if turno == 1:
                # começo do turno 1
                if opc == 1:
                    ataque = (870, 590)
                    ataque2 = (275, 520)
                if opc == 2:
                    ataque = (275, 520)
                    ataque2 = (870, 590)
            #_______________________________________
                if fase == 1:
                    print(f"Sala {sala} e Turno {turno}")

                    if captura_ == 1:
                        # usando a captura
                        #--------------
                        self.buff(640,380, '4')
                        self.buff(640,380, '4')
                        #--------------
                    else:
                        # usando o buff
                        #--------------
                        self.buff(640,380, '1')
                        #--------------
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(ataque, '2')
                    pg.moveTo(650,50)
                    return             
                    #--------------
                if fase == 2:
                    # usando a bomba
                    #--------------
                    self.atack(ataque, '2')              
                    #--------------

                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------
                if fase == 3 and quantidade[1]> 0 and opc == 1:
                    # usando a bomba
                    #--------------
                    self.atack(ataque2, '2')              
                    #--------------

                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------
                
                if fase == 3 and quantidade[0] > 0 and opc == 2:
                    # usando a bomba
                    #--------------
                    self.atack(ataque2, '2')              
                    #--------------

                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------
                if fase == 3 and quantidade[4] > 0:
                    # usando a bomba
                    #--------------
                    self.atack_bomba(230,220, '2')              
                    #--------------

                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------
                else:
                    # Ataca no centro do mob restante
                    ponto = (640,380)
                    rect_prox, mid_point = self.midmob(ponto, rec)
                    self.atack(mid_point, '6')
                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------

            if turno == 2:
                # começo do turno 1
                if opc == 1:
                    ponto = (220,450)
                if opc == 2:
                    ponto = (460,240)
                if opc == 3:
                    ponto = (600,700)
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")

                if captura_ == 1:
                    # usando o buff
                    #--------------
                    self.buff(640,380, '1')
                    #--------------
                if captura_ == 2:
                    # usando o buff
                    #--------------
                    self.buff(640,380, '4')
                    self.buff(640,380, '4')
                    #--------------
                rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                self.andando(740,430)
                if not casaproxima == None:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    if captura_ == 0:
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()
                    #--------------
                else:
                    # Ataca no centro do mob restante
                    rect_prox, mid_point = self.midmob(ponto, rec)
                    self.atack(mid_point, '6')
                    self.atack(mid_point, '6')
                    if captura_ == 0:
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()
                
                # passando o turno
                #--------------
                self.passando_turno()
                return
                #--------------

            if turno >= 3:
                # começo do turno 1
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")

                ponto = (640,380)
                rect_prox, mid_point = self.midmob(ponto, rec)
                self.atack(mid_point, '6')
                self.atack(mid_point, '6')
                sleep(2)
                self.atack_bomba(1210, 760, '3')
                pyautogui.click()
            
                # passando o turno
                #--------------
                self.passando_turno()
                return
                #--------------
        
        if sala == 2:
            if turno == 1:
                # começo do turno 1
            #_______________________________________
                if opc == 1:
                    ataque = (590, 540)
                    ataque2 = (1000, 240)
                    pos = (820, 520)
                if opc == 2:
                    ataque = (1000, 240)
                    ataque2 = (590, 540)
                    pos = (1000, 430)
                if fase == 1:
                    print(f"Sala {sala} e Turno {turno}")

                    if captura_ == 1:
                        # usando a captura
                        #--------------
                        self.buff(822,425, '4')
                        self.buff(822,425, '4')
                        #--------------
                    else:
                        # usando o buff
                        #--------------
                        self.buff(822,425, '1')
                        #--------------
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(ataque, '2')
                    return        
                    #--------------
                
                if fase == 2:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(ataque, '2')
                    sleep(1)
                    self.andando2(pos)
                    sleep(1)
                    #--------------
                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------
                if fase == 3:

                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(ataque2, '2')
                    sleep(1)
                    self.andando2(pos)
                    sleep(1)
                    #--------------
                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------
                        
            if turno == 2:
                # Calcular os pontos centrais dos retângulos
                pontos_centrais = []
                for pt in playera:
                    x_centro = ((pt[0] + pt[2] // 2)+35)
                    y_centro = ((pt[1] + pt[3] // 2) +35)
                    pontos_centrais.append((x_centro, y_centro))
                print(pontos_centrais)
                xx = pontos_centrais[0][0]
                yy = pontos_centrais[0][1]

                if opc == 1:
                    ponto = (1050, 360)
                elif opc == 2:
                    ponto = (770, 490)
                elif opc == 3:
                    ponto = (640, 240)
                else:
                    ponto = (420, 450)
                
                # começo do turno 1
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")
                if captura_ == 1:
                    # usando o buff
                    #--------------
                    self.buff(xx, yy, '1')
                    #--------------
                if captura_ == 2:
                    # usando o buff
                    #--------------
                    self.buff(xx, yy, '4')
                    self.buff(xx, yy, '4')
                    #--------------

                rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                
                if not casaproxima == None:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    #--------------
                else:
                    # Ataca no centro do mob restante
                    ponto = (680,500)
                    rect_prox, mid_point = self.midmob2(ponto, rec)
                    x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                    casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                
                # passando o turno
                #--------------
                sleep(1)
                self.andando(950, 500)
                sleep(1)
                self.passando_turno()
                return
                #--------------
            if turno >= 3:
                # começo do turno 1
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")
                ponto = (800,450)
                rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                
                if not casaproxima == None:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    sleep(2)
                    self.atack_bomba(1210, 760, '3')
                    pyautogui.click()
                    #--------------
                else:
                    # Ataca no centro do mob restante
                    ponto = (650,430)
                    rect_prox, mid_point = self.midmob2(ponto, rec)
                    x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                    casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    sleep(2)
                    self.atack_bomba(1210, 760, '3')
                    pyautogui.click()
            
                # passando o turno
                #--------------
                self.passando_turno()
                return
                #--------------
        
        if sala == 3:
            if turno == 1:
                if opc == 1:
                    ataque = (1100, 380)
                    ataque2 = (180, 340)
                    pos = (780,640)
                if opc == 2:
                    ataque = (180, 340)
                    ataque2 = (1100, 380)
                    pos = (780,640)
                # começo do turno 1
                
            #_______________________________________
                if fase == 1:
                    print(f"Sala {sala} e Turno {turno}")

                    if captura_ == 1:
                        # usando a captura
                        #--------------
                        self.buff(681,545, '4')
                        self.buff(681,545, '4')
                        #--------------
                    else:
                        # usando o buff
                        #--------------
                        self.buff(681,545, '1')
                        #--------------
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(ataque, '2')
                    pg.moveTo(550,50)         
                    #--------------
                if fase == 2:
                    # usando a bomba
                    #--------------
                    self.atack(ataque, '2')
                    sleep(2)
                    self.andando2(pos)             
                    #--------------
                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------
                if fase == 3:
                    # usando a bomba
                    #--------------
                    self.atack(ataque2, '2')
                    sleep(3)
                    self.andando2(pos)             
                    #--------------
                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------
            
            if turno == 2:
                # começo do turno 2
                if opc == 1:
                    ataque = (1100, 380)
                    ataque2 = (180, 340)
                    pos = (780,640)
                if opc == 2:
                    ataque = (180, 340)
                    ataque2 = (1100, 380)
                    pos = (780,640)
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")

                if captura_ == 1:
                    # usando o buff
                    #--------------
                    x = pos[0]
                    y = pos[1]
                    self.buff(x, y, '1')
                    #--------------
                if captura_ == 2:
                    # usando o buff
                    #--------------
                    x = pos[0]
                    y = pos[1]
                    self.buff(x, y, '4')
                    self.buff(x, y, '4')
                    #--------------
                ponto = pos
                rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)

                if not casaproxima == None:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    if captura_ == 0:
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()
                    #--------------
                else:
                    # Ataca no centro do mob restante
                    ponto = pos
                    rect_prox, mid_point = self.midmob2(ponto, rec)
                    x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                    casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    if captura_ == 0:
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()
            
                # passando o turno
                #--------------
                sleep(1)
                self.andando(680,730)
                sleep(1)
                self.passando_turno()
                return
                #--------------
  
            if turno >= 3:
                # começo do turno 3
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")
                    
                if turno == 3:
                    ponto = (400, 630)
                    sleep(1)
                    self.andando(780,780)
                    sleep(1)
                else: 
                    ponto = (650, 700)
                rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                print(casaproxima)

                if not casaproxima == None:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    sleep(2)
                    self.atack_bomba(1210, 760, '3')
                    pyautogui.click()
                    #--------------
                else:
                    # Ataca no centro do mob restante
                    ponto = (600,740)
                    rect_prox, mid_point = self.midmob2(ponto, rec)
                    x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                    casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    sleep(2)
                    self.atack_bomba(1210, 760, '3')
                    pyautogui.click()
            
                # passando o turno
                #--------------
                self.passando_turno()
                return
                #-------------- 
        
        if sala == 4:
            if turno == 1:
                # começo do turno 1
                if opc == 1:
                    ataque = (915, 378)
                    ataque2 = (456, 427)
                if opc == 2:
                    ataque = (456, 427)
                    ataque2 = (915, 378)
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")
                if fase == 1:
                    if captura_ == 1:
                        # usando a captura
                        #--------------
                        self.buff(590, 633, '4')
                        self.buff(590, 633, '4')
                        #--------------
                    else:
                        # usando o buff
                        #--------------
                        self.buff(590, 633, '1')
                        #--------------
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(ataque, '2')
                    pg.moveTo(650,50)
                    return            
                    #--------------
                if fase == 2:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(ataque, '2')           
                    #--------------
                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------

                if fase == 3:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(ataque2, '2')             
                    #--------------

                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------

            if turno == 2:
                # começo do turno 2
                if opc == 1:
                    ponto = (450, 480)
                if opc == 2:
                    ponto = (910, 480)
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")
            
                if captura_ == 1:
                    # usando o buff
                    #--------------
                    self.buff(593,641, '1')
                    #--------------
                if captura_ == 2:
                    # usando o buff
                    #--------------
                    self.buff(593,641, '4')
                    self.buff(593,641, '4')

                rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                
                if not casaproxima == None:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    if captura_ == 0:
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()
                    #--------------
                else:
                    # Ataca no centro do mob restante
                    ponto = (593,641)
                    rect_prox, mid_point = self.midmob(ponto, rec)
                    self.atack(mid_point, '6')
                    self.atack(mid_point, '6')
                    if captura_ == 0:
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()
                # passando o turno
                #--------------
                sleep(2)
                self.passando_turno()
                return
                #--------------
           
            if turno >= 3:
                # começo do turno 3
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")

                ponto = (590,633)
                rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)

                if not casaproxima == None:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    sleep(2)
                    self.atack_bomba(1210, 760, '3')
                    pyautogui.click()
                    #--------------
                else:
                    # Ataca no centro do mob restante
                    ponto = (593,641)
                    rect_prox, mid_point = self.midmob(ponto, rec)
                    self.atack(mid_point, '6')
                    self.atack(mid_point, '6')
                    sleep(2)
                    self.atack_bomba(1210, 760, '3')
                    pyautogui.click()

                # passando o turno
                #--------------
                self.passando_turno()
                return
                #--------------
        
        if sala == 5:
            if turno == 1:
                # começo do turno 1
                if opc == 1:
                    ataque = (729, 566)
                    ataque2 = (456, 651)
                if opc == 2:
                    ataque = (456, 651)
                    ataque2 = (729, 566)
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")
                if fase == 1:
                    # andando
                    #--------------
                    self.andando(367, 427)
                    #--------------

                    if captura_ == 1:
                        # usando a captura
                        #--------------
                        self.buff(367, 427, '4')
                        self.buff(367, 427, '4')
                        #--------------
                    else:
                        # usando o buff
                        #--------------
                        self.buff(367, 427, '1')
                        #--------------
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(ataque, '2')
                    pg.moveTo(650,50)
                    return
                    #--------------
                if fase == 2:
                    # usando a bomba
                    #--------------
                    self.atack(ataque, '2')
                    #--------------

                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------
                if fase == 3:
                    # usando a bomba
                    #--------------
                    self.atack(ataque2, '2')
                    #--------------

                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------            
        
            if turno == 2:
                    # começo do turno 2
                if opc == 1:
                    ponto = (410, 570)
                if opc == 2:
                    ponto = (570, 530)
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")
                
                if captura_ == 1:
                    # usando o buff
                    #--------------
                    self.buff(367, 427, '1')
                    #--------------
                if captura_ == 2:
                    # usando o buff
                    #--------------
                    self.buff(367, 427, '4')
                    self.buff(367, 427, '4')
                    #--------------
                rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                
                if not casaproxima == None:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    if captura_ == 0:
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()
                    #--------------
                else:
                    # Ataca no centro do mob restante
                    ponto = (367, 427)
                    rect_prox, mid_point = self.midmob(ponto, rec)
                    self.atack(mid_point, '2')
                    self.atack(mid_point, '2')
                    if captura_ == 0:
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()

                # passando o turno
                #--------------
                self.passando_turno()
                return
                #--------------
            if turno >= 3:
                    # começo do turno 2
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")
                ponto = (510,540)
                rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                
                if not casaproxima == None:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    sleep(2)
                    self.atack_bomba(1210, 760, '3')
                    pyautogui.click()
                    #--------------
                else:
                    # Ataca no centro do mob restante
                    ponto = (367, 427)
                    rect_prox, mid_point = self.midmob(ponto, rec)
                    self.atack(mid_point, '6')
                    self.atack(mid_point, '6')
                    sleep(2)
                    self.atack_bomba(1210, 760, '3')
                    pyautogui.click()

                # passando o turno
                #--------------
                self.passando_turno()
                return
                #--------------
        
        if sala == 6:
            if turno == 1:
                # começo do turno 1
            #_______________________________________
                if fase == 1:
                    print(f"Sala {sala} e Turno {turno}")
                    # andando
                    #--------------
                    self.andando(412, 497)
                    #--------------
                    if captura_ == 1:
                        # usando a captura
                        #--------------
                        self.buff(410, 495, '4')
                        self.buff(410, 495, '4')
                        #--------------
                        # usando o buff
                        #--------------
                        sleep(0.5)
                        self.buff(411, 497, '1')
                        sleep(0.5)
                        #--------------
                    # usando alcance
                    #--------------
                    self.buff(414, 499, '7')
                    self.buff(414, 499, '7')
                    #--------------

                    # movendo para local de ataque                
                    # usando a bomba
                    #--------------
                    self.atack_bomba(550, 200, '2')
                    if captura_ == 2:
                        self.atack_bomba(550, 200, '2')
                    if captura_ == 0:
                        self.atack_bomba(639, 193, '2')

                    #--------------

                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------
            
            if turno == 2:
                # começo do turno 2
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")
                
                if fase == 1:
                    if captura_ == 0:
                        # usando o buff
                        #--------------
                        self.buff(412, 497, '1')
                        #--------------
                    if captura_ == 2:
                        # usando o buff
                        #--------------
                        self.buff(412, 497, '4')
                        self.buff(412, 497, '4')
                        #--------------
                
                    if quantidade[0] > 0:
                        sleep(1)
                        self.andando(320,450)
                        sleep(1)
                    return


                ponto = (600, 250)
                rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)


                if not casaproxima == None:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    if captura_ == 1:
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()
                    #--------------
                else:
                    # Ataca no centro do mob restante
                    ponto = (412, 497)
                    rect_prox, mid_point = self.midmob2(ponto, rec)
                    x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                    casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    if captura_ == 1:
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()

                # passando o turno
                #--------------
                self.passando_turno()
                return
                #--------------
            if turno >= 3:
                # começo do turno 2
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")

                ponto = (550, 350)
                rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)

                if not casaproxima == None:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    sleep(2)
                    self.atack_bomba(1210, 760, '3')
                    pyautogui.click
                    #--------------
                else:
                    # Ataca no centro do mob restante
                    ponto = (412, 497)
                    rect_prox, mid_point = self.midmob2(ponto, rec)
                    x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                    casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    sleep(2)
                    self.atack_bomba(1210, 760, '3')
                    pyautogui.click

                # passando o turno
                #--------------
                self.passando_turno()
                return
                #--------------

        if sala == 7:
            if turno == 1:
                # começo do turno 1
                if opc == 1:
                    ataque = (680, 130)
                    ataque2 = (183, 521)
                if opc == 2:
                    ataque = (183, 521)
                    ataque2 = (640, 150)
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")
                if fase == 1:
                    # andando
                    #--------------
                    if captura_ == 1:
                        # usando a captura
                        #--------------
                        self.buff(276, 241, '4')
                        self.buff(276, 241, '4')
                        #--------------
                    else:
                        # usando o buff
                        #--------------
                        self.buff(276, 241, '1')
                        #--------------
                    # andando
                    #--------------
                    if opc == 2:
                        self.andando(182, 333)
                    #--------------
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(ataque, '2')
                    pg.moveTo(650,50)
                    return
                    #--------------
                if fase == 2:
                    # usando a bomba
                    #--------------
                    self.atack(ataque, '2')
                    #--------------
                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------
                if fase == 3:
                    # usando a bomba
                    #--------------
                    self.atack(ataque2, '2')
                    #--------------
                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------
                
            if turno == 2:
                # começo do turno 2
                if opc == 1:
                    ataque = (640, 150)
                    ataque2 = (183, 521)
                    ponto = (200,470)
                    pos = (276,241)
                if opc == 2:
                    ataque = (183, 521)
                    ataque2 = (640, 150)
                    ponto = (720,120)
                    pos = (182, 333)
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")
                if fase == 1:
                    x = pos[0]
                    y = pos[1]
                    if captura_ == 1:
                        # usando o buff
                        #--------------
                        self.buff(x, y, '1')
                        #--------------
                    if captura_ == 2:
                        # usando o buff
                        #--------------
                        self.buff(x, y, '4')
                        self.buff(x, y, '4')
                        #--------------
                    if opc == 2:
                        self.andando(360,290)
                    if opc == 1:
                        self.andando(370,330)
                    return
                rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                if not casaproxima == None:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    if captura_ == 0:
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()
                    #--------------
                else:
                    # Ataca no centro do mob restante
                    ponto = (182, 333)
                    rect_prox, mid_point = self.midmob(ponto, rec)
                    self.atack(mid_point, '2')
                    self.atack(mid_point, '2')
                    if captura_ == 0:
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()

                # passando o turno
                #--------------
                self.passando_turno()
                return
                #--------------
   
            if turno >= 3:
                # começo do turno 3
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")
                ponto = (360,290)
                rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)

                if not casaproxima == None:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    sleep(2)
                    self.atack_bomba(1210, 760, '3')
                    pyautogui.click()
                    #--------------
                else:
                    # Ataca no centro do mob restante
                    ponto = (182, 333)
                    rect_prox, mid_point = self.midmob(ponto, rec)
                    self.atack(mid_point, '6')
                    self.atack(mid_point, '6')
                    sleep(2)
                    self.atack_bomba(1210, 760, '3')
                    pyautogui.click()

                # passando o turno
                #--------------
                self.passando_turno()
                return
                #--------------

        if sala == 8:
            if turno == 1:
                # começo do turno 1
            #_______________________________________
                if fase == 1:
                    print(f"Sala {sala} e Turno {turno}")
                    # andando
                    #--------------
                    self.andando(456, 473)
                    #--------------
                    if captura_ == 1:
                        # usando a captura
                        #--------------
                        self.buff(452, 475, '4')
                        self.buff(452, 475, '4')
                        #--------------
                    else:
                        # usando o buff
                        #--------------
                        self.buff(452, 475, '1')
                        #--------------
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack_bomba(917, 243, '2')
                    self.atack_bomba(917, 243, '2')

                    #--------------

                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------

            if turno == 2:
                # começo do turno 2
            #_______________________________________
                if fase == 1:
                    print(f"Sala {sala} e Turno {turno}")
                    
                    if captura_ == 1:
                        # usando o buff
                        #--------------
                        self.buff(456, 473, '1')
                        #--------------
                    if captura_ == 2:
                        # usando o buff
                        #--------------
                        self.buff(456, 473, '4')
                        self.buff(456, 473, '4')
                        #--------------
                    if quantidade[0] > 0:
                        sleep(1)
                        self.andando(450,380)
                        sleep(1)
                    return
                ponto = (700,200)
                rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)

                
                if not casaproxima == None:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    if captura_ == 0:
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()
                    #--------------
                elif len(rec) > 0:
                    # Ataca no centro do mob restante
                    ponto = (410, 450)
                    rect_prox, mid_point = self.midmob2(ponto, rec)
                    x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                    casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    if captura_ == 0:
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()
                
                else:
                    # Ataca no centro do mob restante
                    self.atack_bomba(600, 260, '2')
                    self.atack_bomba(600, 260, '2')
                    if captura_ == 0:
                        self.atack_bomba(1210, 760, '3')
                
                # passando o turno
                #--------------
                self.passando_turno()
                return
                #--------------
            if turno >= 3:
                # começo do turno 2
            #_______________________________________
                print(f"Sala {sala} e Turno {turno}")
                ponto = (410, 450)
                rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)

                if not casaproxima == None:
                    # movendo para local de ataque
                    # usando a bomba
                    #--------------
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    sleep(2)
                    self.atack_bomba(1210, 760, '3')
                    pyautogui.click()
                    #--------------
                else:
                    # Ataca no centro do mob restante
                    ponto = (410, 450)
                    rect_prox, mid_point = self.midmob2(ponto, rec)
                    x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                    casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                    self.atack(casaproxima, '2')
                    self.atack(casaproxima, '2')
                    sleep(2)
                    self.atack_bomba(1210, 760, '3')
                    pyautogui.click()

                # passando o turno
                #--------------
                self.passando_turno()
                return
                #--------------
            
        if sala == 9:
            if captura_ == 1 or captura_ == 2:
                if turno == 1:
                    # começo do turno 1
                    if opc == 1:
                        ataque = (730, 243)
                        ataque2 = (180, 510)
                        pos = (365,200)
                    if opc == 2:
                        ataque = (180, 510)
                        ataque2 = (730, 243)
                        pos = (190, 290)
                #_______________________________________
                    if fase == 1:
                        print(f"Sala {sala} e Turno {turno}")
                        # andando
                        #--------------
                        self.andando2(pos)
                        #--------------
                        if captura_ == 1:
                            # usando a captura
                            #--------------
                            xxx = pos[0]
                            yyy = pos[1]
                            self.buff(xxx, yyy, '4')
                            self.buff(xxx, yyy, '4')
                            #--------------
                        else: 
                            #--------------
                            xxx = pos[0]
                            yyy = pos[1]
                            self.buff(xxx, yyy, '1')
                            #--------------
                        # movendo para local de ataque
                        # usando a bomba
                        #--------------
                        self.atack(ataque, '2')
                        pg.moveTo(650,50)
                        return
                        #--------------
                        
                    if fase == 2:
                        # usando a bomba
                        #--------------
                        self.atack(ataque, '2')
                        #--------------
                        # passando o turno
                        #--------------
                        self.passando_turno()
                        return
                        #--------------
                    if fase == 3:
                        # usando a bomba
                        #--------------
                        self.atack(ataque2, '2')
                        #--------------
                        # passando o turno
                        #--------------
                        self.passando_turno()
                        return
                        #--------------
              
                if turno == 2:
                         # começo do turno 1
                    if opc == 1:
                        ataque = (730, 243)
                        ataque2 = (180, 510)
                        pos = (365,200)
                        ponto = (230,450)
                    if opc == 2:
                        ataque = (180, 510)
                        ataque2 = (730, 243)
                        pos = (190, 290)
                        ponto = (550,200)
                #_______________________________________
                    print(f"Sala {sala} e Turno {turno}")

                    if captura_ == 1:
                        # usando o buff
                        #--------------
                        xxx = pos[0]
                        yyy = pos[1]
                        self.buff(xxx, yyy, '1')
                        #--------------
                    if captura_ == 2:
                        # usando o buff
                        #--------------
                        xxx = pos[0]
                        yyy = pos[1]
                        self.buff(xxx, yyy, '4')
                        self.buff(xxx, yyy, '4')
                        #--------------
                    rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                    x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                    casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                    if not casaproxima == None:
                        # movendo para local de ataque
                        # usando a bomba
                        #--------------
                        self.atack(casaproxima, '2')
                        self.atack(casaproxima, '2')
                        if captura_ == 0:
                            sleep(2)
                            self.atack_bomba(1210, 760, '3')
                            pyautogui.click()
                        #--------------
                    else:
                        # Ataca no centro do mob restante
                        ponto = (365, 200)
                        rect_prox, mid_point = self.midmob2(ponto, rec)
                        x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                        casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                        self.atack(casaproxima, '2')
                        self.atack(casaproxima, '2')
                        if captura_ == 0:
                            sleep(2)
                            self.atack_bomba(1210, 760, '3')
                            pyautogui.click()

                    # passando o turno
                    #--------------
                    self.passando_turno()
                    return
                    #--------------
               
                if turno >= 3:
                         # começo do turno 1
                #_______________________________________
                    print(f"Sala {sala} e Turno {turno}")
                    
                    ponto = (365, 200)
                    rect_prox, mid_point = self.distancia_e_meio(ponto, rec)
                    x_medio, y_medio = self.calcular_ponto_medio(mid_point)
                    casaproxima = self.encontrar_casa_mais_proxima_ponto_medio(x_medio, y_medio, listinha)
                    
                    if not casaproxima == None:
                        # movendo para local de ataque
                        # usando a bomba
                        #--------------
                        self.atack(casaproxima, '2')
                        self.atack(casaproxima, '2')
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()
                        #--------------
                    else:
                        # Ataca no centro do mob restante
                        ponto = (365, 200)
                        rect_prox, mid_point = self.midmob(ponto, rec)
                        self.atack(mid_point, '6')
                        self.atack(mid_point, '6')
                        sleep(2)
                        self.atack_bomba(1210, 760, '3')
                        pyautogui.click()

                    # passando o turno
                    #--------------
                    self.passando_turno()
                    #--------------
            else:
                pg.moveTo(720, 960)
                sleep(1)
                pyautogui.click()
                sleep(1)
                pg.moveTo(520,490)
                sleep(1)
                pyautogui.click()
                return