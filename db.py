import sqlite3

connection = sqlite3.connect('DataBase.db')
cursor = connection.cursor()

# Criação das tabelas 

#Tabela de Usuários
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        accountLevel INT NOT NULL
    )            
""")

# Tabela Clientes
cursor.execute("""
    CREATE TABLE IF NOT EXISTS client (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        cnpj TEXT UNIQUE NOT NULL,
        address TEXT NOT NULL,
        cep TEXT NOT NULL
    )           
""")

# Tabela Chamados Abertos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS openTicket (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        defect TEXT NOT NULL,
        clientName TEXT NOT NULL
    )           
""")

# Tabela Chamados Fechados
cursor.execute("""
    CREATE TABLE IF NOT EXISTS closedTicket (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        defect TEXT NOT NULL,
        clientName TEXT NOT NULL
    )           
""")

connection.close()

# CRUD - Create, Read, Update, Delete

# Create
def registerUser(username, password, accountLevel):
    if username == "":
        print("\nYou need to enter an username.")
        return
    
    if password == "":
        print("\nYou need to enter a password.")
        return
    
    connection = sqlite3.connect('DataBase.db')
    cursor = connection.cursor()
    
    cursor.execute("""
        INSERT INTO user (username, password, accountLevel)
        VALUES (?, ?, ?)            
    """, (username, password, accountLevel))
    connection.commit()

    connection.close()

def registerClient(name, cnpj, address):
    # Casos da função
    if name == "":
        print("\nYou need to enter a name.")
        return
    
    if cnpj == "":
        print("\nYou need to enter a CNPJ.")
        return
    
    if address == "":
        print("\nYou need to enter an address.")
        return
    
    connection = sqlite3.connect('DataBase.db')
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO client (name, cnpj, address)
            VALUES (?, ?, ?)
        """, (name, cnpj, address))
        connection.commit()
        print("\nClient registered successfully!")
    except sqlite3.IntegrityError:
        print("\nError: Client already registered.")
    except Exception as e:
        print(f"\nError registering user: {e}")

    connection.close()

def openTicket(defect, name):
    if defect == "":
        print("\nYou need to enter a defect.")
        return
    
    if name == "":
        print("\nYou need to enter the name of the client.")
        return
    
    connection = sqlite3.connect('DataBase.db')
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO openTickets (defect, clientName)
            VALUES (?, ?, ?)
        """, (defect, name))
        connection.commit()
        print("\nTicket successfully open!")
    except sqlite3.IntegrityError:
        print("\nError: Ticket already open.")
    except Exception as e:
        print(f"\nError opening ticket: {e}")

    connection.close()

# Read
def showClients():
    connection = sqlite3.connect('DataBase.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM client")
    clients = cursor.fetchall()
    if clients:
        print("\nClients Registered:")
        for clients in clients:
            print(f"ID: {clients[0]}, Name: {clients[1]}, CNPJ: {clients[2]}, Address: {clients[3]}")
    else:
        print("\nNo clients registered.")

    connection.close()

def showOpenTickets():
    connection = sqlite3.connect('DataBase.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM openTicket")
    tickets = cursor.fetchall()
    if tickets:
        print("\nOpen Support Tickets:")
        for tickets in tickets:
            print(f"\nID: {tickets[0]} \nDefect: {tickets[1]} \nClient: {tickets[2]}")
    else:
        print("\nNo open tickets.")

    connection.close()

def showClosedTickets():
    connection = sqlite3.connect('DataBase.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM closedTicket")
    tickets = cursor.fetchall()
    if tickets:
        print("\nClosed Support Tickets:")
        for tickets in tickets:
            print(f"\nID: {tickets[0]} \nDefect: {tickets[1]} \nClient: {tickets[2]}")
    else:
        print("\nNo closed tickets.")

    connection.close()

# Update
def updateClient(name, cnpj, address, id):
    connection = sqlite3.connect('DataBase.db')
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE client
        SET name = ?, cnpj = ?, address = ?
        WHERE id = ?
    """, (name, cnpj, address, id))
    connection.commit()
    if cursor.rowcount > 0:
        print("Client updated with success!")
    else:
        print("Error: Client not found.")

    connection.close()

# Delete
def deleteClient(clientID):
    connection = sqlite3.connect('DataBase.db')
    cursor = connection.cursor()

    cursor.execute("DELETE FROM client WHERE id = ?", (clientID))

    connection.close()

def deleteUser(userID):
    connection = sqlite3.connect('DataBase.db')
    cursor = connection.cursor()

    cursor.execute("DELETE FROM user WHERE id = ?", (userID))

    connection.close()


# Default Users (Admin & Client)

# Admin
connection = sqlite3.connect('DataBase.db')
cursor = connection.cursor()

cursor.execute("""
    INSERT OR IGNORE INTO user (username, password, accountLevel)
    VALUES(?, ?, ?)
""", ("admin", 1234, 1))
connection.commit()

# Client
cursor.execute("""
    INSERT OR IGNORE INTO user (username, password, accountLevel)
    VALUES(?, ?, ?)
""", ("client", 1234, 0))
connection.commit()

# Default Clients
cursor.execute("""
    INSERT OR IGNORE INTO client (name, cnpj, address, cep)
    VALUES(?, ?, ?, ?)
""", ("Onyx Solution", "19.450.011/0001-00", "St. de Habitações Coletivas e Geminadas Norte 715 - Asa Norte, Brasília - DF", "70770-513"))
connection.commit()

cursor.execute("""
    INSERT OR IGNORE INTO client (name, cnpj, address, cep)
    VALUES(?, ?, ?, ?)
""", ("UniCEUB", "00.059.857/0001-87", "SEPN 707/907 - Asa Norte, Brasília-DF", "70790-075"))
connection.commit()

cursor.execute("""
    INSERT OR IGNORE INTO client (name, cnpj, address, cep)
    VALUES(?, ?, ?, ?)
""", ("Colégio Veritas", "54.045.157/0001-62", "AE, SEDB Instituo Israel Pinheiro Lote 2, Parte B - Lago Sul, Brasília - DF", "71676-010"))
connection.commit()

connection.close()