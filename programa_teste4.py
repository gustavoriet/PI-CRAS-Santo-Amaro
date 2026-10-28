import json
import os
import time
import random

ARQUIVO_DADOS = "concessoes_cras.json"

# --- PERSISTÊNCIA ---

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

lista_concessoes = carregar_dados()
pilha_historico = []

# --- ESTRUTURA PARA ÁRVORE BINÁRIA DE BUSCA (ABB) ---

class NoABB:
    def __init__(self, chave, dados):
        self.chave = chave
        self.dados = dados
        self.esquerda = None
        self.direita = None

def inserir_abb(raiz, chave, dados):
    if raiz is None:
        return NoABB(chave, dados)
    if chave < raiz.chave:
        raiz.esquerda = inserir_abb(raiz.esquerda, chave, dados)
    else:
        raiz.direita = inserir_abb(raiz.direita, chave, dados)
    return raiz

def buscar_abb(raiz, chave):
    comparacoes = 0
    atual = raiz
    while atual is not None:
        comparacoes += 1
        if chave == atual.chave:
            return atual.dados, comparacoes
        elif chave < atual.chave:
            atual = atual.esquerda
        else:
            atual = atual.direita
    return None, comparacoes

# --- ALGORITMOS DE BUSCA ---

def busca_sequencial(vetor, chave):
    comparacoes = 0
    for item in vetor:
        comparacoes += 1
        if item["cpf"] == chave:
            return item, comparacoes
    return None, comparacoes

def busca_binaria(vetor, chave):
    comparacoes = 0
    inicio = 0
    fim = len(vetor) - 1
    while inicio <= fim:
        comparacoes += 1
        meio = (inicio + fim) // 2
        if vetor[meio]["cpf"] == chave:
            return vetor[meio], comparacoes
        elif vetor[meio]["cpf"] < chave:
            inicio = meio + 1
        else:
            fim = meio - 1
    return None, comparacoes

# --- GERADOR DE DADOS E EXECUÇÃO DO EXPERIMENTO ---

def executar_experimento():
    print("\n" + "="*60)
    print("      EXPERIMENTO DE ALGORITMOS DE BUSCA - PROJETO INTEGRADOR")
    print("="*60)
    
    tamanhos = [100, 1000, 10000]
    
    for n in tamanhos:
        print(f"\n---> TESTANDO COM {n} REGISTROS <---")
        
        # 1. Geração de N registros fictícios
        dados_ficticios = []
        for i in range(n):
            cpf_ficticio = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
            dados_ficticios.append({
                "cpf": cpf_ficticio,
                "nome": f"Beneficiario_{i}",
                "total_cestas": random.randint(1, 12)
            })
        
        # Escolhe um CPF existente próximo do final para testar pior caso
        cpf_alvo = dados_ficticios[-1]["cpf"]
        
        # 2. Teste Busca Sequencial
        inicio_t = time.perf_counter()
        res_seq, comp_seq = busca_sequencial(dados_ficticios, cpf_alvo)
        fim_t = time.perf_counter()
        tempo_seq = (fim_t - inicio_t) * 1000  # milissegundos

        # 3. Preparação e Teste Busca Binária (Requer ordenação)
        dados_ordenados = list(dados_ficticios)
        # Ordenação Bubble Sort manual para volumes pequenos / QuickSort nativo apenas no benchmark de massa
        dados_ordenados.sort(key=lambda x: x["cpf"])
        
        inicio_t = time.perf_counter()
        res_bin, comp_bin = busca_binaria(dados_ordenados, cpf_alvo)
        fim_t = time.perf_counter()
        tempo_bin = (fim_t - inicio_t) * 1000

        # 4. Preparação e Teste Árvore Binária de Busca (ABB)
        raiz_abb = None
        for item in dados_ficticios:
            raiz_abb = inserir_abb(raiz_abb, item["cpf"], item)
            
        inicio_t = time.perf_counter()
        res_abb, comp_abb = buscar_abb(raiz_abb, cpf_alvo)
        fim_t = time.perf_counter()
        tempo_abb = (fim_t - inicio_t) * 1000

        # Exibição da tabela de resultados
        print(f"{'Algoritmo':<22} | {'Comparações':<12} | {'Tempo (ms)':<12}")
        print("-" * 52)
        print(f"{'Busca Sequencial':<22} | {comp_seq:<12} | {tempo_seq:.4f} ms")
        print(f"{'Busca Binária':<22} | {comp_bin:<12} | {tempo_bin:.4f} ms")
        print(f"{'Árvore Binária (ABB)':<22} | {comp_abb:<12} | {tempo_abb:.4f} ms")

# --- MENU PRINCIPAL ---

