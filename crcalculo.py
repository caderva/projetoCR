def crcalculo(nota_array, credito_array):
    cima = 0
    for a in range(len(credito_array)):
        cima = cima + (credito_array[a] * nota_array[a])

    cr = cima/sum(credito_array)
    return cr


