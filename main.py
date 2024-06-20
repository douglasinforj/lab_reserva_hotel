from controller.hotel_controller import HotelController
from view.hotel_view import HotelView

def main():
    hotel_controller = HotelController("Hotel Python")
    hotel_view = HotelView()

    while True:
        hotel_view.exibir_menu()
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            nome, cpf = hotel_view.obter_detalhes_cliente()
            hotel_controller.adicionar_cliente(nome, cpf)
            hotel_view.exibir_mensagem("Cliente adicionado com sucesso.")
        elif escolha == "2":
            numero, tipo, preco = hotel_view.obter_detalhes_quarto()
            hotel_controller.adicionar_quarto(numero, tipo, preco)
            hotel_view.exibir_mensagem("Quarto adicionado com sucesso.")
        elif escolha == "3":
            cpf_cliente, numero_quarto, data_checkin, data_checkout = hotel_view.obter_detalhes_reserva()
            try:
                hotel_controller.fazer_reserva(cpf_cliente, numero_quarto, data_checkin, data_checkout)
                hotel_view.exibir_mensagem("Reserva feita com sucesso.")
            except Exception as e:
                hotel_view.exibir_mensagem(str(e))
        elif escolha == "4":
            cpf_cliente, numero_quarto, data_checkin, data_checkout = hotel_view.obter_detalhes_reserva()
            try:
                hotel_controller.cancelar_reserva(cpf_cliente, numero_quarto, data_checkin, data_checkout)
                hotel_view.exibir_mensagem("Reserva cancelada com sucesso.")
            except Exception as e:
                hotel_view.exibir_mensagem(str(e))
        elif escolha == "5":
            hotel_controller.listar_reservas()
        elif escolha == "6":
            clientes = hotel_controller.listar_clientes()
            hotel_view.exibir_clientes(clientes)
        elif escolha == "0":
            break
        else:
            hotel_view.exibir_mensagem("Opção inválida, por favor tente novamente.")

if __name__ == "__main__":
    main()
