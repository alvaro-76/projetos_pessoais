import utils as ut, db, os


def cadastrar_evento(cliente_id):
    data = input('Data do evento(YYYY-MM-DD): ')
    duracao = input('Duração do evento(HH:MM): ')
    sala = input('Sala do evento: ')
    servicos = input('Digite os serviços (separados por vírgulas): ')

    db.adicionar_eventos(cliente_id, data, duracao, sala, servicos)
    print('EVENTO CADASTRADO COM SUCESSO!')


def mostrar_eventos(eventos):
    print('=====SEUS EVENTOS=====')
    for evento in eventos:
        print(f'ID: {evento[0]}')
        print(f'Data: {evento[1]}')
        print(f'Duração: {evento[2]}')
        print(f'Sala: {evento[3]}')
        print(f'Serviços: {evento[4]}')


def excluir_cliente_menu():
    clientes = db.listar_clientes()
    if not clientes:
        print('NENHUM CLIENTE CADASTRADO')
        return
    
    print('=====CLIENTES EXISTENTES=====')
    for cliente in clientes:
        print(f'ID: {cliente[0]}, Nome: {cliente[1]}, Senha: {cliente[2]}')

    cliente_id = int(input('ID do cliente que deseja excluir: '))
    confirm = input('S-sim/N-Não: ').strip().upper()

    if confirm == 'S':
        db.excluir_cliente(cliente_id)
        print('CLIENTE EXCLUÍDO COM SUCESSO!')
    else:
        print('OPERAÇÃO CANCELADA')


def menu_cliente(cliente_id, nome):
    os.system('cls' if os.name == 'nt' else 'clear')
    menu = f'''
    ==========|OLÁ, BEM VINDO {nome}|==========
    1 -> CADASTRAR NOVO EVENTO
    2 -> LISTAR EVENTOS EXISTENTES
    3 -> BUSCAR EVENTO PELO ID
    4 -> EXCLUIR EVENTO PELO ID
    0 -> VOLTAR PARA MENU INICIAL
    -> '''
    option = ut.obter_entrada(menu, 0, 4)

    while option != 0:

        if option == 1:
            cadastrar_evento(cliente_id)

        elif option == 2:
            eventos = db.listar_eventos(cliente_id)
            if eventos:
                mostrar_eventos(eventos)    
            else:
                print('SEM EVENTOS CADASTRADOS')

        elif option == 3:
            evento_id = int(input('ID do evento: '))
            evento = db.buscar_evento_por_id(cliente_id, evento_id)
            if evento:
                mostrar_eventos([evento])
            else:
                print('EVENTO NÃO ENCONTRADO!')

        elif option == 4:
            evento_id = int(input('ID DO EVENTO: '))
            confirm = input('DESEJA REALMENTE EXCLUIR ESTE EVENTO?(S/N): ').strip().upper()
            if confirm == 'S':
                db.excluir_evento(evento_id, cliente_id)
                print('EVENTO EXCLUÍDO COM SUCESSO!')
            else:
                print('OPERAÇÃO CANCELADA')

        input('Press ENTER to continue')
        os.system('cls' if os.name == 'nt' else 'clear')
        option = ut.obter_entrada(menu, 0, 4)


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    db.criar_tabelas()

    clientes = db.listar_clientes()
    if clientes:
        print('===CLIENTES EXISTENTES=====')
        for cliente in clientes:
            print(f'ID: {cliente[0]}, Nome: {cliente[1]}, Senha: {cliente[2]}')
    else:
        print('NENHUM CLIENTE CADASTRADO AINDA\n')

    entrada = '''
    ==========| RESERVA DE EVENTOS |==========

    1 -> CLIENTE JÁ EXISTENTE
    2 -> NOVO CLIENTE
    3 -> EXCLUIR CLIENTE
    0 -> SAIR
    -> '''
    option = ut.obter_entrada(entrada,0, 3)

    while option != 0:

        if option == 1:
            nome = input('Nome do cliente: ')
            senha = input(f'Senha de {nome}: ')
            cliente = db.buscar_clientes(nome, senha)

            if cliente:
                print(f'Olá {nome}!')
                menu_cliente(cliente[0], nome)
            else:
                print('CLIENTE NÃO CADASTRADO')

        elif option == 2:
            nome = input('Nome do cliente: ')
            senha = db.adicionar_cliente(nome)
            print(f'CLIENTE CADASTRADO COM SUCESSO! SENHA: {senha}')
            cliente = db.buscar_clientes(nome, senha)
            menu_cliente(cliente[0], nome)

        elif option == 3:
            excluir_cliente_menu()

        input('Press ENTER to continue')
        os.system('cls' if os.name == 'nt' else 'clear')
        option = ut.obter_entrada(entrada, 0, 3)

    print('ENCERRANDO...')
    

main()