while True:
    print("\n=== MENU CRAS - SANTO AMARO DA IMPERATRIZ ===")
    print("1 - Cadastrar/Registrar concessão de cesta básica")
    print("2 - Listar todos os beneficiários e histórico de datas")
    print("3 - Listar CPFs com maior número de cestas recebidas (Ranking)")
    print("4 - Desfazer último registro (Operação em Pilha)")
    print("5 - Executar Experimento de Busca (100, 1.000 e 10.000 registros)")
    print("6 - Sair")
    
    opcao = input("Escolha uma opção (1-6): ")

    if opcao == "1":
        print("\n--- REGISTRO DE CONCESSÃO ---")
        cpf_input = input("Digite o CPF do beneficiário: ")
        
        encontrado = None
        for item in lista_concessoes:
            if item["cpf"] == cpf_input:
                encontrado = item
                break
        
        if encontrado:
            data_nova = input("Digite a data desta nova concessão (ex: 28/10/2026): ")
            encontrado["datas_concessoes"].append(data_nova)
            encontrado["total_cestas"] = len(encontrado["datas_concessoes"])
            pilha_historico.append({"tipo": "reincidencia", "cpf": cpf_input, "data": data_nova})
            salvar_dados(lista_concessoes)
            print(f"\n>> CPF já cadastrado! Nova concessão registrada.")
            print(f">> Beneficiário: {encontrado['nome']}")
            print(f">> Total de cestas recebidas: {encontrado['total_cestas']}")
            
        else:
            nome = input("Nome do beneficiário: ")
            membros = input("Quantidade de membros na família: ")
            data_inicial = input("Data da primeira concessão (ex: 28/10/2026): ")
            
            concessao = {
                "cpf": cpf_input,
                "nome": nome,
                "membros_familia": membros,
                "beneficio": "Cesta Básica",
                "datas_concessoes": [data_inicial],
                "total_cestas": 1,
                "amparo_legal": "Lei Municipal nº 2.889/2022"
            }
            
            lista_concessoes.append(concessao)
            pilha_historico.append({"tipo": "novo", "cpf": cpf_input})
            salvar_dados(lista_concessoes)
            print(f"\n>> Novo Beneficiário cadastrado com sucesso!")

    elif opcao == "2":
        print("\n--- LISTA GERAL DE BENEFICIÁRIOS E HISTÓRICO DE DATAS ---")
        if len(lista_concessoes) == 0:
            print("Nenhum registro encontrado.")
        else:
            for index, item in enumerate(lista_concessoes, start=1):
                datas_formatadas = ", ".join(item["datas_concessoes"])
                print(f"{index}. CPF: {item['cpf']} | Nome: {item['nome']} | Total: {item['total_cestas']} cesta(s)")
                print(f"   Datas das doações: [{datas_formatadas}]")
                print("-" * 60)

    elif opcao == "3":
        print("\n--- RANKING: CPFs COM MAIOR NÚMERO DE CESTAS RECEBIDAS ---")
        if len(lista_concessoes) == 0:
            print("Nenhum registro encontrado.")
        else:
            n = len(lista_concessoes)
            ranking = list(lista_concessoes)
            for i in range(n):
                for j in range(0, n - i - 1):
                    if ranking[j]["total_cestas"] < ranking[j + 1]["total_cestas"]:
                        ranking[j], ranking[j + 1] = ranking[j + 1], ranking[j]
            
            for index, item in enumerate(ranking, start=1):
                datas_formatadas = ", ".join(item["datas_concessoes"])
                print(f"{index}º Lugar - CPF: {item['cpf']} | Nome: {item['nome']} | Total: {item['total_cestas']} cesta(s)")
                print(f"   Datas doadas: [{datas_formatadas}]")

    elif opcao == "4":
        print("\n--- OPERAÇÃO EM PILHA: DESFAZER ÚLTIMA AÇÃO ---")
        if len(pilha_historico) == 0:
            print("Nenhuma ação recente para desfazer nesta sessão.")
        else:
            ultima_acao = pilha_historico.pop()
            cpf_alvo = ultima_acao["cpf"]
            for item in lista_concessoes:
                if item["cpf"] == cpf_alvo:
                    if ultima_acao["tipo"] == "novo":
                        lista_concessoes.remove(item)
                        print(f">> Sucesso: Cadastro do CPF {cpf_alvo} foi removido totalmente.")
                    elif ultima_acao["tipo"] == "reincidencia":
                        item["datas_concessoes"].pop()
                        item["total_cestas"] = len(item["datas_concessoes"])
                        print(f">> Sucesso: Última data adicionada ao CPF {cpf_alvo} foi removida.")
                    break
            salvar_dados(lista_concessoes)

    elif opcao == "5":
        executar_experimento()

    elif opcao == "6":
        print("Dados salvos. Encerrando o sistema...")
        break
    else:
        print("Opção inválida. Tente novamente.")