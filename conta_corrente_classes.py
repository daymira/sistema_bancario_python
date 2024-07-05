from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

ROOT_PATH = Path(__file__).parent


# iterar sobre todas contas do banco e retornar informações básicas como nome, conta, saldo atual
class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self._start = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._start]
            return f"""
            Agência:\t{conta.agencia}
            Número:\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\tR$ {conta.saldo}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._start += 1


# Classe Conta
class Conta:
    def __init__(self, cliente, numero):
        self._saldo = 0
        self._agencia = "0001"
        self._numero = numero
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
        return cls(
            cliente,
            numero,
        )

    def sacar(self, valor):
        if valor > self.saldo:
            print("Saldo insuficiente.")
        elif valor > 0:
            self._saldo -= valor
            return True
        else:
            print("Operação não suportada.")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso.")
        else:
            print("Valor inválido.")
            return False

        return True


# Classe ContaCorrente herda de Conta e implementa operação saque
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):

        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == "Saque"
            ]
        )
        # .__name__]) alternativa de pegar o tipo saque

        if valor > self._limite:
            print("Valor excedeu o limite")
        elif numero_saques >= self._limite_saques:
            print("Limite diario de saques excedido.")
        else:
            return super().sacar(valor)

        return False

    def __repr__(self):
        return f"<{self.__class__.__name__}: ('{self.agencia}', '{self.numero}', '{self.cliente.nome}')>"

    def __str__(self):
        return f"""\
          Agência: \t{self.agencia}
          C/C: \t\t{self.numero}
          Titular: \t{self.cliente.nome}
        """


# Classe Cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):

        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("Limite de transações diárias excedido.")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


# Classe PessoaFisica herda de Cliente
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.cpf}')>"


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

    def gerador_relatorio(self, tipo_transacao=None):
        # gerar um relatorio sobre o tipo de transacao escolhido
        for transacao in self._transacoes:
            if (
                tipo_transacao is None
                or transacao["tipo"].lower() == tipo_transacao.lower()
            ):
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.now().date()
        transacoes_do_dia = []

        for transacao in self._transacoes:
            data_transacao = datetime.strptime(
                transacao["data"], "%d/%m/%Y %H:%M:%S"
            ).date()
            if data_atual == data_transacao:
                transacoes_do_dia.append(transacao)
        return transacoes_do_dia


class Transacao(ABC):
    @property
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.now()

    @property
    def valor(self):
        return self._valor

    @property
    def data(self):
        return self._data

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.now()

    @property
    def valor(self):
        return self._valor

    @property
    def data(self):
        return self._data

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# funcões para criação de conta e cliente
def log_transacao(funcao):
    def envelope(*args, **kwargs):
        resultado = funcao(*args, **kwargs)
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # alterar implementacao para salvar em arquivo
        try:
            with open(ROOT_PATH / "log.txt", "a", newline="", encoding="utf-8") as log:
                log.write(
                    f"[{data_hora}] Função: '{funcao.__name__}'. Argumentos: {args} e {kwargs}. Retorna: {resultado}\n"
                )
        except IOError as exc:
            print(f"Arquivo não encontrado: {exc}")

        return resultado

    return envelope


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def encontrar_conta(cliente):
    if not cliente.contas:
        print("Conta não encontrada")
        return

    return cliente.contas[0]


@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe seu cpf(somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Cliente já existe.")
        return

    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento: (dd-mm-aaaa)")
    endereco = input(
        "Informe seu endereço (logradouro, número - bairro - cidade/sigla estado: "
    )

    cliente = PessoaFisica(
        cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco
    )

    clientes.append(cliente)
    print("Titular criado com sucesso!")


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe seu cpf(somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta criada com sucesso!")


def listar_contas(contas):
    for conta in ContaIterador(contas):
        print("-" * 100)
        print(str(conta))


def encontra_cliente_conta(clientes):
    while True:
        cpf = input("Informe seu cpf (somente números): ")
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("Cliente não encontrado. Tente novamente.")
            continue

        conta = encontrar_conta(cliente)
        if not conta:
            print("Conta não encontrada. Tente novamente.")
            continue

        return cliente, conta


@log_transacao
def deposito(clientes):
    cliente, conta = encontra_cliente_conta(clientes)

    valor = float(input("Valor do depósito: "))
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)


@log_transacao
def saque(clientes):
    cliente, conta = encontra_cliente_conta(clientes)

    valor = float(input("Valor do saque: "))
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe seu cpf(somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = encontrar_conta(cliente)
    if not conta:
        return

    # realizar a implementação do gerador do histórico

    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerador_relatorio():
        tem_transacao = True
        extrato += (
            f"\n{transacao['tipo']}:\nR${transacao['valor']:.2f}\n{transacao['data']}"
        )
        if not tem_transacao:
            print("Não existem transações realizadas nesta conta.")

    print(extrato)
    print(f"\nSaldo: R${conta.saldo:.2f}")


def menu():
    menu = """
    Escolha a operacao desejada.
    [1] - Novo Títular. 
    [2] - Nova conta. 
    [3] - Listar contas.
    [4] - Depositar.
    [5] - Sacar.
    [6] - Conferir extrato.
    [7] - Sair.
    => """
    return input(menu)


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        match opcao:
            case "1":
                criar_cliente(clientes)
            case "2":
                numero_conta = len(contas) + 1
                criar_conta(numero_conta, clientes, contas)
            case "3":
                listar_contas(contas)
            case "4":
                deposito(clientes)
            case "5":
                saque(clientes)
            case "6":
                exibir_extrato(clientes)
            case "7":
                print("Saindo....")
                return
            case _:
                print("Opção inválida. Tente novamente.")


main()
