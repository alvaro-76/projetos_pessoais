import sqlite3, random

DB_NAME = "agendamento.db"

def conectar():
    return sqlite3.connect(DB_NAME)


def buscar_evento_por_id(cliente_id, evento_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM eventos WHERE cliente_id=? AND id=?",
        (cliente_id, evento_id)
    )
    evento = cursor.fetchone()
    conn.close()
    return evento


def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, senha FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes


def criar_tabelas():
    conn = conectar()
    
    cursor = conn.cursor()

    #TABELA CLIENTES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    #TABELA EVENTOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        duracao TEXT NOT NULL,
        sala TEXT NOT NULL,
        servicos TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    )
""")
    
    conn.commit()
    conn.close()
    print('Tabelas criadas com sucesso!')


def adicionar_cliente(nome):
    conn = conectar()
    cursor = conn.cursor()

    senha = str(random.randint(100000, 999999))

    cursor.execute("INSERT INTO clientes (nome, senha) VALUES (?, ?)", (nome, senha))
    conn.commit()
    conn.close()
    return senha


def buscar_clientes(nome, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE nome=? AND senha=?", (nome, senha))
    cliente = cursor.fetchone()
    conn.close()
    return cliente


def adicionar_eventos(cliente_id, data, duracao, sala, servicos):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO eventos (cliente_id, data, duracao, sala, servicos) VALUES (?, ?, ?, ?, ?)",
        (cliente_id, data, duracao, sala, servicos)
    )
    conn.commit()
    conn.close()


def listar_eventos(clientes_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM eventos WHERE cliente_id=?", (clientes_id,))
    eventos = cursor.fetchall()
    conn.close()
    return eventos


def excluir_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM eventos WHERE cliente_id=?", (cliente_id,))
    cursor.execute("DELETE FROM clienteS WHERE id=?", (cliente_id,))

    conn.commit()
    conn.close()


def excluir_evento(evento_id, cliente_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM eventos WHERE id=? AND cliente_id=?", (evento_id, cliente_id))

    conn.commit()
    conn.close()
