# --- ALGORITMOS DE BUSCA E ORDENAÇÃO MANUAIS ---

def busca_sequencial(registros, cpf):
    """Realiza a busca sequencial por CPF e retorna o índice e a quantidade de comparações."""
    comparacoes = 0
    for i in range(len(registros)):
        comparacoes += 1
        if registros[i]["cpf"] == cpf:
            return i, comparacoes
    return -1, comparacoes


def busca_binaria(registros, cpf):
    """Realiza a busca binária por CPF num vetor previamente ordenado."""
    inicio = 0
    fim = len(registros) - 1
    comparacoes = 0
    while inicio <= fim:
        meio = (inicio + fim) // 2
        comparacoes += 1
        if registros[meio]["cpf"] == cpf:
            return meio, comparacoes
        elif registros[meio]["cpf"] < cpf:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1, comparacoes


def ordenar_insercao(registros, chave):
    """Ordenação manual (Insertion Sort) sem utilizar sorted() nativo."""
    lista = registros[:]
    for i in range(1, len(lista)):
        atual = lista[i]
        j = i - 1
        while j >= 0 and lista[j][chave] > atual[chave]:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = atual
    return lista

