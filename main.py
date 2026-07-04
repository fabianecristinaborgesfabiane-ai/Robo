from flask import Flask
import threading
import os
import requests
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Robo Ativo - 10 min", 200

def executar_meu_robo():
    TOKEN = "8751846011:AAHFs-ho649VPN4KioG2-4LHDOubj8Lq65s"
    CHAT_ID = "-1003635020867"
    API_KEY = "6487863945mshbffab968d1e5404p149d50jsnae9782728573"
    
    # URL base da Free API Live Football Data
    url = "https://free-api-live-football-data.p.rapidapi.com/football-live"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    
    while True:
        try:
            print("🔄 Iniciando checagem (ciclo de 10 min)...", flush=True)
            resposta = requests.get(url, headers=headers, timeout=15)
            
            print(f"📡 Status da API: {resposta.status_code}", flush=True)
            
            if resposta.status_code == 200:
                print("✅ Conexão OK! Processando jogos ao vivo...", flush=True)
                # O processamento dos dados entraria aqui
            else:
                print(f"⚠️ Erro na API: {resposta.text}", flush=True)
                
            print("😴 Aguardando 10 minutos para o próximo ciclo...", flush=True)
            time.sleep(600) # 600 segundos = 10 minutos
            
        except Exception as e:
            print(f"❌ Erro crítico: {e}", flush=True)
            time.sleep(60)

threading.Thread(target=executar_meu_robo, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
