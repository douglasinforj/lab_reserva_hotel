import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

class Hotel:
    def __init__(self, nome):
        self.nome = nome
        self.conexao = self.criar_conexao()
        self.criar_tabelas()

    def criar_conexao(self):
        try:
            conexao = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST'),
                database=os.getenv('MYSQL_DATABASE'),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD')
            )
            if conexao.is_connected():
                print("Conexão com o banco de dados MySQL foi bem sucedida!")
                return conexao
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None

    def criar_tabelas(self):
        cursor = self.conexao.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            cpf VARCHAR(14) NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Quartos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            numero INT NOT NULL,
            tipo VARCHAR(50) NOT NULL,
            preco DECIMAL(10, 2) NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reservas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cliente_id INT,
            quarto_id INT,
            data_checkin DATE NOT NULL,
            data_checkout DATE NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES Clientes(id),
            FOREIGN KEY (quarto_id) REFERENCES Quartos(id)
        )
        """)
        self.conexao.commit()

    def adicionar_cliente(self, cliente):
        cursor = self.conexao.cursor()
        cursor.execute("INSERT INTO Clientes (nome, cpf) VALUES (%s, %s)", (cliente.nome, cliente.cpf))
        self.conexao.commit()

    def adicionar_quarto(self, quarto):
        cursor = self.conexao.cursor()
        cursor.execute("INSERT INTO Quartos (numero, tipo, preco) VALUES (%s, %s, %s)", (quarto.numero, quarto.tipo, quarto.preco))
        self.conexao.commit()

    def verificar_disponibilidade(self, quarto_id, data_checkin, data_checkout):
        cursor = self.conexao.cursor()
        cursor.execute("""
        SELECT * FROM Reservas
        WHERE quarto_id = %s AND (%s < data_checkout AND %s > data_checkin)
        """, (quarto_id, data_checkin, data_checkout))
        resultado = cursor.fetchall()
        return len(resultado) == 0

    def fazer_reserva(self, cpf_cliente, numero_quarto, data_checkin, data_checkout):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT id FROM Clientes WHERE cpf = %s", (cpf_cliente,))
        cliente_id = cursor.fetchone()
        
        if cliente_id is None:
            raise Exception(f"Cliente com CPF {cpf_cliente} não encontrado.")
        
        cursor.execute("SELECT id FROM Quartos WHERE numero = %s", (numero_quarto,))
        quarto_id = cursor.fetchone()
        
        if quarto_id is None:
            raise Exception(f"Quarto com número {numero_quarto} não encontrado.")
        
        cursor.execute("""
            INSERT INTO Reservas (cliente_id, quarto_id, data_checkin, data_checkout)
            VALUES (%s, %s, %s, %s)
        """, (cliente_id[0], quarto_id[0], data_checkin, data_checkout))
        self.conexao.commit()

    def cancelar_reserva(self, cliente, quarto, data_checkin, data_checkout):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT id FROM Clientes WHERE cpf = %s", (cliente.cpf,))
        cliente_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM Quartos WHERE numero = %s", (quarto.numero,))
        quarto_id = cursor.fetchone()[0]

        cursor.execute("""
        DELETE FROM Reservas
        WHERE cliente_id = %s AND quarto_id = %s AND data_checkin = %s AND data_checkout = %s
        """, (cliente_id, quarto_id, data_checkin, data_checkout))
        self.conexao.commit()
        if cursor.rowcount > 0:
            print(f"Reserva cancelada para o cliente {cliente.nome} no quarto {quarto.numero} de {data_checkin} a {data_checkout}.")
        else:
            print(f"Reserva não encontrada para o cliente {cliente.nome} no quarto {quarto.numero} de {data_checkin} a {data_checkout}.")

    def listar_reservas(self):
        cursor = self.conexao.cursor()
        cursor.execute("""
        SELECT Clientes.nome, Quartos.numero, Reservas.data_checkin, Reservas.data_checkout
        FROM Reservas
        JOIN Clientes ON Reservas.cliente_id = Clientes.id
        JOIN Quartos ON Reservas.quarto_id = Quartos.id
        """)
        reservas = cursor.fetchall()
        if not reservas:
            print("\nNão há reservas.")
        for reserva in reservas:
            print(f"\nCliente: {reserva[0]}, Quarto: {reserva[1]}, Check-in: {reserva[2]}, Check-out: {reserva[3]}")

    def listar_clientes(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT nome, cpf FROM Clientes")
        clientes = cursor.fetchall()
        return clientes
