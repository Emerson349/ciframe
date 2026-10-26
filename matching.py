# coding: utf-8


def musica_contem_sequencia(cifra, sequencia):
    """Retorna True quando a sequencia aparece contiguamente na cifra,
    na mesma ordem, sem acordes extras na musica e com grafia exata."""
    if not cifra or not sequencia:
        return False
    if len(sequencia) > len(cifra):
        return False
    if set(cifra) != set(sequencia):
        return False

    tamanho = len(sequencia)
    for inicio in range(len(cifra) - tamanho + 1):
        if cifra[inicio:inicio + tamanho] == list(sequencia):
            return True
    return False
