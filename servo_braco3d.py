from pyfirmata import Arduino, SERVO
import time

# ============================================================
# CONEXÃO COM O ARDUINO
# ============================================================

board = Arduino('COM6')

# ============================================================
# PINOS DOS SERVOS
# ============================================================

POLEGAR = 10
INDICADOR = 9
MEDIO = 8
ANELAR = 7
MINIMO = 6

pinos = [
    POLEGAR,
    INDICADOR,
    MEDIO,
    ANELAR,
    MINIMO
]

# ============================================================
# CONFIGURA OS PINOS COMO SERVO
# ============================================================

for pin in pinos:
    board.digital[pin].mode = SERVO

# Pequena espera para estabilizar a comunicação
time.sleep(1)

# ============================================================
# ÂNGULOS DOS SERVOS
# ============================================================
#
# Ajuste esses valores conforme a mecânica da mão.
#
# Evite começar usando exatamente 0 e 180,
# pois o servo pode forçar no limite.
# ============================================================

ABERTO = {
    POLEGAR: 20,
    INDICADOR: 20,
    MEDIO: 20,
    ANELAR: 20,
    MINIMO: 20
}


FECHADO = {
    POLEGAR: 150,
    INDICADOR: 160,
    MEDIO: 160,
    ANELAR: 160,
    MINIMO: 160
}

# ============================================================
# FUNÇÃO BÁSICA PARA POSICIONAR SERVO
# ============================================================

def rotateServo(pino, angulo):

    # Segurança para não enviar ângulo inválido
    if angulo < 0:
        angulo = 0

    if angulo > 180:
        angulo = 180

    board.digital[pino].write(angulo)

# ============================================================
# ABRIR / FECHAR UM DEDO
# ============================================================

def abrir_fechar(pin, estado):
    """
    estado = 1 -> dedo aberto
    estado = 0 -> dedo fechado
    """

    if pin not in pinos:
        print(f"Pino inválido: {pin}")
        return

    if estado == 1:

        angulo = ABERTO[pin]

        print(
            f"Servo {pin} -> ABERTO ({angulo} graus)"
        )

        rotateServo(
            pin,
            angulo
        )

    elif estado == 0:

        angulo = FECHADO[pin]

        print(
            f"Servo {pin} -> FECHADO ({angulo} graus)"
        )

        rotateServo(
            pin,
            angulo
        )

# ============================================================
# ABRIR TODOS
# ============================================================

def abrir_todos():

    print("Abrindo todos os dedos...")

    for pin in pinos:

        rotateServo(
            pin,
            ABERTO[pin]
        )

        time.sleep(0.05)

# ============================================================
# FECHAR TODOS
# ============================================================

def fechar_todos():

    print("Fechando todos os dedos...")

    for pin in pinos:

        rotateServo(
            pin,
            FECHADO[pin]
        )

        time.sleep(0.05)

# ============================================================
# TESTE INDIVIDUAL
# ============================================================

def testar_servo(pin):

    if pin not in pinos:
        print("Pino inválido.")
        return

    print(
        f"Testando servo do pino {pin}"
    )

    # Aberto
    rotateServo(
        pin,
        ABERTO[pin]
    )

    time.sleep(1)

    # Fechado
    rotateServo(
        pin,
        FECHADO[pin]
    )

    time.sleep(1)

    # Volta aberto
    rotateServo(
        pin,
        ABERTO[pin]
    )

# ============================================================
# TESTE DE TODOS OS SERVOS
# ============================================================

def testeTodos():

    print("Iniciando teste dos servos...")


    for pin in pinos:

        print(
            f"Testando pino {pin}"
        )

        rotateServo(
            pin,
            ABERTO[pin]
        )

        time.sleep(0.8)

        rotateServo(
            pin,
            FECHADO[pin]
        )

        time.sleep(0.8)

        rotateServo(
            pin,
            ABERTO[pin]
        )

        time.sleep(0.5)

    print("Teste concluído.")

# ============================================================
# ENCERRAR CONEXÃO
# ============================================================

def encerrar():

    print("Encerrando conexão com Arduino...")

    board.exit()
