import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from db import registerUser
from db import deleteUser
from db import registerClient
from db import deleteClient
from db import updateClient
from db import openTicket

connection = sqlite3.connect("DataBase.db")
cursor = connection.cursor()

# Begin of "Login Window" 
def openLoginWindow():
    def verifyUser():
        username = entry_user.get()
        password = entry_password.get()

        # Verify if the username exists in the Data Base
        cursor.execute("SELECT 1 FROM user WHERE username=?", (username,))
        userExists = cursor.fetchone()

        if userExists:
            pass
        else:
            messagebox.showerror("Error", "User doesn't exists.")
            return
        
        # Verify the account level if the username exists
        cursor.execute("SELECT accountLevel FROM user WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        connection.close()

        if result:
            accountLevel = result[0]

            if accountLevel == 0: # Account Level = Client
                login.destroy()
                openClientWindow(username)
            elif accountLevel == 1: # Account Level = Admin
                login.destroy()
                openAdminWindow(username)
            else:
                messagebox.showerror("Error", "Username or password incorrect!")

    login = tk.Tk()
    login.title("Help Desk System")
    login.geometry("350x250")  

    loginText = tk.Label(login, text="Login", font=("Arial", 16))
    loginText.pack(pady=20)

    usernameText = tk.Label(login, text="Username", font="Arial")
    usernameText.pack()
    entry_user = tk.Entry(login, font=("Arial", 10), width=25)
    entry_user.pack(pady=(0, 10))

    passwordText = tk.Label(login, text="Passoword", font="Arial")
    passwordText.pack()
    entry_password = tk.Entry(login, show="*", font=("Arial", 10), width=25)
    entry_password.pack()

    loginButton = tk.Button(login, text="Enter", command=verifyUser, width=20)
    loginButton.pack(pady=10)

    login.mainloop()
# End of "Login Window"

# Begin of "Admin and Client Windows"
# Begin of "openAdminWindow"
def openAdminWindow(user):
    adminWindow = tk.Tk()
    adminWindow.title("Software - Admin Level")
    adminWindow.geometry("600x400")

    tk.Label(adminWindow, text=f"\nWelcome, {user}!", font=("Arial", 16)).pack(pady=10)

    # Buttons
    tk.Button(adminWindow, text="Users", command=firstUserWindow).pack(pady=10)
    tk.Button(adminWindow, text="Clients", command=firstClientWindow).pack(pady=10)
    tk.Button(adminWindow, text="Tickets", command=firstTicketWindow).pack(pady=10)

    adminWindow.mainloop()
# End of "openAdminWindow"

def openClientWindow(user):
    clientWindow = tk.Tk()
    clientWindow.title("Software - Client Level")
    clientWindow.geometry("600x400")

    tk.Label(clientWindow, text=f"\nWelcome, {user}!", font=("Arial", 16)).pack(pady=10)

    # Buttons
    # tk.Button(clientWindow, text="Users", command=).pack(pady=10)
    # tk.Button(clientWindow, text="Clients", command=).pack(pady=10)
    # tk.Button(clientWindow, text="Tickets", command=).pack(pady=10)

    clientWindow.mainloop()
# End of "Admin and Client Windows"

# Function to create the close button
def closeButton(windowName):
    closeButton = tk.Button(windowName, text="Close", command=windowName.destroy)
    closeButton.pack(pady=10)
    

# Begin of "Buttons Admin"
# Begin of "Users Windows"
def firstUserWindow():
    firstUserWindow = tk.Tk()
    firstUserWindow.title("User Section")
    firstUserWindow.geometry("600x400")

    tk.Button(firstUserWindow, text="Show Users", command=showUsersWindow).pack(pady=10)
    tk.Button(firstUserWindow, text="Register User", command=registerUserWindow).pack(pady=10)
    tk.Button(firstUserWindow, text="Delete User", command=deleteUsersWindow).pack(pady=10)

    closeButton(firstUserWindow)

    firstUserWindow.mainloop()


def showUsersWindow():
    showUsersWindow = tk.Tk()
    showUsersWindow.title("Users")
    showUsersWindow.geometry("800x600")

    tk.Label(showUsersWindow, text=f"\nUsers registered in the Data Base", font=("Arial", 16)).pack(pady=10)

    tree = ttk.Treeview(showUsersWindow, columns=("ID", "Username", "Account Level"), show="headings")

    # Definir os nomes das colunas
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Account Level", text="Level")

    # Conectar ao banco de dados
    connection = sqlite3.connect("DataBase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, username, accountLevel FROM user")
    rows = cursor.fetchall()
    connection.close()

    # Inserir os dados na Treeview
    for row in rows:
        tree.insert("", tk.END, values=row)

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    closeButton(showUsersWindow)

    showUsersWindow.mainloop()

def registerUserWindow():
    registerUserWindow = tk.Tk()
    registerUserWindow.title("Register User")
    registerUserWindow.geometry("600x400")

    # Informações para registrar - Username, password, account level

    tk.Label(registerUserWindow, text="Enter the following informations").pack()

    tk.Label(registerUserWindow, text="Username").pack()
    entry_username = tk.Entry(registerUserWindow, font=("Arial", 10), width=25)
    entry_username.pack()

    tk.Label(registerUserWindow, text="Password").pack()
    entry_password = tk.Entry(registerUserWindow, show="*",font=("Arial", 10), width=25)
    entry_password.pack()

    tk.Label(registerUserWindow, text="Account Level (0=User, 1=Admin)").pack()
    entry_accountLevel = tk.Entry(registerUserWindow, font=("Arial", 10), width=25)
    entry_accountLevel.pack()

    def on_click():
        username = entry_username.get()
        password = entry_password.get()
        accountLevel = entry_accountLevel.get()

        try:
            accountLevel = int(accountLevel)
        except ValueError:
            messagebox.showerror("Error", "Account Level must be an integer (0 or 1).")
            return

        registerUser(username, password, accountLevel)
        messagebox.showinfo("Success", "User registered with success!")

        registerUserWindow.destroy()

    registerButton = tk.Button(registerUserWindow, text="Register", command=on_click)
    registerButton.pack()

    closeButton(registerUserWindow)

    registerUserWindow.mainloop()


def deleteUsersWindow():
    deleteUsersWindow = tk.Tk()
    deleteUsersWindow.title("Delete User")
    deleteUsersWindow.geometry("600x400")

    def on_click():
        userID = delete_entry.get()

        deleteUser(userID)
        messagebox.showinfo("Success", "User delete with success!") 

        deleteUsersWindow.destroy()


    tk.Label(deleteUsersWindow, text="Type the ID from the user that you want to delete").pack()

    delete_entry = tk.Entry(deleteUsersWindow, font=("Arial", 10), width=25)
    delete_entry.pack()

    deleteButton = tk.Button(deleteUsersWindow, text="Confirm", command=on_click)
    deleteButton.pack()

    closeButton(deleteUsersWindow)

    deleteUsersWindow.mainloop()
# Fininsh of "Users Windows"

# Begin of "Clients Windows"
def firstClientWindow():
    firstClientWindow = tk.Tk()
    firstClientWindow.title("Clients")
    firstClientWindow.geometry("600x400")

    tk.Label(firstClientWindow, text="Choose an option:").pack(pady=10)

    # CRUD - CREATE, READ, UPDATE, DELETE 
    tk.Button(firstClientWindow, text="Show Clients", command=showClientsWindow).pack(pady=10)
    tk.Button(firstClientWindow, text="Register Client", command=registerClientWindow).pack(pady=10)
    tk.Button(firstClientWindow, text="Update Client Information", command=updateClientWindow).pack(pady=10)
    tk.Button(firstClientWindow, text="Delete Client", command=deleteClientWindow).pack(pady=10)

    closeButton(firstClientWindow)

    firstClientWindow.mainloop()

def showClientsWindow():
    showClientsWindow = tk.Tk()
    showClientsWindow.title("Clients")
    showClientsWindow.geometry("800x600")

    tk.Label(showClientsWindow, text=f"\nClients registered in the Data Base", font=("Arial", 16)).pack(pady=10)

    tree = ttk.Treeview(showClientsWindow, columns=("ID", "Name", "CNPJ", "Address", "CEP"), show="headings")

    # Definir os nomes das colunas
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("CNPJ", text="CNPJ")
    tree.heading("Address", text="Address")
    tree.heading("CEP", text="CEP")

    # Conectar ao banco de dados
    connection = sqlite3.connect("DataBase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, cnpj, address, cep FROM client")
    rows = cursor.fetchall()
    connection.close()

    # Inserir os dados na Treeview
    for row in rows:
        tree.insert("", tk.END, values=row)

    scrollbar = tk.Scrollbar(showClientsWindow, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=scrollbar.set)
    tree.pack(expand=True, fill="both", padx=10, pady=10)
    scrollbar.pack(fill="x", padx=10)

    closeButton(showClientsWindow)

    showClientsWindow.mainloop()

def registerClientWindow():
    registerClientWindow = tk.Tk()
    registerClientWindow.title("Register Client")
    registerClientWindow.geometry("600x400")

    informationText = tk.Label(registerClientWindow, text="Enter the client's information")
    informationText.pack()

    nameText = tk.Label(registerClientWindow, text="Name")
    nameText.pack()
    nameEntry = tk.Entry(registerClientWindow, font=("Arial", 16))
    nameEntry.pack()

    cnpjText = tk.Label(registerClientWindow, text="CNPJ")
    cnpjText.pack()
    cnpjEntry = tk.Entry(registerClientWindow, font=("Arial", 16))
    cnpjEntry.pack()

    addressText = tk.Label(registerClientWindow, text="Address")
    addressText.pack()
    addressEntry = tk.Entry(registerClientWindow, font=("Arial", 16))
    addressEntry.pack()

    cepText = tk.Label(registerClientWindow, text="CEP")
    cepText.pack()
    cepEntry = tk.Entry(registerClientWindow, font=("Arial", 16))
    cepEntry.pack()

    def onClick():
        name = nameEntry.get()
        cnpj = cnpjEntry.get()
        address = addressEntry.get()
        cep = cepEntry.get()

        registerClient(name, cnpj, address, cep)
        messagebox.showinfo("Success!", "The client has been registered")

        registerClientWindow.destroy()

    registerButton = tk.Button(registerClientWindow, text="Register", command=onClick)
    registerButton.pack()

    closeButton(registerClientWindow)

    registerClientWindow.mainloop()

def updateClientWindow():
    updateClientWindow = tk.Tk()
    updateClientWindow.title("Update Client")
    updateClientWindow.geometry("600x400")

    informationText = tk.Label(updateClientWindow, text="Enter the client's information")
    informationText.pack()

    idText = tk.Label(updateClientWindow, text="Client ID")
    idText.pack()
    idEntry = tk.Entry(updateClientWindow, font=("Arial", 12))
    idEntry.pack()

    nameText = tk.Label(updateClientWindow, text="Name")
    nameText.pack()
    nameEntry = tk.Entry(updateClientWindow, font=("Arial", 12))
    nameEntry.pack()

    cnpjText = tk.Label(updateClientWindow, text="CNPJ")
    cnpjText.pack()
    cnpjEntry = tk.Entry(updateClientWindow, font=("Arial", 12))
    cnpjEntry.pack()

    addressText = tk.Label(updateClientWindow, text="Address")
    addressText.pack()
    addressEntry = tk.Entry(updateClientWindow, font=("Arial", 12))
    addressEntry.pack()

    cepText = tk.Label(updateClientWindow, text="CEP")
    cepText.pack()
    cepEntry = tk.Entry(updateClientWindow, font=("Arial", 12))
    cepEntry.pack()

    def onClick(clientID, name, cnpj, address, cep):
        updateClient(name, cnpj, address, cep, clientID)
        messagebox.showinfo("Success!", "The client has been updated")

        updateClientWindow.destroy()

    confirmButton = tk.Button(updateClientWindow, text="Confirm", command=lambda:onClick(idEntry.get(), nameEntry.get(), cnpjEntry.get(), addressEntry.get(), cepEntry.get()))
    confirmButton.pack(pady=10)

    closeButton(updateClientWindow)

    updateClientWindow.mainloop()

def deleteClientWindow():
    deleteClientWindow = tk.Tk()
    deleteClientWindow.title("Delete Client")
    deleteClientWindow.geometry("600x400")

    informationText = tk.Label(deleteClientWindow, text="Type the ID from the client that you want to delete")
    informationText.pack()

    userIdEntry = tk.Entry(deleteClientWindow, font=("Arial", 16))
    userIdEntry.pack()

    def onClick(clientID):
        deleteClient(clientID)
        messagebox.showinfo("Success", "The Client has been deleted")

        deleteClientWindow.destroy()

    deleteButton = tk.Button(deleteClientWindow, text="Confirm", command=lambda:onClick(userIdEntry.get()))
    deleteButton.pack(pady=10)

    closeButton(deleteClientWindow)

    deleteClientWindow.mainloop()

# Begin of "Tickets Windows"
def firstTicketWindow():
    firstTicketWindow = tk.Tk()
    firstTicketWindow.title("Ticket")
    firstTicketWindow.geometry("600x400")

    ticketInformation = tk.Label(firstTicketWindow, text="Choose an option:")
    ticketInformation.pack(pady=10)

    # CRUD - CREATE, READ, DELETE
    showTicketsButton = tk.Button(firstTicketWindow, text="Show Tickets", command=ticketWindow)
    showTicketsButton.pack(pady=10)
    createTicketButton = tk.Button(firstTicketWindow, text="Create Ticket", command=createTicketWindow)
    createTicketButton.pack(pady=10)
    deleteTicketButton = tk.Button(firstTicketWindow, text="Delete Ticket", command=deleteTicketWindow)
    deleteTicketButton.pack(pady=10)

    firstTicketWindow.mainloop()

# Begin of "ticketWindow"
def ticketWindow():
    ticketWindow = tk.Tk()
    ticketWindow.title("Tickets")
    ticketWindow.geometry("600x400")

    tk.Label(ticketWindow, text="\nChoose an option:", font=("Arial", 16)).pack(pady=10)

    openTicketsButton = tk.Button(ticketWindow, text="Open Tickets", command=showOpenTickets)
    openTicketsButton.pack(pady=10)

    closedTicketsButton = tk.Button(ticketWindow, text="Closed Tickets", command=showClosedTickets)
    closedTicketsButton.pack(pady=10)

    closeButton(ticketWindow)

    ticketWindow.mainloop()
# End of "ticketWindow"

def showOpenTickets():
    showOpenTickets = tk.Tk()
    showOpenTickets.title("Open Tickets")
    showOpenTickets.geometry("600x400")

    openTicketsInformation = tk.Label(showOpenTickets, text="These are the tickets that are open on the Data Base")
    openTicketsInformation.pack(pady=10)

    tree = ttk.Treeview(showOpenTickets, columns=("ID", "Client Name", "Defect"), show="headings")

    tree.heading("ID", text="ID")
    tree.heading("Client Name", text="Client Name")
    tree.heading("Defect", text="Defect")

    connection = sqlite3.connect("DataBase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, clientName, defect FROM openTicket")
    rows = cursor.fetchall()
    connection.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

    scrollbar = tk.Scrollbar(showOpenTickets, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=scrollbar.set)
    tree.pack(expand=True, fill="both", padx=10, pady=10)
    scrollbar.pack(fill="x", padx=10)    

    showOpenTickets.mainloop()

def showClosedTickets():
    showClosedTickets = tk.Tk()
    showClosedTickets.title("Closed Tickets")
    showClosedTickets.geometry("600x400")

    closedTicketsInformation = tk.Label(showClosedTickets, text="These are the tickets that are closed on the Data Base")
    closedTicketsInformation.pack(pady=10)

    tree = ttk.Treeview(showClosedTickets, columns=("ID", "Client Name", "Defect"), show="headings")

    tree.heading("ID", text="ID")
    tree.heading("Client Name", text="Client Name")
    tree.heading("Defect", text="Defect")

    connection = sqlite3.connect("DataBase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, clientName, defect FROM closedTicket")
    rows = cursor.fetchall()
    connection.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

    scrollbar = tk.Scrollbar(showClosedTickets, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=scrollbar.set)
    tree.pack(expand=True, fill="both", padx=10, pady=10)
    scrollbar.pack(fill="x", padx=10) 

    showClosedTickets.mainloop()

def createTicketWindow():
    createTicketWindow = tk.Tk()
    createTicketWindow.title("Create Ticket")
    createTicketWindow.geometry("600x400")

    createInformation = tk.Label(createTicketWindow, text="Type the following informations:")
    createInformation.pack(pady=10)

    clientName = tk.Label(createTicketWindow, text="Client Name")
    clientName.pack(pady=10)
    clientNameEntry = tk.Entry(createTicketWindow, font=("Arial", 12))
    clientNameEntry.pack(pady=10)

    defect = tk.Label(createTicketWindow, text="Defect")
    defect.pack(pady=10)
    defectNameEntry = tk.Entry(createTicketWindow, font=("Arial", 12))
    defectNameEntry.pack(pady=10)

    def onClick(name, defect):
        clientName = name
        ticketDefect = defect

        openTicket(name, defect)

        messagebox.showinfo("Success!", "Ticket opened successfully")
        createTicketWindow.destroy()

    registerButton = tk.Button(createTicketWindow, text="Register", command=lambda:onClick(clientNameEntry.get(), defectNameEntry.get()))
    registerButton.pack(pady=10)

    createTicketWindow.mainloop()

def deleteTicketWindow():
    deleteTicketWindow = tk.Tk()
    deleteTicketWindow.title("Delete Ticket")
    deleteTicketWindow.geometry("600x400")

    def onClick(ticketIDEntry):
        ticketID = ticketIDEntry

        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM closedTicket WHERE id = ?", (ticketID,))
        connection.commit()

        connection.close()

        messagebox.showinfo("Success!", "Ticket deleted successfully")
        deleteTicketWindow.destroy()

    deleteInformation = tk.Label(deleteTicketWindow, text="Enter the Ticket ID")
    deleteInformation.pack(pady=10)

    ticketIdEntry = tk.Entry(deleteTicketWindow, font=("Arial", 12))
    ticketIdEntry.pack(pady=10)

    deleteButton = tk.Button(deleteTicketWindow, text="Confirm", command=lambda:onClick(ticketIdEntry.get()))
    deleteButton.pack(pady=10)

    deleteTicketWindow.mainloop()
#End of "Admin Buttons"