## DIO: Python AI Backend Developer

### 1° Desafio de Código

Sistema bancário em **Python**

### Objetivo
Criar um sistema bancário com as  operações:
- Depositar
- Sacar
- Visualizar Extrato
 
Só é possível realizar três saques diários com um limite de **R$500** por saque.

[código](conta_corrente.py)


### 2° Desafio de Código

Otimizando o Sistema Bancário com Funções Python

### Objetivo
- Melhorar o código criando funções para as operações utilizadas no desafio anterior. 
- Criar novas operações para criação de usuário e contas.

[código](conta_corrente_funcoes.py)


### 3° Desafio de Código

Modelando o Sistema Bancário em POO com Python

### Objetivo
- Armazenar os dados dos cliente e contas bancárias em objeto.
- O código deve seguir o modelo de classes abaixo


```mermaid
classDiagram
    Conta <|-- ContaCorrente
    Conta <| -- ContaPoupanca
    Conta "*" *-- "1" Cliente
    Conta "*" *-- "1" Historico
    Historico "1" o-- "*" Transacao
    Transacao <|-- Saque
    Transacao <|-- Deposito
    Cliente <|-- PessoaFisica
    class Conta {
        -saldo: float 
        -numero: int 
        -agencia: string 
        -cliente: Cliente 
        -historico: Historico 
        +saldo() float
        +nova_conta(cliente: Cliente, numero: int)Conta
        +sacar(valor: float) bool
        +depositar(valor: float) bool
    }
    class ContaPoupanca{
        
    }
    class ContaCorrente {
        -limite: float 
        -limite_saques: int 
    }
    class Historico {
        -adicionar_transacao: Transacao 
    }
    class Transacao {
        <<interface>>
        +registrar(conta: Conta)
    }
    class Saque {
        -valor: float
    }
    class Deposito {
        -valor: float
    }
    class Cliente {
        -endereco: string 
        -contas: List
        +realizar_transacao(conta: Conta, transacao: Transacao)
        +adicionar_conta(conta: Conta)
    }
    class PessoaFisica {
        -cpf: string
        -nome: string
        -data_nascimento: date
    }
```

[código](conta_corrente_classes.py)