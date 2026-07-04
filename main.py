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
    # URL padronizada para busca de eventos
    url = "https://sofascore.p.rapidapi.com/matches/live"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "sofascore.p.rapidapi.com"
    }

    while True:
        try:
            print("🔄 Buscando jogos ao vivo...", flush=True)
            resposta = requests.get(url, headers=headers, timeout=15)
            
            # Se for 200, ele encontrou o endpoint
            if resposta.status_code == 200:
                print("✅ Conectado com sucesso!", flush=True)
                # Lógica de análise de probabilidade virá aqui
            else:
                print(f"⚠️ Status da API: {resposta.status_code}", flush=True)
                
            time.sleep(600) 
            
        except Exception as e:
            print(f"❌ Erro: {e}", flush=True)
            time.sleep(60)

threading.Thread(target=monitorar_jogos, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
