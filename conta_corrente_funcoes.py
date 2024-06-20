def menu():
    menu = """
    Escolha a operacao desejada.
    [1] - Novo usuario. 
    [2] - Nova conta. 
    [3] - Listar contas.
    [4] - Depositar.
    [5] - Sacar.
    [6] - Conferir extrato.
    [7] - Sair.
    => """
    return input(menu)

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_usuario(usuarios):
    cpf = input("Informe seu cpf(somente números): ")
    usuario = filtrar_usuario(cpf,usuarios)
    
    if usuario:
        print("Esse CPF já está cadastrado.")
        return
        
    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe a data de nascimento(dd/mm/aaaa): ")
    endereco = input("Informe seu endereço (logradouro, número - bairro - cidade/sigla estado: ")
    
    usuarios.append({"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "endereco": endereco})
    
    print("Usuário criado com sucesso!") 

def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe seu cpf(somente números): ")
    usuario = filtrar_usuario(cpf,usuarios)
    
    if usuario:
        conta = ({"agencia": agencia, "numero_conta": str(numero_conta), "usuario": usuario, "saldo": 0.0, "extrato": "",
            "numero_saque": 0})
        contas.append(conta)
        print("Conta criada com sucesso!")
    else:
        print("Usuário não cadastrado, realize o cadastro primeiro.")
        
def listar_contas(contas):
    if contas:
        for conta in contas:
            print(f"Agencia: {conta['agencia']}\nNúmero da Conta: {conta['numero_conta']}\nUsuário: {conta['usuario']['nome']} ")
    else:
        print("Conta não encontrada.")
        
def encontrar_conta(numero_conta, contas):
    conta = [conta for conta in contas if conta['numero_conta'] == numero_conta]
    return conta[0] if conta else None
    
def deposito(conta, valor, /):
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito de R$ {valor:.2f}.\n"
        print(f"Depósito de {valor:.2f} realizado com sucesso!")
    else:
        print("Valor inválido.")
    return conta

def saque(*, conta, valor, limite, limite_diario):
    if valor > conta["saldo"]:
        print("Saldo insuficiente.")
    elif valor > limite:
        print("Valor excedeu o limite")
    elif conta["numero_saque"] >= limite_diario:
        print("Limite diario de saques excedido.")
    elif valor > 0:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque de R$ {valor:.2f}\n"
        conta["numero_saque"] += 1
        print("Saque  realizado com sucesso.")
    else:
        print("Não foi possível realizar a operação. Valor inválido")
    return conta

def exibir_extrato(conta, / ):
    print("Extrato vazio." if not conta['extrato'] else conta['extrato'])
    print(f"Saldo: R${conta['saldo']}.")
    

        
def main():
    usuarios = []
    contas = []
    LIMITE_DIARIO = 3
    LIMITE = 500
    AGENCIA = "0001"
    numero_conta = 1
    
    while True:
        opcao = menu()
        if opcao == "1":
            criar_usuario(usuarios)
        elif opcao == "2":
            criar_conta(AGENCIA, numero_conta, usuarios, contas)
            numero_conta += 1
        elif opcao == "3":
            listar_contas(contas)
        elif opcao == "4":
            numero_conta = input("Informe o número da conta: ")
            conta = encontrar_conta(numero_conta, contas)
            if conta:
                valor = float(input("Informe o valor para depósito: "))
                conta = deposito(conta, valor)
            else:
                print("Conta não encontrada.")
        elif opcao == "5":
            numero_conta = input("Informe o número da conta: ")
            conta = encontrar_conta(numero_conta, contas)
            if conta:
                valor = float(input("Informe o valor para saque: "))
                conta = saque(conta = conta, valor = valor, limite = LIMITE, limite_diario = LIMITE_DIARIO)
            else:
                print("Conta não encontrada.")
        elif opcao == "6":
            numero_conta = input("Informe o número da conta: ")
            conta = encontrar_conta(numero_conta, contas)
            if conta:
                exibir_extrato(conta)
            else:
                print("Conta não encontrada.")
        elif opcao == "7":
            break
        else:
            print("Opção inválida. Tente novamente.")
            
main()