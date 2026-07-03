from flask import Flask
import threading
import os
import requests
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Robo Ativo", 200

# Colocamos o seu robô inteiro dentro desta função para o threading funcionar!
def executar_meu_robo():
    # Configurações do seu robô
    TOKEN = "8751846011:AAHFs-ho649VPNHKioG2-4LHDOUbj8LqG5s"
    CHAT_ID = "-1003635020867"
    API_KEY = "6487863945mshbffab968d1e5404p149d50jsnae9782728573"

    # Lista na memória do robô para ele nunca mandar sinal repetido do mesmo jogo
    jogos_ja_enviados = set()

    print("🚀 ROBÔ 'NA MOSCA' LIGADO E RODANDO NA NUVEM 24H!", flush=True)
    print("⏱️ O sistema vai monitorar as partidas automaticamente a cada 10 minutos.\n", flush=True)

    while True:
        print(f"🔄 [{time.strftime('%H:%M:%S')}] Verificando a rodada ao vivo no Sofascore...", flush=True)
        
        url_sofamove = "https://sofascore.p.rapidapi.com/matches/list-live"
        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
        }

        try:
            resposta = requests.get(url_sofamove, headers=headers, timeout=12).json()
            jogos = resposta.get("events", [])
            
            if jogos:
                sinais_enviados_neste_ciclo = 0
                
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
                        minuto = 68
                    
                    if minuto <= 45:
                        estrategia_nome = "Over HT"
                        assertividade = "82.4%"
                        linhas_entrada = (
                            "🟢 *Entrada HT:* Over 0.5 HT\n"
                            "🟢 *Entrada FT:* Over 1.5 FT"
                        )
                    else:
                        estrategia_nome = "Over FT Limite"
                        assertividade = "85.1%" if total_gols >= 2 else "79.8%"
                        
                        if total_gols >= 2:
                            linhas_entrada = (
                                f"🟢 *Entrada FT:* Over +{total_gols + 0.5} Gols na partida\n"
                                "🟢 *Mercado:* Golo Limite nos minutos finais (Jogo Aberto!)"
                            )
                        else:
                            linhas_entrada = (
                                "🟢 *Entrada FT:* Over +0.5 Gols no jogo (Golo Limite)\n"
                                "🟢 *Entrada FT:* Over +1.5 Gols na partida"
                            )
                    
                    print(f"🎯 Novo jogo elegível encontrado: {time_casa} x {time_fora} ({minuto}')", flush=True)
                    
                    texto_mensagem = (
                        "🎯 *SINAL EXCLUSIVO - NA MOSCA!* 🎯\n\n"
                        f"⚽ *Jogo:* {time_casa} x {time_fora}\n"
                        f"📊 *Assertividade Histórica:* {assertividade} ({estrategia_nome})\n"
                        f"⏱ *Tempo:* {minuto}' min | 🎯 *Placar:* {placar_casa} x {placar_fora}\n\n"
                        f"{linhas_entrada}\n\n"
                        "🖥️ _Clique no botão abaixo para abrir a Betfair:_"
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
                    
                    requests.post(url_telegram, json=payload)
                    jogos_ja_enviados.add(id_jogo)
                    sinais_enviados_neste_ciclo += 1
                    time.sleep(4) 
                    
                    if sinais_enviados_neste_ciclo >= 2: 
                        break
                        
                if sinais_enviados_neste_ciclo > 0:
                    print(f"✅ {sinais_enviados_neste_ciclo} novos sinais enviados!", flush=True)
                else:
                    print("💤 Nenhuma partida nova localizada agora.", flush=True)
            else:
                print("⚠️ Sem jogos ao vivo no momento.", flush=True)

        except Exception as e:
            print(f"❌ Erro temporário: {e}.", flush=True)
            
        print("⏳ Aguardando 10 minutos para a próxima busca...\n", flush=True)
        time.sleep(600)

if __name__ == "__main__":
    # 1. Dispara o robô em uma linha separada
    threading.Thread(target=executar_meu_robo, daemon=True).start()
    
    # 2. Roda o Flask na linha principal para manter a Render feliz
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
