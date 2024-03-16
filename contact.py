import cv2 as cv
import numpy as np
from time import sleep, time
from threading import Thread, Lock
from salas import Salas
import pyautogui as pg

class BotState:
    INITIALIZING = 0
    SEARCHING = 1
    MOVING = 2
    MINING = 3
    BACKTRACKING = 4

class AlbionBot:

    partida = Salas()

    # constants
    INITIALIZING_SECONDS = 1
    MINING_SECONDS = 14
    MOVEMENT_STOPPED_THRESHOLD = 0.975
    IGNORE_RADIUS = 130
    TOOLTIP_MATCH_THRESHOLD = 0.72
    THRESHOLD = 0.9
    # threading properties
    stopped = True
    lock = None
    # properties
    state = None 
    screenshot = None
    timestamp = None
    movement_screenshot = None
    targets = []
    window_offset = (0,0)
    window_w = 0
    window_h = 0
    loopsala = 0
    sala = 0
    xx = 0
    yy = 0
    skill = 0
    pronto = None
    comeco = None
    saida = None
    saida2 = None 
    inicio = None
    inicio2 = None
    murango = None
    menta = None
    mobs = None
    click_history = []
    red   = "\033[1;31m"  
    blue  = "\033[1;34m"
    cian  = "\033[1;36m"
    green = "\033[0;32m"
    R = "\033[0;0m"
    B    = "\033[;1m"
    REVERSE = "\033[;7m"

    SALA_REGIONS = {
        1:[(730, 485, 280, 149), (80, 380, 383, 207), (360, 690, 151, 77), (180, 150, 106, 63)],
        2:[(540, 490, 191, 101), (990, 150, 106, 124), (85, 390, 103, 110), (400, 80, 190, 112)],
        3:[(1050, 320, 190, 64), (90, 250, 193, 64), (90, 510, 150, 82), (1090, 600, 151, 79)],
        4:[(770, 260, 246, 123), (300, 320, 254, 112)],
        5:[(660, 470, 240, 150), (300, 590, 300, 121)],
        6:[(360, 60, 464, 119), (730, 60, 95, 71)],
        7:[(670, 40, 160, 115), (30, 460, 300, 107)],
        8:[(730, 70, 380, 242), (730, 70, 110, 50)],
        9:[(690, 130, 202, 118), (40, 420, 300, 110)]
        
    }

    def __init__(self, window_offset, window_size):
        # create a thread lock object
        self.lock = Lock()
    
        # for translating window positions into screen positions, it's easier to just
        # get the offsets and window size from WindowCapture rather than passing in 
        # the whole object
        self.window_offset = window_offset
        self.window_w = window_size[0]
        self.window_h = window_size[1]
        # pre-load the needle image used to confirm our object detection
        self.pronto = cv.imread('pronto.jpg', cv.IMREAD_UNCHANGED)
        self.saida2 = cv.imread('result.jpg', cv.IMREAD_UNCHANGED)
        self.inicio2 = cv.imread('ponteiro4.jpg', cv.IMREAD_UNCHANGED)
        self.mobs = cv.imread('mobs2.jpg', cv.IMREAD_UNCHANGED)
        self.murango = cv.imread('murango.jpg', cv.IMREAD_UNCHANGED)
        self.menta = cv.imread('menta.jpg', cv.IMREAD_UNCHANGED)
        self.lima = cv.imread('limao.jpg', cv.IMREAD_UNCHANGED)
        self.player = cv.imread('player.jpg', cv.IMREAD_UNCHANGED)
        # start bot in the initializing mode to allow us time to get setup.
        # mark the time at which this started so we know when to complete it
        self.state = BotState.INITIALIZING
        self.timestamp = time()
    
    def desenhar_grade_losangos(self, imagem, deslocamento_x, deslocamento_y, tamanho_quadrante_x, tamanho_quadrante_y):
        altura, largura, _ = imagem.shape

        for i in range(0, altura, int(tamanho_quadrante_y)):
            for j in range(0, largura, int(tamanho_quadrante_x)):
                if i % (2 * int(tamanho_quadrante_y)) == 0:  # Linhas pares
                    cv.line(imagem, (int(j + deslocamento_x), int(i + deslocamento_y)),
                            (int(j + deslocamento_x + tamanho_quadrante_x / 2), int(i + deslocamento_y + tamanho_quadrante_y)), (0, 0, 0), 1)
                    cv.line(imagem, (int(j + deslocamento_x + tamanho_quadrante_x / 2), int(i + deslocamento_y + tamanho_quadrante_y)),
                            (int(j + deslocamento_x + tamanho_quadrante_x), int(i + deslocamento_y)), (0, 0, 0), 1)
                    # Adiciona ponto de partida
                    cv.circle(imagem, (int(j + deslocamento_x + tamanho_quadrante_x / 4), int(i + deslocamento_y + tamanho_quadrante_y / 2)), 3, (255, 0, 0), -1)
                else:  # Linhas ímpares
                    cv.line(imagem, (int(j + deslocamento_x + tamanho_quadrante_x / 2), int(i + deslocamento_y)),
                            (int(j + deslocamento_x), int(i + deslocamento_y + tamanho_quadrante_y)), (0, 0, 0), 1)
                    cv.line(imagem, (int(j + deslocamento_x + tamanho_quadrante_x / 2), int(i + deslocamento_y)),
                            (int(j + deslocamento_x + tamanho_quadrante_x), int(i + deslocamento_y + tamanho_quadrante_y)), (0, 0, 0), 1)
                    # Adiciona ponto de partida
                    cv.circle(imagem, (int(j + deslocamento_x + (3 * tamanho_quadrante_x) / 4), int(i + deslocamento_y + tamanho_quadrante_y / 2)), 3, (255, 0, 0), -1)
    # Função para verificar se a cor está presente em uma região
    def verificar_cor_na_regiao(self, imagem, centro_x, centro_y, cor1, cor2, raio_regiao):
        # Extrai a região ao redor do centro
        regiao = imagem[max(0, centro_y - raio_regiao):min(imagem.shape[0], centro_y + raio_regiao),
                    max(0, centro_x - raio_regiao):min(imagem.shape[1], centro_x + raio_regiao)]

        # Verifica se a região não está vazia
        if regiao.size == 0:
            return False

        # Converte a região para o espaço de cores RGB
        regiao_rgb = cv.cvtColor(regiao, cv.COLOR_BGR2RGB)

        # Verifica se alguma parte da região corresponde a uma das cores
        mask1 = np.all(np.abs(regiao_rgb - cor1) <= 10, axis=2)
        mask2 = np.all(np.abs(regiao_rgb - cor2) <= 10, axis=2)

        return np.any(mask1) or np.any(mask2)
    
    def listinha(self):
        # Carrega a imagem
        imagem_rgb = self.screenshot

        # Deslocamento em x e y
        deslocamento_x = 47.0  # Deslocamento em pixels na direção x
        deslocamento_y = 75.0  # Deslocamento em pixels na direção y

        # Tamanho do quadrante em X e Y
        tamanho_quadrante_x = 91.5
        tamanho_quadrante_y = 23.8

        # Raio da região ao redor do centro para verificar a cor
        raio_regiao = 5

        # Chama a função para desenhar a grade de losangos
        self.desenhar_grade_losangos(imagem_rgb, deslocamento_x, deslocamento_y, tamanho_quadrante_x, tamanho_quadrante_y)

        listinha = []
        # Analisa cada losango
        for i in range(0, imagem_rgb.shape[0], int(tamanho_quadrante_y)):
            for j in range(0, imagem_rgb.shape[1], int(tamanho_quadrante_x)):
                if i % (2 * int(tamanho_quadrante_y)) == 0:  # Linhas pares
                    ponto_central = (int(j + deslocamento_x + tamanho_quadrante_x/ 4), int(i + deslocamento_y + tamanho_quadrante_y / 1))
                else:  # Linhas ímpares
                    ponto_central = (int(j + deslocamento_x + (3 * (tamanho_quadrante_x)) / 4), int(i + deslocamento_y + tamanho_quadrante_y / 1))

                # Verifica a cor na região central do losango
                if self.verificar_cor_na_regiao(imagem_rgb, ponto_central[0], ponto_central[1], (46, 108, 167), (60, 115, 170), raio_regiao):
                    # Marca o ponto central em vermelho
                    cv.circle(imagem_rgb, ponto_central, 3, (0, 0, 255), -1)
                    ponto_central = (ponto_central[0], ponto_central[1]+30)
                    listinha.append(ponto_central)
        # output_path = 'output_image.jpg'
        # cv.imwrite(output_path, imagem_rgb)
        return listinha

    def confirm_pronto(self, comeco):
        # check the current screenshot for the limestone tooltip using match template
        result = cv.matchTemplate(self.screenshot, self.pronto, cv.TM_CCOEFF_NORMED)
        # get the best match postition
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        # if we can closely match the tooltip image, consider the object found
        if max_val >= self.TOOLTIP_MATCH_THRESHOLD:
            self.comeco = True
            return comeco
        # print('Tooltip not found.')
        return False
    
    def confirm_saida(self, saida):
        # check the current screenshot for the limestone tooltip using match template
        result = cv.matchTemplate(self.screenshot, self.saida2, cv.TM_CCOEFF_NORMED)
        # get the best match postition
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        # if we can closely match the tooltip image, consider the object found
        if max_val >= self.TOOLTIP_MATCH_THRESHOLD:
            self.saida = True
            return saida
        # print('Tooltip not found.')
        return False
    
    def confirm_inicio(self, inicio):
        # check the current screenshot for the limestone tooltip using match template
        result = cv.matchTemplate(self.screenshot, self.inicio2, cv.TM_CCOEFF_NORMED)
        # get the best match postition
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        # if we can closely match the tooltip image, consider the object found
        if max_val >= self.THRESHOLD:
            self.inicio = True
            return inicio
        # print('Tooltip not found.')
        return False
    
    def regiao(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.w = self.mobs.shape[1]
        self.h = self.mobs.shape[0]

        # Corte a região específica da imagem
        self.regiao_especifica = self.screenshot[y:y+altura, x:x+largura]
        result = cv.matchTemplate(self.regiao_especifica, self.mobs, cv.TM_SQDIFF_NORMED)

        limiar = 0.127
        locs = np.where(result <= limiar)

        rectangles = []
        for loc in zip(*locs[::-1]):
            rect = [loc[0], loc[1], self.w, self.h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        rectangles, weights= cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        quantidade_deteccoes = len(rectangles)
        # print(f'Nessa região tem {quantidade_deteccoes} mob(s)')
        return quantidade_deteccoes, rectangles
    
    
    def morango(self, x, y, largura, altura, iimagem, limia):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.w = self.mobs.shape[1]
        self.h = self.mobs.shape[0]

        # Corte a região específica da imagem
        self.regiao_especifica = self.screenshot[y:y+altura, x:x+largura]
        result = cv.matchTemplate(self.regiao_especifica, iimagem, cv.TM_SQDIFF_NORMED)

        limiar = limia
        locs = np.where(result <= limiar)

        rectangles = []
        for loc in zip(*locs[::-1]):
            rect = [loc[0], loc[1], self.w, self.h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        rectangles, weights= cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        quantidade_deteccoes = len(rectangles)
        # print(f'Nessa região tem {quantidade_deteccoes} mob(s)')
        return quantidade_deteccoes
    
    def player11(self, x, y, largura, altura, iimagem, limia):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.w = self.mobs.shape[1]
        self.h = self.mobs.shape[0]

        # Corte a região específica da imagem
        self.regiao_especifica = self.screenshot[y:y+altura, x:x+largura]
        result = cv.matchTemplate(self.regiao_especifica, iimagem, cv.TM_SQDIFF_NORMED)

        limiar = limia
        locs = np.where(result <= limiar)

        rectangles = []
        for loc in zip(*locs[::-1]):
            rect = [loc[0], loc[1], self.w, self.h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        rectangles, weights= cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        quantidade_deteccoes = len(rectangles)
        # print(f'Nessa região tem {quantidade_deteccoes} mob(s)')
        return rectangles
    
    def jogando(self, sala):
        turno = 1
        self.inicio = False
        print(f'{self.blue}>>>>>>>> Entrando na BATALHA DA SALA {sala}' + self.R)
        # Define se vai capturar ou não
        captura = []
        captura2 = []
        limao = []
        sleep(0.5)
        self.partida.inicio_turno(sala)
        self.loopsala = 0
        quantidade = []
        rect = []
        listinha = []
        playera = []

        while(self.loopsala == 0) and not self.stopped:
            sleep(0.5)

            if not self.saida:
                # Confirma o ínicio do turno
                self.confirm_inicio(self.inicio)
                if self.inicio and turno == 1:
                    print(f'{self.blue}>>>>>>>>>>>>> Turno iniciou, detectando mobs. <<<<<<<<<<<<<' + self.R)
                    sleep(0.5)
                    # Analisa as regiões de acordo com o número da sala
                    for regiao in self.SALA_REGIONS[sala]:
                        quantidades, qq = self.regiao(*regiao)
                        quantidade.append(quantidades)
                    print(f'Foram detectados {quantidade} mobs na posição 1 e 2, respectivamente!!!')

                    if len(quantidade) < 3 or len(quantidade) < 2:
                        quantidade.extend([0, 0, 0])

                    captura.append(self.morango(650, 680, 633, 145, self.murango, 0.04))
                    captura2.append(self.morango(650, 680, 633, 145, self.menta, 0.03))
                    limao.append(self.morango(650, 680, 633, 145, self.lima, 0.02))
            
                    if captura[0] >= 1 or captura2[0] > 2:
                        print(self.red + f'Morangos: {captura}' + self.R + self.green + f' Mentas: {captura2}' + self.R)
                        if quantidade[0] == 0 or quantidade[1] == 0:
                            captura_ = 1
                            print(f'{self.green}>>>>>>>>>>>>> CAPTURA ATIVA!! <<<<<<<<<<<<<' + self.R)
                        else:
                            if limao[0] > 0:
                                captura_ = 2
                                print(f'{self.green}>>>>>>>>>>>>> CAPTURA ATIVA NO TURNO 2!! <<<<<<<<<<<<<' + self.R)
                            else:
                                captura_ = 1
                                print(f'{self.green}>>>>>>>>>>>>> CAPTURA ATIVA!! <<<<<<<<<<<<<' + self.R)
                    else:
                        captura_ = 0
                        print(f'{self.red}>>>>>>>>>>>>> SEM CAPTURA!! <<<<<<<<<<<<<' + self.R)
                                

                    # Compara as regiões e identifica qual tem mais mobs
                    if len(quantidade) > 0:
                        if quantidade[0] >= quantidade[1]:
                            # detecta todos os mobs do mapa e envia pra função midpoint
                            qq, rect = self.regiao(0, 0, 1280, 1025)
                            rec = [[x, y, largura, altura] for x, y, largura, altura in rect]
                            print('>>>>>>>>>>>>> Atacando na posição 1 <<<<<<<<<<<<<')
                            opc = 1
                            fase = 1

                            # script de cada sala
                            self.partida.turno(sala, turno, opc, captura_, fase, rec, quantidade, listinha, playera)
                            # checa se os mobs morreram após o primeiro ataque
                            x, y, largura, altura = self.SALA_REGIONS[sala][0]
                            if sala != 6 and sala != 8:
                                if quantidade[0] == 2:
                                    print('Esperando 4 segundos')
                                    sleep(4)
                                    
                                elif quantidade[0] == 3:
                                    print('Esperando 5 segundos')
                                    sleep(5)
                                    
                                elif quantidade[0] == 4:
                                    print('Esperando 6 segundos')
                                    sleep(6)
                                elif quantidade[0] == 5:
                                    print('Esperando 7 segundos')
                                    sleep(7)
                                    
                                else:
                                    print('Esperando 3 segundos')
                                    sleep(3)

                            quantidade2, qqq = self.regiao(x, y, largura, altura)
                            if quantidade2 > 0:
                                fase = 2
                                self.partida.turno(sala, turno, opc, captura_, fase, rec, quantidade, listinha, playera)
                            else:
                                fase = 3                          
                                self.partida.turno(sala, turno, opc, captura_, fase, rec, quantidade, listinha, playera)
                            
                            turno = 2
                            self.inicio = False

                        else:
                            qq, rect = self.regiao(0, 0, 1280, 1025)
                            rec = [[x, y, largura, altura] for x, y, largura, altura in rect]
                            print('>>>>>>>>>>>>> Atacando na posição 2 <<<<<<<<<<<<<')
                            opc = 2
                            fase = 1

                            self.partida.turno(sala, turno, opc, captura_, fase, rec, quantidade, listinha, playera)
                            x, y, largura, altura = self.SALA_REGIONS[sala][1]
                            
                            if sala != 6 and sala != 8:
                                if quantidade[1] == 2:
                                    print('Esperando 4 segundos')
                                    sleep(4)
                                    
                                elif quantidade[1] == 3:
                                    print('Esperando 5 segundos')
                                    sleep(5)
                                    
                                elif quantidade[1] == 4:
                                    print('Esperando 6 segundos')
                                    sleep(6)
                                elif quantidade[1] == 5:
                                    print('Esperando 7 segundos')
                                    sleep(7)
                                    
                                else:
                                    print('Esperando 3 segundos')
                                    sleep(3)
                                
                            quantidade2, qqq = self.regiao(x, y, largura, altura)
                            if quantidade2 > 0:
                                fase = 2
                                self.partida.turno(sala, turno, opc, captura_, fase, rec, quantidade, listinha, playera)
                            else:
                                fase = 3
                                self.partida.turno(sala, turno, opc, captura_, fase, rec, quantidade, listinha, playera)
                            
                            turno = 2
                            self.inicio = False

                if self.inicio and turno >= 2:
                    print(f'{self.green}>>>>>>>>>>>>> Turno {turno} iniciou <<<<<<<<<<<<<' + self.R)
                    qq, rect = self.regiao(0, 0, 1280, 1025)
                    rec = [[x, y, largura, altura] for x, y, largura, altura in rect]
                    listinha = []
                    quantidade = []
                    fase = 0
                    
                    # Posição do player
                    playera = self.player11(15, 15, 1260, 1035, self.player, 0.03)
                    
                    # Mentas no turno 2+
                    quantidade.append(self.morango(650, 680, 633, 145, self.menta, 0.03))

                    # Particularidade sala 8 7 e 6 
                    if sala == 8 or sala == 7 or sala == 6 and turno == 2:
                        fase = 1
                        self.partida.turno(sala, turno, opc, captura_, fase, rec, quantidade, listinha, playera)
                        fase = 2
                    

                    # pega a lista de casas disponíveis para atacar
                    sleep(0.5)
                    pg.moveTo(550,50)
                    pg.press('2')
                    sleep(1)
                    listinha = self.listinha()
                    pg.press('esc')

                    # Particularidade sala 1
                    if sala == 1 and turno == 2:
                        sleep(2)
                        qq, reee = self.regiao(270, 300, 380, 240)
                        print(f'Na zona 1 tem {qq} mobs')
                        qq2, ree = self.regiao(300, 170, 179, 155)
                        print(f'Na zona 2 tem {qq} mobs')
                        if qq > 0 or qq2 > 0:
                            if qq >= qq2:
                                opc = 1
                            else:
                                opc = 2
                        else:
                            opc = 3

                    # Particularidade sala 2
                    if sala == 2 and turno == 2:
                        sleep(2)
                        qq, reee = self.regiao(815, 250, 450, 200) # Parte de cima
                        print(f'Na zona 1 tem {qq} mobs')
                        qq2, ree = self.regiao(630, 370, 295, 212) # Parte de baixo
                        print(f'Na zona 2 tem {qq2} mobs')
                        qq3, ree = self.regiao(540, 150, 241, 143) # Parte do meio
                        print(f'Na zona 3 tem {qq3} mobs')
                        if qq > 0 or qq2 > 0 or qq3 > 0:
                            if qq >= qq2 and qq > 0:
                                opc = 1
                            if qq2 >= qq and qq2 > 0:
                                opc = 2
                            else:
                                opc = 3
                    
                    sleep(0.5)
                    self.partida.turno(sala, turno, opc, captura_, fase, rec, quantidade, listinha, playera)
                    turno += 1
                    self.inicio = False   
                          

                self.confirm_saida(self.saida)
            
            if self.saida:
                print(f'{self.red}------------FIM DE PARTIDA--------------' + self.R)
                self.partida.acabou_turno()
                self.loopsala = 1
                return   

    # threading methods

    def update_targets(self, targets):
        self.lock.acquire()
        self.targets = targets
        self.lock.release()

    def update_screenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    # main logic controller
    def run(self):
        while not self.stopped:
            if self.state == BotState.INITIALIZING:
                sleep(0.5)
                print('BOT INICIANDO')
                # do no bot actions until the startup waiting period is complete
                if time() > self.timestamp + self.INITIALIZING_SECONDS:
                    print('----------------------------BOT INICIADO')
                    self.sala = int(input("Digite qual sala você está (de 1 a 8) >>>> :  "))
                    # start searching when the waiting period is over
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()

            elif self.state == BotState.SEARCHING:
                sleep(0.5)
                # check the given click point targets, confirm a limestone deposit,
                # then click it.
                if not self.comeco:
                    if self.sala > 9:
                        print('_____________________________________')
                        print('FIM DA LINHA')
                        print('AGUARDANDO 30 SEGUNDOS PARA RECOMEÇAR A CONTAGEM')
                        sleep(30)
                        self.sala = 1
                    print(self.red + f"Procurando partida na sala {self.sala}" + self.R)
                    self.confirm_pronto(self.comeco)

                # if successful, switch state to moving
                # if not, backtrack or hold the current position
                if self.comeco:
                    print(f'{self.green}------------PARTIDA ENCONTRADA-----------')
                    self.comeco = False
                    self.lock.acquire()
                    self.state = BotState.MOVING
                    self.lock.release()

            elif self.state == BotState.MOVING:
                
                if not self.saida:
                    self.jogando(self.sala)
                    self.sala += 1
                    sleep(1)
                if self.saida:
                    print(self.red + f'------------FIM DE PARTIDA--------------' + self.R)
                    self.saida = False
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()
                