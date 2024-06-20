#criando class que será instanciadas no controller.py

class Reserva:
    def __init__(self, cliente, quarto, data_checkin, data_checkout):
        self.cliente = cliente
        self.data_checkin = data_checkin
        self.data_checkout = data_checkout