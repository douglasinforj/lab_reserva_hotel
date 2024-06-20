class HotelView:
    @staticmethod
    def exibir_menu():
        print("1. Adicionar Cliente")
        print("2. Adicionar Quarto")
        print("3. Fazer Reserva")
        print("4. Cancelar Reserva")
        print("5. Listar Reservas")
        print("6. Listar Clientes")
        print("0. Sair")

    @staticmethod
    def obter_detalhes_cliente():
        nome = input("Nome do cliente: ")
        cpf = input("CPF do cliente: ")
        return nome, cpf

    @staticmethod
    def obter_detalhes_quarto():
        numero = int(input("Número do quarto: "))
        tipo = input("Tipo do quarto: ")
        preco = float(input("Preço do quarto: "))
        return numero, tipo, preco

    @staticmethod
    def obter_detalhes_reserva():
        cpf_cliente = input("CPF do cliente: ")
        numero_quarto = int(input("Número do quarto: "))
        data_checkin = input("Data de check-in (YYYY-MM-DD): ")
        data_checkout = input("Data de check-out (YYYY-MM-DD): ")
        return cpf_cliente, numero_quarto, data_checkin, data_checkout

    @staticmethod
    def exibir_mensagem(mensagem):
        print(mensagem)

    @staticmethod
    def exibir_clientes(clientes):
        if not clientes:
            print("Nenhum cliente cadastrado.")
        else:
            print("Clientes cadastrados:")
            for cliente in clientes:
                print(f"Nome: {cliente[0]}, CPF: {cliente[1]}")
