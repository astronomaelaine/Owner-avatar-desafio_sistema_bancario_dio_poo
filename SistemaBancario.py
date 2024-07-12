from datetime import datetime
from abc import ABC, abstractproperty, abstractclassmethod


class Historico():
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo":transacao.__class__.__name__, #Saque ou Deposito (pega o nome da classe)
                "valor": transacao.valor,
                "data":datetime.now()
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    @abstractclassmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor_deposito = valor

    @property
    def valor(self):
        return self.valor_deposito

    def registrar(self, conta):
        if(conta.depositar(self.valor_deposito)):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor_saque = valor
    @property
    def valor(self):
        return self.valor_saque

    def registrar(self, conta):
        if(conta.sacar(self.valor_saque)):
            conta.historico.adicionar_transacao(self)

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


    def __str__(self):
        return f"""\
            Enderecoo:\t{self.endereco}
            CPF:\t\t{self.cpf}
            Nome:\t{self.nome}
            data_nascimento:\t{self.data_nascimento}
        """


class Conta():
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):
        if (self._saldo < valor):
            print(f""" Você não possui saldo suficente para esta operação. 
                    Saldo em conta: R$ {self._saldo:.2f}
                    Valor retirada: R$ {valor:.2f}
                    """)
        elif (valor > 0):
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n=== Operacao Falhou! ===")

        return False
    def depositar(self, valor):
        if(valor > 0):
            self._saldo += valor
            print("\n=== Deposito realizado com sucesso! ===")
            return True

        else:
            print("""Operação Inválida!
                    Não é possível realizar depósitos de valores negativos.
                """)

        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite;
        self._limite_saques = limite_saques;

    def sacar(self, valor):
        numero_saques = len( [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        if (valor > self._limite):
            print(f""" Operação Inválida! 
                            O valor limite para saque é de R${self._limite}.
                            """)
            return False

        elif (numero_saques >= self._limite_saques):
            print(f""" Operacao Invalida! 
                                Você já  realizou os {self._limite_saques} saques permitidos hoje.
                                """)
            return False

        else:
            return super().sacar(valor)

    @property
    def limite(self):
        return self._limite

    def __str__(self):
        return f"""\
            Agencia:\t{self.agencia}
            Numero da Conta:\t\t{self.numero}
            Cliente:\t{self.cliente}
        """

def sacar(lista_clientes):

    cpf = input("Informe o CPF do cliente: ")
    cliente = busca_cliente(cpf, lista_clientes)

    if not cliente:
        print("\nCliente não localizado.")
        return
    valor_saque = int(input("Informe o valor que deseja sacar: "))
    transacao = Saque(valor_saque)

    conta = busca_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def busca_cliente(doc, lista_clientes):
    clientes_filtrados = [cliente for cliente in lista_clientes if cliente.cpf == doc]
    return clientes_filtrados[0] if clientes_filtrados else None

def busca_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente sem conta cadastrada. Adicione uma conta para ele")
        return

    return cliente.contas[0]
def depositar(lista_clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = busca_cliente(cpf, lista_clientes)

    if not cliente:
        print("\nCliente não localizado.")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = busca_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(lista_clientes):

    cpf = input("Digite o cpf do usuario: ")

    cliente = busca_cliente(cpf, lista_clientes)

    if not cliente:
        print("\n Cliente não localizado.\n")
        return

    conta = busca_conta_cliente(cliente)
    print("\n ------------------- Extrato ------------------- \n")

    movimentacoes = conta.historico.transacoes

    if not movimentacoes:
        print("\n Não foram realizadas movimentações na conta.\n")

    else:
        for transacao in movimentacoes:
            print(f"""\
                {transacao['tipo']}:\tR$ {transacao['valor']:.2f}
            """)

    print(f"\n Saldo em conta: R$ {conta.saldo:.2f}")
    print("\n ----------------------------------------------- \n")

def criar_usuario(lista_clientes):

    print("\n ------------------- CADASTRO DE USUARIO ------------------- \n")
    cpf = input("Digite o cpf do usuario: ")

    cliente = busca_cliente(cpf, lista_clientes)

    if(cliente):
        print(f"\nOps! Já existe usuário com o CPF {cpf}!")
        print(f"\nRetornando ao menu inicial...")
        return

    nome = input("Digite o nome do usuario: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(endereco, cpf, nome, data_nascimento)

    lista_clientes.append(cliente)

    print("\n Usuário cadastrado com sucesso!")
    print("\n -------------------*****------------------- \n")

def listar_usuarios(lista_usuarios):

    print("\n Lista de usuarios do sistema!")
    print("*********************************************************")
    for cliente in lista_usuarios:
        print(cliente.__str__())
        for conta in cliente.contas:
            print(f"""\
            Agencia:\t{conta.agencia}
            Numero da Conta:\t\t{conta.numero}
        """)
        print("*********************************************************")


def criar_conta(numero_conta, lista_usuarios, lista_contas):

    print("\n ------------------- CADASTRO DE CONTA ------------------- \n")

    cpf = input("\nDigite o CPF do cliente: ")
    cliente = busca_cliente(cpf, lista_usuarios)

    if(cliente):
        print("Cliente localizado")
        conta = ContaCorrente.nova_conta(cliente, numero_conta)
        lista_contas.append(conta)
        cliente.contas.append(conta)
        print("\n Conta cadastrada com sucesso!")
        print("\n -------------------*****------------------- \n")

    else:
        print("Não foi possível localizar um cliente com essa conta.")
        print("\nPor favor, tente novamente.")
        return

def listar_contas(lista_contas):

    print("\n Lista de contas do sistema!")
    print("*********************************************************")
    for conta in lista_contas:
        print(conta.__str__())
        print("*********************************************************")
def menu():
    menu = """
    ***************** MENU *****************
    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    
    [u]  Novo Usuario
    [lu] Lista Usuarios
    
    [c]  Nova Conta
    [lc] Lista Contas
    
    [q]  Sair
    
    ::> """

    return menu
def main():

    lista_clientes = []
    lista_contas = []

    while True:
        opcao = input(menu())

        if (opcao == "d"):
            print("Deposito")
            depositar(lista_clientes)


        elif (opcao == "s"):
            print("Saque")


            sacar(lista_clientes)


        elif (opcao == "e"):
            print("Extrato")
            exibir_extrato(lista_clientes)

        elif (opcao == "u"):
            print("Novo usuario")
            criar_usuario(lista_clientes)


        elif (opcao == "lu"):
            print("Lista de Usuarios")

            if not lista_clientes:
                print("Não há usuários cadastrados.")
                print("Retornando ao menu")
            else:
                listar_usuarios(lista_clientes)

        elif (opcao == "c"):
            print("Nova Conta")
            num_conta= len(lista_contas)+1
            criar_conta(num_conta,lista_clientes, lista_contas)


        elif (opcao == "lc"):
            print("Lista Contas")

            if not lista_contas:
                print("Não há contas cadastrados.")
                print("Retornando ao menu")
            else:
                listar_contas(lista_contas)

        elif (opcao == "q"):
            print("SAIR")
            exit()

        else:
            print("Opcao invalida.")


main()