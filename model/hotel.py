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
                print("Conexão com o banco de dados MYSQL foi bem Sucedida!")
                return conexao
        except Error as e:
            print(f"Erro ao conectar ao MYSQL: {e}")
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

# instanciando a Class para teste (Testando o codigo $python hotel.py)
#hotel = Hotel("Hotel Exemplo")

# Criando as funções para manipulação no banco de dados, dados vindos do hotel_controller.py

        def adicionar_cliente(self, cliente):
            cursor = self.conexao.cursor()
            cursor.execute("INSERT INTO Clientes (nome, cpf) VALUES (%s, %s)", (cliente.nome, cliente.cpf))
            self.conexao.commit()
        
        def adicionar_quarto(self, quarto):
            cursor = self.conexao.cursor()
            cursor.execute("INSERT INTO Quartos (numero, tipo, preco) VALUES (%s, %s, %s)", (quarto.numero, quarto.tipo, quarto.preco))
            self.conexao.commit()

        def verificar_disponibilidade(self, quarto_id, data_checkin, data_chekout):
            cursor = self.conexao.cursor()
            cursor.exceute("""
            SELECT * FROM Reservas
            WHERE quarto_id = %s AND (%s < data_checkout AND %s > data_checkin)
            """, (quarto_id, data_checkin, data_chekout))
            resultado = cursor.fetchall()
            return len(resultado) == 0
        
        def fazer_reserva(self, cliente, quarto, data_checkin, data_checkout):
            cursor = self.conexao.cursor()
            cursor.execute("SELECT id FROM Clientes WHERE cpf = %s", (cliente.cpf,))
            cliente_id = cursor.fetchone()[0]
            cursor.excute("SELECT id FROM Quartos WHERE numer = %s", (quarto.numero,))
            quarto_id = cursor.fetchone()[0]

            if self.verificar_disponibilidade(quarto_id, data_checkin, data_checkout):
                cursor.execute("""
                INSERT INTO Reservas (cliente_id, quarto_id, data_checkin, data_checkout)
                VALUES (%s, %s, %s, %s)
                """, (cliente_id, quarto_id, data_checkin, data_checkout))
                self.conexao.commit()
                print(f"Reserva feita para o cliente {cliente.nome} no quarto {quarto.numero} de {data_checkin} a {data_checkout}")
            else:
                print(f"Quarto {quarto.numero} não está disponivel de {data_checkin} a {data_checkout}.")
        
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
                print("Não há reservas.")
            for reserva in reservas:
                print(f"Cliente: {reserva[0]}, Quarto: {reserva[1]}, Check-in: {reserva[2]}, Check-out: {reserva[3]}")
        

