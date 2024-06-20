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

# instanciando a Class para teste
hotel = Hotel("Hotel Exemplo")
