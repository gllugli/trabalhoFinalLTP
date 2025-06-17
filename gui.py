import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from db import registerUser
from db import deleteUser

connection = sqlite3.connect("DataBase.db")
cursor = connection.cursor()

# Begin of "Buttons Admin"
# Begin of "Users Windows"
def firstUserWindow():
    firstUserWindow = tk.Tk()
    firstUserWindow.title("User Section")
    firstUserWindow.geometry("600x400")

    # CRUD on TABLE user - Create, Read and Delete

    tk.Button(firstUserWindow, text="Show Users", command=showUsersWindow).pack(pady=10)
    tk.Button(firstUserWindow, text="Register User", command=registerUserWindow).pack(pady=10)
    tk.Button(firstUserWindow, text="Delete User", command=deleteUsersWindow).pack(pady=10)

    closeButton = tk.Button(firstUserWindow, text="Close", command=lambda:firstUserWindow.destroy())
    closeButton.pack()

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

    closeButton = tk.Button(showUsersWindow, text="Close", command=lambda:showUsersWindow.destroy())
    closeButton.pack()

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

    closeButton = tk.Button(registerUserWindow, text="Close", command=lambda:registerUserWindow.destroy)
    closeButton.pack(pady=10)

    registerUserWindow.mainloop()

def deleteUsersWindow():
    deleteUsersWindow = tk.Tk()
    deleteUsersWindow.title("Delete User")
    deleteUsersWindow.geometry("600x400")

    def on_click():
        userID = delete_entry.get()

        deleteUser(userID[0])
        messagebox.showinfo("Success", "User delete with success!") 

        deleteUsersWindow.destroy()


    tk.Label(deleteUsersWindow, text="Type the ID from the user that you want to delete").pack()

    delete_entry = tk.Entry(deleteUsersWindow, font=("Arial", 10), width=25)
    delete_entry.pack()

    deleteButton = tk.Button(deleteUsersWindow, text="Confirm", command=on_click)
    deleteButton.pack()

    deleteUsersWindow.mainloop()
# Fininsh of "Users Windows"

# Begin of "Clients Windows"
def showClientsWindow():
    clientsWindow = tk.Tk()
    clientsWindow.title("Clients")
    clientsWindow.geometry("800x600")

    tk.Label(clientsWindow, text=f"\nClients registered in the Data Base", font=("Arial", 16)).pack(pady=10)

    tree = ttk.Treeview(clientsWindow, columns=("ID", "Name", "CNPJ", "Address", "CEP"), show="headings")

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

    scrollbar = tk.Scrollbar(clientsWindow, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=scrollbar.set)
    tree.pack(expand=True, fill="both", padx=10, pady=10)
    scrollbar.pack(fill="x", padx=10)

    closeButton = tk.Button(clientsWindow, text="Close", command=lambda: clientsWindow.destroy())
    closeButton.pack()

    clientsWindow.mainloop()

# Begin of "Tickets Windows"
def showTicketsWindow():
    ticketWindow = tk.Tk()
    ticketWindow.title("Tickets")
    ticketWindow.geometry("600x400")

    tk.Label(ticketWindow, text=f"\nChoose an option:", font=("Arial", 16)).pack(pady=10)

    openTicketsButton = tk.Button(ticketWindow, text="Open Tickets")
    openTicketsButton.pack()

    closedTicketsButton = tk.Button(ticketWindow, text="Closed Tickets")
    closedTicketsButton.pack()

    closeButton = tk.Button(ticketWindow, text="Close", command=lambda: ticketWindow.destroy())
    closeButton.pack()

    ticketWindow.mainloop()
# End of "Tickets Windows"
#End of "Admin Buttons"

# Begin of "Admin and Client Windows"
def openAdminWindow(user):
    adminWindow = tk.Tk()
    adminWindow.title("Software - Admin Level")
    adminWindow.geometry("600x400")

    tk.Label(adminWindow, text=f"\nWelcome, {user}!", font=("Arial", 16)).pack(pady=10)

    # Buttons
    tk.Button(adminWindow, text="Users", command=firstUserWindow).pack(pady=10)
    tk.Button(adminWindow, text="Clients", command=showClientsWindow).pack(pady=10)
    tk.Button(adminWindow, text="Tickets", command=showTicketsWindow).pack(pady=10)

    adminWindow.mainloop()

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



