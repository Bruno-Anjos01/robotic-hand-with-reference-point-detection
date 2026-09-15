# 🖐️ Mão Robótica com Arduino, Python e MediaPipe

Projeto de uma **mão robótica controlada por visão computacional**, utilizando uma câmera para identificar os movimentos da mão do usuário e reproduzi-los em uma mão robótica através de servomotores.

O projeto utiliza **Python, MediaPipe, OpenCV, pyFirmata e Arduino UNO**.

> Este projeto é uma modificação de um projeto originalmente desenvolvido por **Wellington Isac Souza (WellingtonDev25)**.  
> A versão presente neste repositório contém modificações e adaptações realizadas por mim.

---

## 📖 Sobre o projeto

A câmera captura a mão do usuário em tempo real e o **MediaPipe** identifica os 21 pontos de referência (landmarks) da mão.

A partir desses pontos, o programa determina se cada dedo está **aberto ou fechado**.

O Python então envia comandos para o **Arduino UNO** através da biblioteca **pyFirmata**, fazendo com que cinco servomotores reproduzam os movimentos dos dedos.

O projeto utiliza um servomotor para cada dedo:

| Dedo | Pino Arduino |
|---|---|
| Polegar | D10 |
| Indicador | D9 |
| Médio | D8 |
| Anelar | D7 |
| Mínimo | D6 |

---

## 🛠️ Tecnologias utilizadas

- Python 3
- Arduino UNO
- Protoboard
- Jumpers macho-macho
- adaptador P4 fêmea 5,5 × 2,1 mm para borne de parafuso para fonte
- MediaPipe
- OpenCV
- pyFirmata
- StandardFirmata
- 5 servomotores SG90 de 180°
- Webcam
- Fonte externa de 5V e 5A para os servomotores

---

## 📦 Dependências

As principais bibliotecas Python utilizadas são:

```txt
opencv-python==4.9.0.80
mediapipe==0.10.11
pillow==10.2.0
protobuf==3.20.3
pyFirmata==1.1.0
```

Para instalar as dependências:

```
pip install -r requirements.txt
```

---

## 🔌 Configuração do Arduino

A comunicação entre Python e Arduino é realizada utilizando **pyFirmata**.

Por isso, o Arduino precisa estar executando o firmware **StandardFirmata**.

No Arduino IDE, acesse:

```text
Arquivo > Exemplos > Firmata > StandardFirmata
```

Selecione:

```text
Placa: Arduino UNO
Porta: porta correspondente ao Arduino
```

Depois envie o **StandardFirmata** para o Arduino.

> ⚠️ Depois de carregar o StandardFirmata, feche o Monitor Serial do Arduino IDE antes de executar o programa Python. Caso contrário, a porta COM poderá ficar ocupada.

---

## 🔧 Ligações dos servomotores

Os servomotores são conectados aos seguintes pinos:

```text
Polegar    -> D10
Indicador  -> D9
Médio      -> D8
Anelar     -> D7
Mínimo     -> D6
```

Os fios de sinal dos servos são conectados ao Arduino UNO R3.

A alimentação dos servomotores é realizada através de uma **fonte externa de 5V e 5A**.

Exemplo:

```text
                    postivo e negativo ---------------- Servo Polegar
                    |
                    postivo e negativo ---------------- Servo Indicador
                    |
Fonte 5V (+) <----- Protoboard ------- postivo e negativo ---------------- Servo Médio
                    |
                    postivo e negativo ---------------- Servo Anelar
                    |
                    postivo e negativo ---------------- Servo Mínimo


⚠️ negativo do protoboard -------------- GND do Arduino
```

> ⚠️ O GND da fonte externa e o GND do Arduino devem estar conectados.

---

## ⚙️ Funcionamento

O funcionamento do projeto pode ser resumido da seguinte maneira:

```text
Webcam
   ↓
OpenCV
   ↓
MediaPipe
   ↓
Detecção dos dedos
   ↓
Python
   ↓
pyFirmata
   ↓
Arduino UNO
   ↓
Servomotores
   ↓
Mão Robótica
```

O MediaPipe identifica se cada dedo está aberto ou fechado.

Quando o estado de um dedo muda, o Python envia uma nova posição para o servo correspondente.

---

## 🎛️ Servomotores

Os servomotores utilizados são **SG90 de 180°**.

Portanto, os valores enviados representam posições.

Por exemplo:

```python
ABERTO = {
    10: 20,
    9: 20,
    8: 20,
    7: 20,
    6: 20
}

FECHADO = {
    10: 150,
    9: 160,
    8: 160,
    7: 160,
    6: 160
}
```

Os valores podem ser alterados de acordo com a montagem da mão robótica.

> ⚠️ Evite utilizar ângulos que façam o servo continuar forçando depois que o dedo atingir o limite mecânico.

---

## 📁 Estrutura do projeto

```text
mao-robotica-mediapipe/
│
├── main.py
├── servo_braco3d.py
├── requirements.txt
└── README.md
```

### `main.py`

Responsável por:

- Capturar a imagem da webcam;
- Executar o MediaPipe;
- Detectar a mão;
- Identificar os dedos abertos e fechados;
- Mostrar os landmarks na tela;
- Enviar os estados dos dedos para o controle dos servos.

### `servo_braco3d.py`

Responsável por:

- Conectar o Python ao Arduino;
- Configurar os pinos dos servomotores;
- Definir os ângulos de abertura;
- Definir os ângulos de fechamento;
- Controlar a posição de cada servo.

---

## ▶️ Como executar

Primeiro, carregue o **StandardFirmata** no Arduino.

Depois instale as dependências:

```bash
py -m pip install -r requirements.txt
```

Verifique a porta do Arduino no arquivo `servo_braco3d.py`.

Exemplo:

```python
board = Arduino('COM6')
```

Depois execute:

```bash
py main.py
```

A câmera será aberta e o MediaPipe começará a detectar os movimentos da mão.

Para encerrar o programa, pressione:

```text
Q
```

---

## 🔍 MediaPipe

O MediaPipe identifica **21 pontos da mão**.

Esses pontos são utilizados para determinar a posição dos dedos.

O sistema identifica:

- Polegar
- Indicador
- Médio
- Anelar
- Mínimo

Quando o usuário abre ou fecha um dedo, o programa altera a posição do servo correspondente.

---

## 🤝 Autores e créditos

### Projeto original

**Wellington Isac Souza**  
GitHub: **WellingtonDev25**

### Modificações

Esta versão é uma **modificação e adaptação do projeto original**, com alterações realizadas para adequar o software e o hardware à implementação desta mão robótica.

Entre as modificações estão ajustes relacionados ao controle dos servomotores, comunicação com o Arduino, detecção dos dedos e funcionamento geral do sistema.

Todo o crédito pela **ideia e implementação inicial do projeto** é mantido para **Wellington Isac Souza (WellingtonDev25)**.

---

## 📄 Licença

Este projeto é baseado em um trabalho existente.

Antes de redistribuir, modificar ou aplicar uma licença a esta versão, consulte a licença e os termos definidos no projeto original.

---

## 👊 Agradecimentos

Agradecimentos a **Wellington Isac Souza (WellingtonDev25)** pelo desenvolvimento e disponibilização do projeto inicial que serviu como base para esta versão.