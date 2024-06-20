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
            print(f"Erro ao conetar ao MYSQL: {e}")
            return None



