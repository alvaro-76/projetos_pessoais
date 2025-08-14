import os, sqlite3

#config. do BD
conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

#cria tabela caso não haja
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    task TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")
conn.commit()


def get_create_user(username):
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if user:
        return user[0]
    cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
    conn.commit()
    return cursor.lastrowid


def get_tasks(user_id):
    cursor.execute('SELECT id, task FROM todos WHERE user_id= ?', (user_id,))
    return cursor.fetchall()


def add_task(user_id, task):
    cursor.execute('INSERT INTO todos (user_id, task) VALUES (?, ?)', (user_id, task))
    conn.commit()


def delete_task(task_id, user_id):
    cursor.execute('DELETE FROM todos WHERE id=? AND user_id=?', (task_id, user_id))
    conn.commit()

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    username = input('Informe seu user_name: ')
    user_id = get_create_user(username)

    print('='*60)
    menu = f'''
    ==========Lista de Tarefas==========
    Olá, {username}
    
    1 - Exibir lista
    2 - Adicionar item
    3 - Excluir item
    0 - Sair

    -> '''

    option = obter_entrada(menu, 0, 3)

    while option != 0:
        os.system('cls' if os.name == 'nt' else 'clear')

        if option == 1:
            exibir_lista(user_id)
        elif option == 3:
            excluir_item(user_id)
        elif option == 2:
            adicionar_item(user_id)
        
        input('\ncontinue...')
        os.system('cls' if os.name == 'nt' else 'clear')
        option = obter_entrada(menu, 0, 3)
    
    print('='*60)
    print('Encerrando...')


def adicionar_item(user_id):
    os.system('cls' if os.name == 'nt' else 'clear')
    item = input("Tarefa: ")
    add_task(user_id, item)


def excluir_item(user_id):
    tarefas = get_tasks(user_id)
    if not tarefas:
        print('Lista vazia')
        return
    exibir_lista(user_id)
    try:
        indice = obter_numero('Digite o ID da tarefa a ser excluida: ')
        delete_task(indice, user_id)
    except ValueError:
        print('INVALIDO')
            

def exibir_lista(user_id):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('='*60)
    tarefas = get_tasks(user_id)

    if not tarefas:
        print('Lista vazia')
    else:
        for tid, task in tarefas:
            print(f'{tid} -> {task}')


def obter_entrada(label, min, max):
    try:
        entrada = int(input(label))
        if entrada < min or entrada > max:
            print('INVALIDO')
            return obter_entrada(label, min, max)
    except ValueError:
        print('INVALIDO')
        return obter_entrada(label, min, max)
    
    return entrada


def obter_numero(label):
    try:
        num = int(input(label))
    except ValueError:
        print('INVALIDO')
        return obter_numero(label)
    
    return num


main()