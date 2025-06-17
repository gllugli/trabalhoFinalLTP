import sqlite3

connection = sqlite3.connect('DataBase.db')
cursor = connection.cursor()

# Criação das tabelas 

# Tabela Clientes
cursor.execute("""
    CREATE TABLE IF NOT EXISTS client (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        cnpj TEXT UNIQUE NOT NULL,
        address TEXT NOT NULL
    )           
""")

# Tabela Chamados Abertos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS openTickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        defect TEXT NOT NULL,
        clientName TEXT NOT NULL
    )           
""")

# Tabela Chamados Fechados
cursor.execute("""
    CREATE TABLE IF NOT EXISTS closedTickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        defect TEXT NOT NULL,
        clientName TEXT NOT NULL
    )           
""")

# CRUD - Create, Read, Update, Delete

# Create
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

def openTicket(defect, name):

    if defect == "":
        print("\nYou need to enter a defect.")
        return
    
    if name == "":
        print("\nYou need to enter the name of the client.")
        return
    
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

# Read
def showClients():
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    if clients:
        print("\nClients Registered:")
        for clients in clients:
            print(f"ID: {clients[0]}, Name: {clients[1]}, CNPJ: {clients[2]}, Address: {clients[3]}")
    else:
        print("\nNo clients registered.")

def showOpenTickets():
    cursor.execute("SELECT * FROM openTickets")
    tickets = cursor.fetchall()
    if tickets:
        print("\nOpen Support Tickets:")
        for tickets in tickets:
            print(f"\nID: {tickets[0]} \nDefect: {tickets[1]} \nClient: {tickets[2]}")
    else:
        print("\nNo open tickets.")

def showClosedTickets():
    cursor.execute("SELECT * FROM closedTickets")
    tickets = cursor.fetchall()
    if tickets:
        print("\nClosed Support Tickets:")
        for tickets in tickets:
            print(f"\nID: {tickets[0]} \nDefect: {tickets[1]} \nClient: {tickets[2]}")
    else:
        print("\nNo closed tickets.")

# Update
def updateClient(name, cnpj, address, id):
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

# Delete
def deleteClient(id):
    cursor.execute("DELETE FROM client WHERE id = ?", (id))

