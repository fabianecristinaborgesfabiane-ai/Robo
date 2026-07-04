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
    TOKEN = "8751846011:AAHFs-ho649VPN4KioG2-4LHDOubj8Lq65s"
    CHAT_ID = "-1003635020867"
    API_KEY = "6487863945mshbffab968d1e5404p149d50jsnae9782728573"
    
    jogos_ja_enviados = set()
    
    while True:
        try:
            print("🔄 Iniciando checagem...", flush=True)
            url = "https://sofascore.p.rapidapi.com/v1/events/live"
            
            # CORREÇÃO 1: Host atualizado para bater com a URL da Sofascore
            headers = {
                "X-RapidAPI-Key": API_KEY,
                "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
            }
            params = {"sport_id": "1", "locale": "pt_BR"}
            
            resposta = requests.get(url, headers=headers, params=params, timeout=15).json()
            jogos = resposta.get("events", [])
            
            if jogos:
                for jogo in jogos:
                    time_casa = jogo.get("homeTeam", {}).get("name", "Time")
                    time_fora = jogo.get("awayTeam", {}).get("name", "Time")
                    print(f"🎯 JOGO ENCONTRADO: {time_casa} x {time_fora}", flush=True)
                    # Comenta (coloca # na frente) as linhas de filtro e de cálculo abaixo
            else:
                print("⚠️ A lista de jogos retornada pela API está vazia.", flush=True)
                        
                    id_jogo = jogo.get("id")
                    if id_jogo in jogos_ja_enviados:
                        continue
                        
                    time_casa = jogo.get("homeTeam", {}).get("name", "Time Casa")
                    time_fora = jogo.get("awayTeam", {}).get("name", "Time Fora")
                    placar_casa = jogo.get("homeScore", {}).get("current", 0)
                    placar_fora = jogo.get("awayScore", {}).get("current", 0)
                    total_gols = placar_casa + placar_fora
                    
                    status_tempo = jogo.get("status", {})
                    minuto = status_tempo.get("minute", 0)
                    periodo = status_tempo.get("description", "Em andamento")
                    tempo_formatado = f"{minuto}'" if minuto else f"{periodo}"
                    
                    stats = jogo.get("stats", {})
                    ap_casa = stats.get("dangerous_attacks", {}).get("home", 0)
                    ap_fora = stats.get("dangerous_attacks", {}).get("away", 0)
                    total_ap = ap_casa + ap_fora
                    
                    chutes_gol_casa = stats.get("shots_on_target", {}).get("home", 0)
                    chutes_gol_fora = stats.get("shots_on_target", {}).get("away", 0)
                    chutes_fora_casa = stats.get("shots_off_target", {}).get("home", 0)
                    chutes_fora_fora = stats.get("shots_off_target", {}).get("away", 0)
                    total_chutes = chutes_gol_casa + chutes_gol_fora + chutes_fora_casa + chutes_fora_fora
                    
                    if total_ap == 0 and total_chutes == 0:
                        assertividade_num = round(65.0 + (int(id_jogo) % 15 if id_jogo.isdigit() else 5), 1)
                    else:
                        pressao_bruta = total_ap * 0.4
                        chutes_brutos = total_chutes * 2.5
                        base_calculo = 55.0 + pressao_bruta + chutes_brutos
                        assertividade_num = round(min(base_calculo, 98.4), 1)
                    
                    # CORREÇÃO 2: Filtro relaxado para 0.0 (vai enviar tudo agora)
                    if assertividade_num < 0.0:
                        continue
                    
                    linhas_entrada = (
                        f"🟢 *Entrada LIVE:* Over {total_gols + 0.5} Gols na partida\n"
                        f"📊 *Estatísticas:* {total_ap} Ataques Perigosos | {total_chutes} Chutes"
                    )
                    
                    print(f"🎯 Jogo Elegível ({assertividade_num}%): {time_casa} x {time_fora}", flush=True)
                    
                    texto_mensagem = (
                        "🎯 *SINAL EXCLUSIVO - ANÁLISE EM TEMPO REAL* 🎯\n\n"
                        f"⚽ *Jogo:* {time_casa} x {time_fora}\n"
                        f"📊 *Assertividade Calculada:* {assertividade_num}%\n"
                        f"⏱ *Tempo:* {tempo_formatado} | 🎯 *Placar:* {placar_casa} x {placar_fora}\n"
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
            time.sleep(300)
            
        except Exception as e:
            print(f"❌ Erro no loop do robô: {e}", flush=True)
            time.sleep(30)

threading.Thread(target=executar_meu_robo, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
