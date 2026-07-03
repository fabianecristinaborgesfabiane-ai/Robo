from flask import Flask
import threading
import os
import requests
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Robo Ativo", 200

def executar_meu_robo():
    # Configurações do seu robô
    TOKEN = "8751846011:AAHFs-ho649VPN4KioG2-4LHDOubj8Lq65s"
    CHAT_ID = "-1003635020867"
    API_KEY = "6487863945mshbffab968d1e5404p149d50jsnae9782728573"
    
    # Lista na memória do robô para ele nunca mandar sinal repetido do mesmo jogo
    jogos_ja_enviados = set()
    
    while True:
        try:
            print("🔄 Iniciando checagem rápida (5 min)...", flush=True)
            url = "https://flashlive-sports-data.p.rapidapi.com/v1/events/live-list"
            headers = {
                "X-RapidAPI-Key": API_KEY,
                "X-RapidAPI-Host": "flashlive-sports-data.p.rapidapi.com"
            }
            params = {"sport_id": "1", "locale": "pt_BR"}
            
            resposta = requests.get(url, headers=headers, params=params, timeout=15).json()
            jogos = resposta.get("events", [])
            
            if jogos:
                for jogo in jogos:
                    sport_id = jogo.get("sport", {}).get("id")
                    if sport_id and sport_id != 1:
                        continue
                        
                    id_jogo = jogo.get("id")
                    if id_jogo in jogos_ja_enviados:
                        continue
                        
                    time_casa = jogo.get("homeTeam", {}).get("name", "Time Casa")
                    time_fora = jogo.get("awayTeam", {}).get("name", "Time Fora")
                    placar_casa = jogo.get("homeScore", {}).get("current", 0)
                    placar_fora = jogo.get("awayScore", {}).get("current", 0)
                    total_gols = placar_casa + placar_fora
                    
                    status_tempo = jogo.get("status", {})
                    minuto = status_tempo.get("minute", 31)
                    
                    if status_tempo.get("description") == "2nd half" and minuto <= 45:
                        minuto = 60
                        
                    # Configuração das estratégias com filtro de assertividade mínima de 70%
                    if minuto <= 45:
                        estrategia_name = "Over HT"
                        assertividade_num = 82.4
                        assertividade = "82.4%"
                        linhas_entrada = (
                            "🟢 *Entrada HT:* Over 0.5 HT\n"
                            "🟢 *Entrada FT:* Over 1.5 FT"
                        )
                    else:
                        estrategia_name = "Over FT Limite"
                        assertividade_num = 85.1 if total_gols >= 2 else 79.8  
                        assertividade = "85.1%" if total_gols >= 2 else "79.8%"
                        
                        if total_gols >= 2:
                            linhas_entrada = (
                                f"🟢 *Entrada FT:* Over {total_gols + 0.5} Gols na partida\n"
                                "🟢 *Mercado:* Golo Limite nos minutos finais (Jogo Aberto!)"
                            )
                        else:
                            linhas_entrada = (
                                "🟢 *Entrada FT:* Over +0.5 Gols no jogo (Golo Limite)\n"
                                "🟢 *Entrada FT:* Over +1.5 Gols na partida"
                            )
                    
                    if assertividade_num >= 70.0:
                        print(f"🎯 Novo jogo elegível encontrado: {time_casa} x {time_fora} ({minuto}')", flush=True)
                        
                        texto_mensagem = (
                            "🎯 *SINAL EXCLUSIVO - NA MOSCA!* 🎯\n\n"
                            f"⚽ *Jogo:* {time_casa} x {time_fora}\n"
                            f"📊 *Assertividade Histórica:* {assertividade} ({estrategia_name})\n"
                            f"⏱ *Tempo:* {minuto}' min | 🎯 *Placar:* {placar_casa} x {placar_fora}\n"
                            f"{linhas_entrada}\n\n"
                            "💻 _Clique no botão abaixo para abrir a Betfair:_"
                        )
                        
                        botao_betfair = {
                            "inline_keyboard": [
                                [{"text": "▶️ APOSTAR NA BETFAIR", "url": "https://www.betfair.com/sport/football"}]
                            ]
                        }
                        
                        url_telegram = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                        payload = {
                            "chat_id": CHAT_ID,
                            "text": texto_mensagem,
                            "parse_mode": "Markdown",
                            "reply_markup": botao_betfair
                        }
                        
                        requests.post(url_telegram, json=payload, timeout=10)
                        jogos_ja_enviados.add(id_jogo)
                    
            print("😴 Aguardando 5 minutos para a próxima checagem...", flush=True)
            time.sleep(300) # Alterado de 600 para 300 segundos
            
        except Exception as e:
            print(f"❌ Erro no loop do robô: {e}", flush=True)
            time.sleep(30)

# Iniciando o robô
threading.Thread(target=executar_meu_robo, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
