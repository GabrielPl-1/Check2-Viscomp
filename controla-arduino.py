import cv2
import mediapipe as mp
import serial
import time

# Configurar a porta serial
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)

# Inicializa o MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Captura da câmera
cap = cv2.VideoCapture(0)

def dedo_levantado(pontos, tip, pip):
    return pontos[tip].y < pontos[pip].y

def polegar_levantado(pontos, direita=True):
    if direita:
        return pontos[4].x < pontos[3].x  # Tip à esquerda do IP para mão direita
    else:
        return pontos[4].x > pontos[3].x  # Tip à direita do IP para mão esquerda

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Erro ao carregar a câmera.")
        break

    frame = cv2.resize(frame, (500, 500))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks, hand_info in zip(result.multi_hand_landmarks, result.multi_handedness):
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            pontos = hand_landmarks.landmark

            # Verifica se a mão é direita ou esquerda
            is_direita = hand_info.classification[0].label == "Right"

            polegar = polegar_levantado(pontos, direita=is_direita)
            indicador = dedo_levantado(pontos, 8, 6)
            medio    = dedo_levantado(pontos, 12, 10)
            anelar   = dedo_levantado(pontos, 16, 14)
            mindinho = dedo_levantado(pontos, 20, 18)

            dedos = [polegar, indicador, medio, anelar, mindinho]

            if polegar and not indicador and not medio and not anelar and not mindinho:
                arduino.write(b'C')  # Joinha
            elif all(dedos):
                arduino.write(b'P')  # Todos os dedos levantados

    cv2.imshow("Video", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
