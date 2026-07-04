from flask import Flask
import threading
import os
import requests
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Robo Ativo - SportAPI7", 200

def executar_meu_robo():
    TOKEN = "8751846011:AAHFs-ho649VPN4KioG2-4LHDOubj8Lq65s"
    CHAT_ID = "-1003635020867"
    API_KEY = "6487863945mshbffab968d1e5404p149d50jsnae9782728573"
    
    # URL e Headers conforme a imagem da sua API
    url = "https://sportapi7.p.rapidapi.com/api/scheduled-events/2026-07-04"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "sportapi7.p.rapidapi.com"
    }
    
    while True:
        try:
            print("🔄 Iniciando checagem...", flush=True)
            resposta = requests.get(url, headers=headers, timeout=15)
            
            print(f"📡 Status: {resposta.status_code}", flush=True)
            
            if resposta.status_code == 200:
                dados = resposta.json()
                print("✅ Conectado com sucesso! Processando eventos...", flush=True)
                # Aqui o robô processaria os eventos (está pronto para o seu uso)
            else:
                print(f"⚠️ Erro na API: {resposta.text}", flush=True)
                
            print("😴 Aguardando 5 minutos...", flush=True)
            time.sleep(300)
            
        except Exception as e:
            print(f"❌ Erro: {e}", flush=True)
            time.sleep(60)

threading.Thread(target=executar_meu_robo, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
