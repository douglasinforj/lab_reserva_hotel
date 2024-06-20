#Importando as Classes dos arquivos de model para instanciação

from model.cliente import Cliente
from model.quarto import Quarto
from model.hotel import Hotel

class HotelController:
    def __init__(self, nome):
        self.hotel = Hotel(nome)                   # instanciando a classe Hotel do hotel.py para objeto hotel, na classe construtora
    
    def adicionar_cliente(self, nome, cpf):        #função recebe parametros
        cliente = Cliente(nome, cpf)               #instanciando a classe para objeto cliente
        self.hotel.adicionar_cliente(cliente)      #chamando a função adicionar_cliente da classe Hotel instanciada para o objeto hotel, injetando como parametro cliente

    def adicionar_quarto(self, numero, tipo, preco):
        quarto = Quarto(numero, tipo, preco)
        self.hotel.adicionar_quarto(quarto)

    def fazer_reserva(self, cpf_cliente, numero_quarto, data_checkin, data_checkout):
        cliente = self.obter_cliente_por_cpf(cpf_cliente)
        quarto = self.obter_quarto_por_numero(numero_quarto)
        self.hotel.fazer_reserva(cpf_cliente, numero_quarto, data_checkin, data_checkout)
    
    def fazer_reserva(self, cpf_cliente, numero_quarto, data_checkin, data_checkout):
        cliente = self.obter_cliente_por_cpf(cpf_cliente)
        quarto = self.obter_quarto_por_numero(numero_quarto)
        self.hotel.fazer_reserva(cpf_cliente, numero_quarto, data_checkin, data_checkout)
        

    def listar_reservas(self):
        self.hotel.listar_reservas()

    def obter_cliente_por_cpf(self, cpf):
        cursor = self.hotel.conexao.cursor()
        cursor.execute("SELECT nome, cpf FROM Clientes WHERE cpf = %s", (cpf,))
        resultado = cursor.fetchone()
        if resultado:
             return Cliente(resultado[0], resultado[1])
        else:
            raise Exception(f'Cliente com CPF {cpf} não encontrado')

    def obter_quarto_por_numero(self, numero):
        cursor = self.hotel.conexao.cursor()
        cursor.execute("SELECT numero, tipo, preco FROM Quartos WHERE numero = %s", (numero,))
        resultado = cursor.fetchone()
        if resultado:
            return Quarto(resultado[0], resultado[1], resultado[2])
        else:
            raise Exception(f'Quarto com número {numero} não encontrado')
        
    def listar_clientes(self):
        clientes = self.hotel.listar_clientes()
        return clientes
    
    def verificar_disponibilidade(self, numero_quarto, data_chekin, data_checkout):
        quarto = self.obter_quarto_por_numero(numero_quarto)
        return self.hotel.verificar_disponibilidade(quarto['id'], data_chekin, data_checkout)