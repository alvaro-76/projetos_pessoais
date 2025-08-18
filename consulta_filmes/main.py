import requests, os, readchar

api_key = "8ae83a7b"
url = "http://www.omdbapi.com/"


def buscar_filmes(titulo):
    params = {"s": titulo, "apikey": api_key}
    resposta = requests.get(url, params=params)

    if resposta.status_code != 200:
        print(f'ERRO {resposta.status_code}!')
        return []
    
    dados = resposta.json()
    
    if dados.get("Response") == "True":
        return dados.get("Search", [])
    else:
        print("Nenhum filme encontrado")
        return []
    

def detalhar_filmes(imdb_id):
    params = {"i":imdb_id, "apikey": api_key}
    resposta = requests.get(url, params=params)

    if resposta.status_code != 200:
        print(f'ERRO {resposta.status_code}!')
        return
    
    dados = resposta.json()
    if dados.get("Response") == "True":
        return dados
    else:
        return
    

def exibir_detalhes(dados):
    limpar_tela()

    print(f'''
        ==========|DETALHES DO FILME|==========
    Título: {dados.get("Title", 'N/A')}
    Ano: {dados.get("Year", 'N/A')}
    Gênero: {dados.get("Genre", 'N/A')}
    Diretor: {dados.get("Director", 'N/A')}
    Atores: {dados.get("Actors", 'N/A')}
    Nota IMDb: {dados.get("imdbRating", 'N/A')}
    Enredo: {dados.get("Plot", 'N/A')}
''')


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def selecionar(opcoes):
    idx = 0

    while True:
        limpar_tela()
        print("Use ↑ ↓ para navegar e ENTER para selecionar:\n")

        for i, opcao in enumerate(opcoes):
            if i == idx:
                print(f"\033[44m\033[97m-> {opcao}\033[0m")
            else:
                print(f"   {opcao}")
                
        tecla = readchar.readkey()
        if tecla == readchar.key.UP and idx > 0:
            idx -= 1
        elif tecla == readchar.key.DOWN and idx < len(opcoes) - 1:
            idx += 1
        elif tecla == readchar.key.ENTER:
            return idx


def main():
    while True:
        menu = ["BUSCAR FILME", "SAIR"]
        escolha = selecionar(menu)

        if escolha == 1:
            print('Encerrando...')
            break

        titulo = input('NOME DO FILME: ')
        resultados = buscar_filmes(titulo)

        if resultados:
            idx_filme = selecionar([f"{f.get('Title')} ({f.get('Year')})" for f in resultados])
            imdb_id = resultados[idx_filme].get("imdbID")
            detalhes = detalhar_filmes(imdb_id)
            if detalhes:
                exibir_detalhes(detalhes)
                input('Press ENTER to continue')


if __name__ == "__main__":
    main()