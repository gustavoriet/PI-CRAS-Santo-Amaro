import csv
from busca_ordenacao import busca_sequencial, busca_binaria, ordenar_insercao

ARQUIVO = "concessoes_cras.csv"
CAMPOS = ["cpf", "nome", "membros", "beneficio", "total_cestas", "datas"]

concessoes = []


def carregar():
    """Lê o arquivo CSV e carrega a lista de concessões na memória."""
    try:
        with open(ARQUIVO, newline="", encoding="utf-8") as arq:
            for linha in csv.DictReader(arq):
                linha["membros"] = int(linha["membros"])
                linha["total_cestas"] = int(linha["total_cestas"])
                concessoes.append(linha)
    except FileNotFoundError:
        pass  # Primeira execução: o arquivo ainda não existe


def salvar():
    """Grava a lista de concessões no arquivo CSV."""
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as arq:
        escritor = csv.DictWriter(arq, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(concessoes)


def ler_inteiro_positivo(mensagem):
    """Auxiliar para validação de entrada de números inteiros positivos."""
    while True:
        try:
            valor = int(input(mensagem))
            if valor > 0:
                return valor
            print("O valor precisa ser maior que zero.")
        except ValueError:
            print("Digite um número inteiro válido.")


def mostrar(c):
    """Exibe os dados formatados de um beneficiário do CRAS."""
    print(f"CPF: {c['cpf']} | Nome: {c['nome']:<25} | Membros: {c['membros']} | Total Cestas: {c['total_cestas']} | Datas: [{c['datas']}]")


def cadastrar():
    """Cadastra um novo beneficiário ou incrementa reincidência por CPF."""
    print("\n--- REGISTRO DE CONCESSÃO ---")
    cpf = input("CPF do beneficiário: ").strip()
    
    # Verifica reincidência via busca sequencial
    posicao, _ = busca_sequencial(concessoes, cpf)
    
    if posicao != -1:
        # CPF já cadastrado: incrementa total de cestas e adiciona nova data
        data_nova = input("Data desta nova concessão (dd/mm/aaaa): ").strip()
        concessoes[posicao]["total_cestas"] += 1
        concessoes[posicao]["datas"] += f"; {data_nova}"
        salvar()
        print(f">> CPF já cadastrado! Nova concessão registrada. Total acumulado: {concessoes[posicao]['total_cestas']}")
    else:
        # Novo CPF
        nome = input("Nome do beneficiário: ").strip().upper()
        membros = ler_inteiro_positivo("Quantidade de membros na família: ")
        data_inicial = input("Data da concessão (dd/mm/aaaa): ").strip()
        
        novo_registro = {
            "cpf": cpf,
            "nome": nome,
            "membros": membros,
            "beneficio": "Cesta Básica",
            "total_cestas": 1,
            "datas": data_inicial
        }
        concessoes.append(novo_registro)
        salvar()
        print(">> Novo beneficiário cadastrado com sucesso!")


def listar(lista):
    """Lista todos os registros passados por parâmetro."""
    if len(lista) == 0:
        print("Nenhuma concessão cadastrada.")
        return
    for c in lista:
        mostrar(c)


def buscar():
    """Realiza busca binária por CPF num vetor ordenado por inserção."""
    cpf = input("CPF procurado: ").strip()
    # Ordena a lista por CPF para possibilitar a Busca Binária
    ordenadas = ordenar_insercao(concessoes, "cpf")
    posicao, comparacoes = busca_binaria(ordenadas, cpf)
    
    if posicao == -1:
        print(f"Beneficiário não encontrado ({comparacoes} comparações).")
    else:
        print("\n--- REGISTRO ENCONTRADO ---")
        mostrar(ordenadas[posicao])
        print(f"({comparacoes} comparações computacionais realizadas)")


def relatorio():
    """Gera o relatório geral de concessões do CRAS Orlando Becker."""
    if len(concessoes) == 0:
        print("Nenhuma concessão cadastrada.")
        return
    
    total_cestas_geral = 0
    maior = concessoes[0]
    menor = concessoes[0]
    
    for c in concessoes:
        total_cestas_geral += c["total_cestas"]
        if c["total_cestas"] > maior["total_cestas"]:
            maior = c
        if c["total_cestas"] < menor["total_cestas"]:
            menor = c
            
    print("\n" + "="*50)
    print("  RELATÓRIO GERAL - CRAS SANTO AMARO DA IMPERATRIZ")
    print("="*50)
    print(f"Total de famílias cadastradas: {len(concessoes)}")
    print(f"Total geral de cestas doadas: {total_cestas_geral}")
    print(f"Média de cestas por família: {total_cestas_geral / len(concessoes):.1f}")
    print(f"Família com mais cestas: {maior['nome']} ({maior['total_cestas']} cestas)")
    print(f"Família com menos cestas: {menor['nome']} ({menor['total_cestas']} cestas)")


def menu():
    """Menu principal do sistema."""
    carregar()
    while True:
        print("\n=== SISTEMA DE BENEFÍCIOS EVENTUAIS - CRAS ===")
        print("1-Cadastrar  2-Listar  3-Buscar por CPF  4-Ranking por Cestas  5-Relatório  0-Sair")
        opcao = input("Opção: ").strip()
        
        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar(concessoes)
        elif opcao == "3":
            buscar()
        elif opcao == "4":
            # Ordena por total_cestas e exibe do maior para o menor (inverte a lista com [::-1])
            print("\n--- RANKING DE REINCIDÊNCIA (MAIOR PARA O MENOR) ---")
            listar(ordenar_insercao(concessoes, "total_cestas")[::-1])
        elif opcao == "5":
            relatorio()
        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()