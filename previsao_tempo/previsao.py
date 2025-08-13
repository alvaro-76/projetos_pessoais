import requests, pytz, time, os
from datetime import datetime

API_KEY = '543443696a8f7dd5b6a4ec71f0c1af1f'


def obter_entrada(label):
    try:
        entrada = int(input(label))
        if entrada == 1 or entrada == 0:
            return entrada
        else:
            print('INVALIDO')
            return obter_entrada(label)
    except ValueError:
        print('INVALIDO')
        return obter_entrada(label)
    

def dados(cidade):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()

        temperatura = dados['main']['temp']
        umidade = dados['main']['humidity']
        condicao = dados['weather'][0]['description']
        if "nuvem" in condicao.lower():
            icone = "☁️"
        elif "chuva" in condicao.lower():
            icone = "🌧️"
        elif "céu limpo" in condicao.lower():
            icone = "🌧️"
        else:
            icone = "🌤️"

        timezone_offset = dados['timezone']
        tz = pytz.FixedOffset(timezone_offset / 60)
        hora_local = datetime.now(tz).strftime('%H:%M:%S')

        print('='*60)
        resultado = f'''
        =====PREVISÃO DO TEMPO=====
    Cidade: {cidade}
    Horário local: {hora_local}
    Temperatura: {temperatura:.1f} °C
    Umidade: {umidade}%
    Tempo: {condicao.capitalize()}{icone}    
'''
        print(resultado)
    else:
        print(f'ERRO {resposta.status_code}!')


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    menu = '''
    1 - Obter informações de uma determinada cidade
    0 - Sair
    -> '''

    option = obter_entrada(menu)
    while option != 0:
        cidade = input('Informe a cidade(cidade,estado,país): ')
        dados(cidade)

        print('='*60)
        input('continue...')
        os.system('cls' if os.name == 'nt' else 'clear')
        option = obter_entrada(menu)

    print('Encerrando...')
