# Importa as bibliotecas necessárias
import cv2  # OpenCV para processamento de vídeo e imagens
import numpy as np  # NumPy para operações matemáticas

# Define a função principal para contar panelas
def contar_panelas(video_path):
    # Abre o arquivo de vídeo
    cap = cv2.VideoCapture(video_path)
    
    # Cria um subtrator de fundo para detectar objetos em movimento
    subtractor = cv2.createBackgroundSubtractorMOG2()
    
    # Inicializa o contador de panelas
    contador = 0
    
    # Dicionário para armazenar as panelas detectadas
    panelas = {}
    
    # Loop principal de processamento de cada frame do vídeo
    while cap.isOpened():
        # Lê o próximo frame do vídeo
        ret, frame = cap.read()
        
        # Se não conseguir ler o frame (fim do vídeo), sai do loop
        if not ret:
            break
            
        # Pré-processamento do frame:
        # 1. Converte para escala de cinza
        # 2. Aplica desfoque gaussiano para reduzir ruído
        # 3. Aplica subtração de fundo
        mask = subtractor.apply(cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (5,5), 0))
        
        # Operação morfológica para remover pequenos ruídos
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
        
        # Encontra contornos dos objetos detectados
        for cnt in cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
            # Filtra contornos pequenos (área menor que 500 pixels)
            if cv2.contourArea(cnt) > 500:
                # Obtém retângulo delimitador do contorno
                x,y,w,h = cv2.boundingRect(cnt)
                
                # Filtra por formato (proporção largura/altura entre 0.7 e 1.3)
                if 0.7 < w/h < 1.3:
                    # Calcula o centro do objeto
                    centro = (x+w//2, y+h//2)
                    
                    # Verifica se é uma panela nova (não muito próxima de uma já detectada)
                    if not any(np.linalg.norm(np.array(centro)-np.array(c)) < 50 for c,_ in panelas.values()):
                        # Incrementa o contador
                        contador += 1
                        
                        # Armazena a panela no dicionário
                        panelas[contador] = (centro, (x,y,w,h))
                        
                        # Desenha retângulo ao redor da panela
                        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                        
                        # Escreve o ID da panela
                        cv2.putText(frame, str(contador), (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        
        # Mostra o contador total no canto superior esquerdo
        cv2.putText(frame, f"Panelas: {contador}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        
        # Exibe o frame com as marcações
        cv2.imshow('Contagem de Panelas', frame)
        
        # Verifica se o usuário pressionou 'q' para sair
        if cv2.waitKey(30) == ord('q'):
            break
            
    # Libera os recursos e fecha as janelas
    cap.release()
    cv2.destroyAllWindows()
    
    # Retorna o total de panelas contadas
    return contador

# Exemplo de uso:
total = contar_panelas("linha_producao.mp4")
# print(f"Total de panelas contadas: {total}")