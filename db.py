import sqlite3

conexao = sqlite3.connect('Cliente.db')
cursor = conexao.cursor()

# Criação das tabelas 

# Tabela Clientes
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        cnpj TEXT UNIQUE NOT NULL,
        endereco TEXT NOT NULL
    )           
""")

# Tabela Chamados Abertos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS chamadosAbertos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        defeito TEXT NOT NULL,
        nomeCliente TEXT NOT NULL
    )           
""")

# Tabela Chamados Fechados
cursor.execute("""
    CREATE TABLE IF NOT EXISTS chamadosFechados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        defeito TEXT NOT NULL,
        nomeCliente TEXT NOT NULL
    )           
""")

# Funções CRUD - Create, Read, Update, Delete

# Create
def cadastrarCliente(nome, cnpj, endereco):
    # Casos da função
    if nome == "":
        print("\nVocê precisa inserir um nome.")
        return
    
    if cnpj == "":
        print("\nVocê precisa inserir um CNPJ.")
        return
    
    if endereco == "":
        print("\nVocê precisa inserir um endereço.")
        return
    
    try:
        cursor.execute("""
            INSERT INTO produtos (nome, cnpj, endereco)
            VALUES (?, ?, ?)
        """, (nome, cnpj, endereco))
        conexao.commit()
        print("\nProduto cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("\nErro: Produto já cadastrado.")
    except Exception as e:
        print(f"\nErro ao cadastrar cliente: {e}")

def abrirChamado(defeito, nome):

    if defeito == "":
        print("\nÉ necessário entrar com o defeito.")
        return
    
    if nome == "":
        print("\nÉ necessário entrar com o nome do cliente.")
        return
    
    try:
        cursor.execute("""
            INSERT INTO chamadosAbertos (defeito, nomeCleinte)
            VALUES (?, ?, ?)
        """, (defeito, nome))
        conexao.commit()
        print("\nChamado aberto com sucesso!")
    except sqlite3.IntegrityError:
        print("\nErro: Chamdo já aberto.")
    except Exception as e:
        print(f"\nErro ao abrir chamado: {e}")

# Read
def mostrarClientes():
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    if clientes:
        print("\nClientes cadastrados:")
        for clientes in clientes:
            print(f"ID: {clientes[0]}, Nome: {clientes[1]}, CNPJ: {clientes[2]}, Endereço: {clientes[3]}")
    else:
        print("\nNenhum cliente cadastrado.")

def mostrarChamadosAbertos():
    cursor.execute("SELECT * FROM chamadosAbertos")
    chamados = cursor.fetchall()
    if chamados:
        print("\nClientes cadastrados:")
        for chamados in chamados:
            print(f"\nID: {chamados[0]} \nDefeito: {chamados[1]} \nCliente: {chamados[2]}")
    else:
        print("\nNenhum chamado abertos.")

def mostrarChamadosFechados():
    cursor.execute("SELECT * FROM chamadosFechados")
    chamados = cursor.fetchall()
    if chamados:
        print("\nChamados Fechados:")
        for chamados in chamados:
            print(f"\nID: {chamados[0]} \nDefeito: {chamados[1]} \nCliente: {chamados[2]}")
    else:
        print("\nNenhum chamado fechado.")

# Update
def atualizarCliente(nome, cnpj, endereco, id):
    cursor.execute("""
        UPDATE cliente
        SET nome = ?, cnpf = ?, endereco = ?
        WHERE id = ?
    """, (nome, cnpj, endereco, id))
    conexao.commit()
    if cursor.rowcount > 0:
        print("Cliente atualizado com sucesso!")
    else:
        print("Erro: Cliente não encontrado.")

# Delete
def deletar_produto(id):
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id))

