import cv2
import mediapipe as mp
import servo_braco3d as mao

# ============================================================
# CONFIGURAÇÃO DA CÂMERA
# ============================================================

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ============================================================
# CONFIGURAÇÃO DO MEDIAPIPE
# ===========================================q=================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# ============================================================
# PINOS DOS SERVOS
# ============================================================

POLEGAR = 10
INDICADOR = 9
MEDIO = 8
ANELAR = 7
MINIMO = 6

# ============================================================
# ESTADO ANTERIOR DOS DEDOS
# ============================================================

# Estado atual confirmado dos dedos
estado_anterior = {
    POLEGAR: None,
    INDICADOR: None,
    MEDIO: None,
    ANELAR: None,
    MINIMO: None
}

# Estado que está sendo observado pela câmera
estado_candidato = {
    POLEGAR: None,
    INDICADOR: None,
    MEDIO: None,
    ANELAR: None,
    MINIMO: None
}

# Quantos frames seguidos o mesmo estado apareceu
contador_estado = {
    POLEGAR: 0,
    INDICADOR: 0,
    MEDIO: 0,
    ANELAR: 0,
    MINIMO: 0
}

# Quantidade de frames necessários para aceitar a mudança
FRAMES_CONFIRMACAO = 5

def atualizar_servo(pin, novo_estado):

    # Se mudou o estado que a câmera está enxergando,
    # começa a contagem novamente
    if estado_candidato[pin] != novo_estado:

        estado_candidato[pin] = novo_estado
        contador_estado[pin] = 1

    else:

        contador_estado[pin] += 1

    # Só movimenta depois de vários frames iguais
    if contador_estado[pin] >= FRAMES_CONFIRMACAO:

        if estado_anterior[pin] != novo_estado:

            if novo_estado == 1:
                print(f"Servo {pin}: ABRIR")
            else:
                print(f"Servo {pin}: FECHAR")

            mao.abrir_fechar(
                pin,
                novo_estado
            )

            estado_anterior[pin] = novo_estado

# ============================================================
# LOOP PRINCIPAL
# ============================================================

print("Sistema iniciado.")
print("Mostre a mão para a câmera.")
print("Pressione Q para sair.")

while True:

    success, img = cap.read()

    if not success:
        print("Erro ao capturar imagem da câmera.")
        break

    # Espelha a imagem
    img = cv2.flip(img, 1)

    # Converte BGR para RGB
    frameRGB = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    )

    # Processa a mão
    results = hands.process(frameRGB)

    h, w, _ = img.shape

    # ========================================================
    # SE UMA MÃO FOI DETECTADA
    # ========================================================

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Desenha os pontos e conexões da mão
            mp_draw.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            pontos = []

            # =================================================
            # PEGA OS 21 PONTOS DA MÃO
            # =================================================

            for id, cord in enumerate(hand_landmarks.landmark):

                cx = int(cord.x * w)
                cy = int(cord.y * h)

                pontos.append((cx, cy))

                # Desenha os pontos
                cv2.circle(
                    img,
                    (cx, cy),
                    4,
                    (255, 0, 0),
                    -1
                )

            # =================================================
            # VERIFICA SE TEM OS 21 PONTOS
            # =================================================

            if len(pontos) == 21:

                # =============================================
                # POLEGAR
                # =============================================

                distPolegar = abs(
                    pontos[17][0] -
                    pontos[4][0]
                )

                if distPolegar < 80:

                    atualizar_servo(
                        POLEGAR,
                        0
                    )

                    textoPolegar = "FECHADO"

                else:

                    atualizar_servo(
                        POLEGAR,
                        1
                    )

                    textoPolegar = "ABERTO"

                # =============================================
                # INDICADOR
                # =============================================

                distIndicador = (
                    pontos[5][1] -
                    pontos[8][1]
                )

                if distIndicador >= 1:

                    atualizar_servo(
                        INDICADOR,
                        1
                    )

                    textoIndicador = "ABERTO"

                else:

                    atualizar_servo(
                        INDICADOR,
                        0
                    )

                    textoIndicador = "FECHADO"

                # =============================================
                # MÉDIO
                # =============================================

                distMedio = (
                    pontos[9][1] -
                    pontos[12][1]
                )

                if distMedio >= 1:

                    atualizar_servo(
                        MEDIO,
                        1
                    )

                    textoMedio = "ABERTO"

                else:

                    atualizar_servo(
                        MEDIO,
                        0
                    )

                    textoMedio = "FECHADO"

                # =============================================
                # ANELAR
                # =============================================

                distAnelar = (
                    pontos[13][1] -
                    pontos[16][1]
                )

                if distAnelar >= 1:

                    atualizar_servo(
                        ANELAR,
                        1
                    )

                    textoAnelar = "ABERTO"

                else:

                    atualizar_servo(
                        ANELAR,
                        0
                    )

                    textoAnelar = "FECHADO"

                # =============================================
                # MÍNIMO
                # =============================================

                distMinimo = (
                    pontos[17][1] -
                    pontos[20][1]
                )

                if distMinimo >= 1:

                    atualizar_servo(
                        MINIMO,
                        1
                    )

                    textoMinimo = "ABERTO"

                else:

                    atualizar_servo(
                        MINIMO,
                        0
                    )

                    textoMinimo = "FECHADO"

                # =============================================
                # TEXTOS EM VERMELHO
                # =============================================

                cv2.putText(
                    img,
                    f"Polegar: {textoPolegar}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2
                )

                cv2.putText(
                    img,
                    f"Indicador: {textoIndicador}",
                    (10, 55),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2
                )

                cv2.putText(
                    img,
                    f"Medio: {textoMedio}",
                    (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2
                )

                cv2.putText(
                    img,
                    f"Anelar: {textoAnelar}",
                    (10, 105),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2
                )

                cv2.putText(
                    img,
                    f"Minimo: {textoMinimo}",
                    (10, 130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2
                )

    # ========================================================
    # MOSTRA A IMAGEM
    # ========================================================

    cv2.imshow(
        "Mao Robotica - MediaPipe",
        img
    )

    # Pressione Q para sair
    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord("q"):
        break

# ============================================================
# FINALIZAÇÃO
# ============================================================

print("Encerrando programa...")

hands.close()

cap.release()

cv2.destroyAllWindows()

print("Programa encerrado.")
