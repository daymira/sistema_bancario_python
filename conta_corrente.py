menu = """
Escolha a operacao desejada.
[1] - Depositar.
[2] - Sacar.
[3] - Conferir extrato.
[4] - Sair.
=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_DIARIO = 3

while(True):
    opcao = input(menu)
    if opcao == "1":
        valor = float(input("Valor: "))
        if valor > 0:
            saldo += valor
            extrato = f"Deposito de R${valor:.2f} realizado com sucesso."
            print("Deposito realizado.")
        else:
            print("Valor inválido.")
    elif opcao == "2":
        valor_saque = float(input("Valor do saque: "))
        if valor_saque > saldo:
            print("Saldo insuficiente")
        elif valor_saque > limite:
            print("Limite excedido.")
        elif numero_saques >= LIMITE_DIARIO:
            print("Limite diario de saques excedido.")
        elif valor_saque > 0:
            saldo -= valor_saque
            extrato = f"Saque de R${valor_saque:.2f} realizado com sucesso."
            print("Saque realizado.")
            numero_saques += 1
    elif opcao == "3":
        print("Extrato vazio." if not extrato else extrato)
        print(f"Saldo: R${saldo:.2f}.")
    elif opcao == "4":
        break
    else:
        print("Operacao invalida. Selecione uma operacao valida.")
        
