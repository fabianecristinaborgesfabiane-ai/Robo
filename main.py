from flask import Flask
import threading
import os
import requests
import time

app = Flask(__name__)

# Configurações
TOKEN = "8751846011:AAHFs-ho649VPN4KioG2-4LHDOubj8Lq65s"
CHAT_ID = "-1003635020867"
API_KEY = "6487863945mshbffab968d1e5404p149d50jsnae9782728573"

@app.route('/')
def home():
    return "Robo Sofascore Ativo - 10 min", 200

def enviar_mensagem(texto):
    url_tel = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto}
    requests.post(url_tel, json=payload)

def executar_meu_robo():
    # URL do Sofascore para jogos ao vivo
    url = "https://sofascore.p.rapidapi.com/v1/sport/football/events/live"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "sofascore.p.rapidapi.com"
    }
    
    while True:
        try:
            print("🔄 Checando Sofascore...", flush=True)
            resposta = requests.get(url, headers=headers, timeout=15)
            
            if resposta.status_code == 200:
                print("✅ Sucesso!", flush=True)
                # Processamento dos jogos ao vivo vai aqui
            else:
                print(f"⚠️ Erro na API: {resposta.status_code}", flush=True)
                
            time.sleep(600) # 10 minutos
            
        except Exception as e:
            print(f"❌ Erro: {e}", flush=True)
            time.sleep(60)

threading.Thread(target=executar_meu_robo, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
