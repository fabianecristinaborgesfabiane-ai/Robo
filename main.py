def monitorar_jogos():
    # URL correta baseada nos endpoints disponíveis na sua imagem
    url = "https://sofascore.p.rapidapi.com/v1/categories/list-live"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "sofascore.p.rapidapi.com"
    }

    while True:
        try:
            print("🔄 Buscando categorias ao vivo...", flush=True)
            resposta = requests.get(url, headers=headers, timeout=15)
            
            if resposta.status_code == 200:
                print("✅ Conectado com sucesso!", flush=True)
                # Aqui o robô vai receber a lista de categorias com jogos ao vivo
            else:
                print(f"⚠️ Status da API: {resposta.status_code}", flush=True)
                
            time.sleep(600) 
            
        except Exception as e:
            print(f"❌ Erro: {e}", flush=True)
            time.sleep(60)
