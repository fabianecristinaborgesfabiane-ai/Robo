from flask import Flask
import threading
import os
import requests
import time

app = Flask(__name__)

# Configurações do seu Robô
TOKEN = "8751846011:AAHFs-ho649VPN4KioG2-4LHDOubj8Lq65s"
CHAT_ID = "-1003635020867"
API_KEY = "6487863945mshbffab968d1e5404p149d50jsnae9782728573"

@app.route('/')
def home():
    return "Robô Sofascore Operacional", 200

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, json=payload)

def monitorar_jogos():
    # URL do endpoint que você encontrou na imagem 93fbc23e-0092-4271-bffe-67071ee77972
    url = "https://sofascore.p.rapidapi.com/matches/get-h2h-events"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "sofascore.p.rapidapi.com"
    }
    
    # Você precisa colocar o ID do evento que quer monitorar aqui
    # Exemplo: params = {"eventIds": "1234567"}
    params = {"eventIds": "COLOCAR_ID_DO_JOGO_AQUI"} 

    while True:
        try:
            print("🔄 Iniciando verificação...", flush=True)
            resposta = requests.get(url, headers=headers, params=params, timeout=15)
            
            if resposta.status_code == 200:
                dados = resposta.json()
                print("✅ Conexão estável (200 OK)", flush=True)
                # Aqui entra a lógica de processamento que você precisa
            else:
                print(f"⚠️ Erro na API: {resposta.status_code} - {resposta.text}", flush=True)
                
            time.sleep(600) # 10 minutos
            
        except Exception as e:
            print(f"❌ Erro crítico: {e}", flush=True)
            time.sleep(60)

# Iniciar thread do robô
threading.Thread(target=monitorar_jogos, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# O código acima está estruturado para manter o serviço vivo e 
# realizar as checagens com o intervalo que você definiu.
