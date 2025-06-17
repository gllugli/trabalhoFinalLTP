# Sistema para Chamados/Suporte técnico

import db as DataBase
import gui as Interface

print("+---------------------------------------------+")
print("|        Welcome to the Help Desk System      |")
print("+---------------------------------------------+")
print("|           1 - Register Client               |")
print("|           2 - Open Support Ticket           |")
print("|           3 - Show Open Support Tickets     |")
print("|           4 - Show Clients                  |")
print("+---------------------------------------------+")


option = int(input("\nChoose an option: "))

# Register Client
if option == 1:
    name = input("\nWhat is the client's name? ")
    cnpj = input("What is the client's CNPJ? ")
    address = input("What is the client's address? ")
    DataBase.registerClient(name, cnpj, address)

# Open Ticket
if option == 2:
    defect = input("\nWhat problem are you facing?")
    name = input("\nWhat is the client's name? ")
    DataBase.openTicket(defect, name)

# Show Open Tickets
if option == 3:
    DataBase.showOpenTickets()
    
# Show Clients
if option == 4:
    DataBase.showClients()