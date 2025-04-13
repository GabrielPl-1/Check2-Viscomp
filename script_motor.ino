void setup() {
  // Configura os pinos como saída
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(11, OUTPUT);
  
  // Inicializa a comunicação serial
  Serial.begin(9600);

  // Estado inicial: 13 e 12 ligados, 11 desligado
  digitalWrite(13, HIGH);
  digitalWrite(12, HIGH);
  digitalWrite(11, LOW);
}

void loop() {
  // Verifica se há dados disponíveis na serial
  if (Serial.available() > 0) {
    char comando = Serial.read();  // Lê o caractere recebido

    if (comando == 'P') {
      // Desliga 13 e 12, liga 11
      digitalWrite(13, LOW);
      digitalWrite(12, LOW);
      digitalWrite(11, HIGH);
    }
    else if (comando == 'C') {
      // Liga 13 e 12, desliga 11
      digitalWrite(13, HIGH);
      digitalWrite(12, HIGH);
      digitalWrite(11, LOW);
    }
  }
}
