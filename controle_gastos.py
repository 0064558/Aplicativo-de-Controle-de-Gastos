import sqlite3
from datetime import datetime

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Criação da tabela de despesas, caso ainda não exista
cursor.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL
)
''')

# Função para adicionar uma despesa
def add_expense(amount, category, description):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO expenses (amount, category, description, date) 
        VALUES (?, ?, ?, ?)
    ''', (amount, category, description, date))
    conn.commit()
    print("Despesa adicionada com sucesso.")

# Função para listar todas as despesas
def list_expenses():
    cursor.execute('SELECT * FROM expenses')
    rows = cursor.fetchall()
    if rows:
        print("\n--- Lista de Despesas ---")
        for row in rows:
            print(f"ID: {row[0]}, Valor: R${row[1]:.2f}, Categoria: {row[2]}, Descrição: {row[3]}, Data: {row[4]}")
    else:
        print("\nNenhuma despesa registrada.")
    
# Função para listar despesas por categoria
def list_expenses_by_category(category):
    cursor.execute('SELECT * FROM expenses WHERE category = ?', (category,))
    rows = cursor.fetchall()
    if rows:
        print(f"\n--- Despesas na Categoria '{category}' ---")
        for row in rows:
            print(f"ID: {row[0]}, Valor: R${row[1]:.2f}, Descrição: {row[3]}, Data: {row[4]}")
    else:
        print(f"\nNenhuma despesa encontrada para a categoria '{category}'.")

# Função para remover uma despesa pelo ID
def remove_expense(expense_id):
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    if cursor.rowcount > 0:
        print(f"Despesa com ID {expense_id} removida com sucesso.")
    else:
        print(f"Nenhuma despesa encontrada com ID {expense_id}.")

# Função para gerar relatório de gastos por categoria
def generate_report():
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    rows = cursor.fetchall()
    if rows:
        print("\n--- Relatório de Gastos por Categoria ---")
        for row in rows:
            print(f"Categoria: {row[0]}, Total Gasto: R${row[1]:.2f}")
    else:
        print("Nenhuma despesa registrada.")

# Função para exibir o menu e interagir com o usuário
def show_menu():
    while True:
        print("\nControle de Gastos")
        print("1. Adicionar Despesa")
        print("2. Listar Todas as Despesas")
        print("3. Listar Despesas por Categoria")
        print("4. Remover Despesa")
        print("5. Gerar Relatório de Gastos por Categoria")
        print("6. Sair")
        
        choice = input("Escolha uma opção: ")

        if choice == '1':
            try:
                amount = float(input("Digite o valor da despesa: R$"))
                category = input("Digite a categoria: ")
                description = input("Digite a descrição (opcional): ")
                add_expense(amount, category, description)
            except ValueError:
                print("Erro: O valor da despesa deve ser um número.")

        elif choice == '2':
            list_expenses()

        elif choice == '3':
            category = input("Digite a categoria: ")
            list_expenses_by_category(category)

        elif choice == '4':
            try:
                expense_id = int(input("Digite o ID da despesa que deseja remover: "))
                remove_expense(expense_id)
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")
        
        elif choice == '5':
            generate_report()

        elif choice == '6':
            print("Saindo do aplicativo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

# Rodar o menu
show_menu()

# Fechar a conexão com o banco de dados ao finalizar
conn.close()
