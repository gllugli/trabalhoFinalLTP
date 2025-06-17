import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

connection = sqlite3.connect("DataBase.db")
cursor = connection.cursor()

#Funcions

def showUsersWindow():
    usersWindow = tk.Tk()
    usersWindow.title("Users")
    usersWindow.geometry("800x600")

    tk.Label(usersWindow, text=f"\nUsers registered in the Data Base", font=("Arial", 16)).pack(pady=10)

    tree = ttk.Treeview(usersWindow, columns=("ID", "Username", "Account Level"), show="headings")

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

    closeButton = tk.Button(usersWindow, text="Close", command=lambda: usersWindow.destroy())
    closeButton.pack()

    usersWindow.mainloop()

def showClientsWindow():
    clientsWindow = tk.Tk()
    clientsWindow.title("Clients")
    clientsWindow.geometry("800x600")

    tk.Label(clientsWindow, text=f"\nClients registered in the Data Base", font=("Arial", 16)).pack(pady=10)

    tree = ttk.Treeview(clientsWindow, columns=("ID", "Name", "CNPJ", "Address"), show="headings")

    # Definir os nomes das colunas
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("CNPJ", text="CNPJ")
    tree.heading("Address", text="Address")

    # Conectar ao banco de dados
    connection = sqlite3.connect("DataBase.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, cnpj, address FROM client")
    rows = cursor.fetchall()
    connection.close()

    # Inserir os dados na Treeview
    for row in rows:
        tree.insert("", tk.END, values=row)

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    closeButton = tk.Button(clientsWindow, text="Close", command=lambda: clientsWindow.destroy())
    closeButton.pack()

    clientsWindow.mainloop()

    
def openAdminWindow(user):
    adminWindow = tk.Tk()
    adminWindow.title("Software - Admin Level")
    adminWindow.geometry("600x400")

    tk.Label(adminWindow, text=f"\nWelcome, {user}!", font=("Arial", 16)).pack(pady=10)

    # Buttons
    tk.Button(adminWindow, text="Users", command=showUsersWindow).pack(pady=10)
    # tk.Button(adminWindow, text="Clients", command=).pack(pady=10)
    # tk.Button(adminWindow, text="Tickets", command=).pack(pady=10)



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

# Login Window
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



