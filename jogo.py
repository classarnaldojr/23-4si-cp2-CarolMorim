import cv2
import mediapipe as mp

# Caroline Santana Amorim 27_08_2023
#RM86007 Checkpoint2

#####################################################################

#Função: Faz as linhas sobre o video 
mp_drawing = mp.solutions.drawing_utils

# Função:Faz as linhas sobre o video - Parte que detecta mãos
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# Função: Gesto da mão
def getHandGesture(limite_de_mao):
    limites = []
    for limite in limite_de_mao.landmark:
        limites.append((limite.x, limite.y, limite.z))

# Função: Calcula a distância entre os dedos e com isso identifica a diferença ente pedra, papel e tesoura
    dedo1 = ((limites[8][0] - limites[12][0])**2 +
             (limites[8][1] - limites[12][1])**2)**0.5
# Função: Calcula a distância entre os dedos - Indicador e polegar
    dedo2 = ((limites[8][0] - limites[4][0])**2 +
             (limites[8][1] - limites[4][1])**2)**0.5

# Função: Puxa o gesto 
    if dedo1 < 0.04 and dedo2 < 0.04:
        return "pedra"
    elif dedo1 > 0.06 and dedo2 > 0.06:
        return "tesoura"
    else:
        return "papel"

# Função: Video 
cap = cv2.VideoCapture('pedra-papel-tesoura.mp4')

# Função: Puxar e configurar as mãos
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

    gestoPlayer1 = None
    gestoPlayer2 = None
    vencedor = None  
    pontuacao = [0, 0]

    while True:
        success, img = cap.read()

        img.flags.writeable = False
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img)

# Função: identificando as maos e desenhando os pontos
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for limite_de_mao in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    img,
                    limite_de_mao,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

        hls = results.multi_hand_landmarks

# Função: detecção das mãos
        if hls and len(hls) == 2:

# Função: menor valora 1 mao detectada
            min_x_hand_1 = min(list(
                map(lambda l: l.x, hls[0].landmark)))
            
# Função: menor valor 2 mao detectada
            min_x_hand_2 = min(list(
                map(lambda l: l.x, hls[1].landmark)))
            maoPrimeiroJogador = hls[0] if min_x_hand_1 < min_x_hand_2 else hls[1]
            maoSegundoJogador = hls[0] if min_x_hand_1 > min_x_hand_2 else hls[1]

            if (getHandGesture(maoSegundoJogador) != gestoPlayer2 or getHandGesture(maoPrimeiroJogador) != gestoPlayer1):

                print("Primeira mao", min_x_hand_1)
                print("Segunda mao", min_x_hand_2)

# Função: pegar a mao da direita
                gestoPlayer2 = getHandGesture(maoSegundoJogador)

# Função: pegar a mao da esquerda
                gestoPlayer1 = getHandGesture(maoPrimeiroJogador)

# Função: condicoes para quem ganha if e else
                if success:
                    if gestoPlayer1 == gestoPlayer2:
                        vencedor = 0
                    elif gestoPlayer1 == "papel" and gestoPlayer2 == "pedra":
                        vencedor = 1
                    elif gestoPlayer1 == "papel" and gestoPlayer2 == "tesoura":
                        vencedor = 2
                    elif gestoPlayer1 == "pedra" and gestoPlayer2 == "tesoura":
                        vencedor = 1
                    elif gestoPlayer1 == "pedra" and gestoPlayer2 == "papel":
                        vencedor = 2
                    elif gestoPlayer1 == "tesoura" and gestoPlayer2 == "papel":
                        vencedor = 1
                    elif gestoPlayer1 == "tesoura" and gestoPlayer2 == "pedra":
                        vencedor = 2
                    else:
                        print("404 Not Found")
                else:
                    success = False

                if vencedor == 1:
                    pontuacao[0] += 1
                elif vencedor == 2:
                    pontuacao[1] += 1

        round_result = "O jogo empatou" if vencedor == 0 else f"Jogador {vencedor} venceu!"

# Função: Para os textos: cor e fonte
        cv2.putText(img, round_result, (600, 950),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (252, 3, 255), 2)
        cv2.putText(img, str("Jogador 1"), (100, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (252, 3, 255), 2)
        cv2.putText(img, gestoPlayer1, (100, 300),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (252, 3, 255), 2)
        cv2.putText(img, str(pontuacao[0]), (100, 400),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (252, 3, 255), 2)
        cv2.putText(img, str('Jogador 2'), (1400, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (252, 3, 255), 2)
        cv2.putText(img, gestoPlayer2, (1400, 300),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (252, 3, 255), 2)
        cv2.putText(img, str(pontuacao[1]), (1400, 400),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (252, 3, 255), 2)
        
# Função: Definição de tamanho
        cv2.namedWindow('Hands', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Hands', 960, 540)
        cv2.imshow('Hands', img)

# Função: Ao colocar esse "q" ele vai parar de rodar
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
