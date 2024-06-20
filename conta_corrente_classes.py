from abc import ABC, ABCMeta, abstractmethod
from datetime import datetime

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
        return cls(cliente, numero,)
    
    def sacar(self, valor):
        if valor > self.saldo:
            print("Saldo insuficiente.")
        elif valor > 0:
            self._saldo -= valor
            # print(f"Saque de {valor} realizado. ")
            # self.historico.adicionar_transacao(Saque(valor))
            return True
        else:
            print("Operação não suportada.")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso.")
            # self.historico.adicionar_transacao(Deposito(valor))
        else:
            print("Valor inválido.")
            return False
        
        return True
        
            
# Classe ContaCorrente herda de Conta e implementa operação saque
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques = 3):
        super().__init__(cliente, numero)
        self._limite = limite
        self._limite_saques = limite_saques
    
    def sacar(self, valor):
        hoje = datetime.now().date()
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"  and transacao["data"].date() == hoje])
        #.__name__]) alternativa de pegar o tipo saque
        
        if valor > self._limite:
            print("Valor excedeu o limite")
        elif numero_saques >= self._limite_saques:
            print("Limite diario de saques excedido.")
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
          Agência: \t{self.agencia}
          C/C: \t\t{self.numero}
          Titular: \t{self.cliente.nome}
        """
        
        
# Classe Cliente 
class Cliente():
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
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
        
class Historico():
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
        
    def adicionar_transacao(self, transacao):
        self._transacoes.append({"tipo": transacao.__class__.__name__,
                                 "valor": transacao.valor,
                                 "data": transacao.data})
        
    
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
        sucesso_transacao =  conta.sacar(self.valor)
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
        sucesso_transacao =  conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            
# funcões para criação de conta e cliente
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None      

def encontrar_conta(cliente):
    if not cliente.contas:
        print("Conta não encontrada")
        return
    
    return cliente.contas[0]

def criar_cliente(clientes):
    cpf = input("Informe seu cpf(somente números): ")
    cliente = filtrar_cliente(cpf,clientes)
    
    if cliente:
        print("Cliente já existe.")
        return
    
    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento: (dd-mm-aaaa)")
    endereco = input("Informe seu endereço (logradouro, número - bairro - cidade/sigla estado: ")
    
    cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
    
    clientes.append(cliente)
    print("Titular criado com sucesso!")
    
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe seu cpf(somente números): ")
    cliente = filtrar_cliente(cpf,clientes)
    
    if not cliente:
        print("Cliente não encontrado.")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print("\nConta criada com sucesso!")
    
def listar_contas(contas):
    for conta in contas:
        print("-" *100)
        # print(f"""
        #     Agência: \t{conta.agencia}
        #     C/C: \t{conta.numero}
        #     Titular: \t{conta.cliente.nome}
        # """)
        print(str(conta))
        
    
def deposito(clientes):
    cpf = input("Informe seu cpf(somente números): ")
    cliente = filtrar_cliente(cpf,clientes)
    
    if not cliente:
        print("Cliente não encontrado.")
        return
    
    valor = float(input("Valor do depósito: "))
    transacao = Deposito(valor)  
    
    conta = encontrar_conta(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def sacar(clientes):
    cpf = input("Informe seu cpf(somente números): ")
    cliente = filtrar_cliente(cpf,clientes)
    
    if not cliente:
        print("Cliente não encontrado.")
        return
    
    valor = float(input("Valor do saque: "))
    transacao = Saque(valor)  
    
    conta = encontrar_conta(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def exibir_extrato(clientes):
    cpf = input("Informe seu cpf(somente números): ")
    cliente = filtrar_cliente(cpf,clientes)
    
    if not cliente:
        print("Cliente não encontrado.")
        return
    
    conta = encontrar_conta(cliente)
    if not conta:
        return
    
    transacoes = conta.historico.transacoes
    
    extrato = ""
    if not transacoes:
        print("Não há nenhuma transação realizada na sua conta.")
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\nR${transacao['valor']:.2f}\n{transacao['data']}"
            
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
        if opcao == "1":
            criar_cliente(clientes)
        elif opcao == "2":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "3":
            listar_contas(contas)
        elif opcao == "4":
            deposito(clientes)
        elif opcao == "5":
            sacar(clientes)
        elif opcao == "6":
            exibir_extrato(clientes)
        elif opcao == "7":
            break
        else:
            print("Opção inválida. Tente novamente.")
            
main()