import igraph
from crcalculo import crcalculo
from como_passou import como_passou
from numpy import genfromtxt

### PROGRAMA ANTERIOR, PARA CAMINHO MINIMO

# Entrada de Dados

# mode(0) = fweigth ; mode(1) = Mean(abcdf)
# mode_2(0) = max(statistics) ; mode_2(1) = mean(statistics)

mode = 0
mode_2 = 1

# Início
# CSV_Materias_BCT_FINALIZADO.csv
my_data = genfromtxt('CSV_Materias_BCT_FINALIZADO.csv', delimiter=',', dtype=None, encoding=None)

# Criação do Grafo

g = igraph.Graph(len(my_data[0]) + 1, directed=True)

for i in range(len(g.vs)):
    try:
        g.vs[i]['id'] = i
        g.vs[i]['label'] = my_data[0][i]
        g.vs[i]['A'] = my_data[1][i]
        g.vs[i]['B'] = my_data[2][i]
        g.vs[i]['C'] = my_data[3][i]
        g.vs[i]['D'] = my_data[4][i]
        g.vs[i]['F'] = my_data[5][i]
        g.vs[i]['peso'] = my_data[5][i]
        if mode == 1:
            g.vs[i]['peso'] = 4 - (
                    4 * float(g.vs[i]['A']) + 3 * float(g.vs[i]['B']) + 2 * float(g.vs[i]['C']) + 1 * float(
                g.vs[i]['D']) + 0 * float(g.vs[i]['F']))
        g.vs[i]['credito'] = my_data[6][i]
    except:
        if i == len(my_data[0]):
            g.vs[i]['id'] = i + 1
            g.vs[i]['label'] = 'fim'
# Criação Dos EDGES

x = 0
for b in range(len(my_data[0])):
    for a in range(len(my_data[0])):
        if g.vs[b]["label"][:-2] == 'pd' and a == len(my_data[0]) - 1:  # Trocar 'em' pelo ultimo vertice
            weight = g.vs[b]['peso']
            g.add_edges([(b, len(my_data[0]))])
            g.es[x]['id'] = x
            g.es[x]['og'] = g.vs[b]['label']
            g.es[x]['end'] = 'fim'
            g.es[x]['weight'] = weight
            x = x + 1
        if g.vs[a]["label"][:-2] != g.vs[b]["label"][:-2] and b < a:
            weight = g.vs[b]['peso']
            g.add_edges([(b, a)])
            g.es[x]['id'] = x
            g.es[x]['og'] = g.vs[b]['label']
            g.es[x]['end'] = g.vs[a]['label']
            g.es[x]['weight'] = weight
            x = x + 1
            if g.vs[a]["label"][:-2] != g.vs[a + 1]["label"][:-2]:
                break

# BUSCA DO MENOR CAMINHO

priors = [[0.5, 0.15, 0.15, 0.10, 0.1], [0.25, 0.3, 0.20, 0.15, 0.1], [0.20, 0.25, 0.20, 0.20, 0.15],
          [0.20, 0.20, 0.30, 0.15, 0.15], [0.10, 0.2, 0.3, 0.25, 0.15], [0.175, 0.175, 0.30, 0.175, 0.175]]

g.vs['label_size'] = 6
g.vs['vertex_size'] = 0.1
g.es['width'] = 0.09
g.es['arrow_size'] = 0.3
color = ['red', 'blue', 'brown', 'cyan', 'yellow', 'purple']

for k in range(6):
    prior = priors[k]

    cr_division = [6, 5, 4, 5, 3, 3]
    g.vs['checklist'] = 'undone'

    menor = []
    names = []
    temp = []
    position = []

    id = []
    likelihood = []
    nota_array = []
    credito_array = []

    for c in range(
            6):  # [For] destinado a separar os quadrimestres ideais(cr_division) if para pular o primeiro e usa o [id]
        if c != 0:
            for d in range(len(id)):
                likelihood.append(g.vs[id[d]]['A'])
                likelihood.append(g.vs[id[d]]['B'])
                likelihood.append(g.vs[id[d]]['C'])
                likelihood.append(g.vs[id[d]]['D'])
                likelihood.append(g.vs[id[d]]['F'])
                nota_array.append(como_passou(prior, likelihood, mode_2))
                credito_array.append(int(g.vs[id[d]]['credito']))
                likelihood = []
            cr = crcalculo(nota_array, credito_array)
            # print(f'O CR no quadrimestre {c} é {cr:.3f}')
        for a in range(cr_division[c] + 1):  # Número de materias + 1 (manual)
            if temp != []:
                p = temp.index(min(temp))
                menor.append(names[p])
                id.append(position[p])
                position = []
                names = []
                temp = []
            for b in range(len(my_data[0])):
                if g.vs[b]['checklist'] == 'done':
                    continue
                temp.append(g.vs[b]['peso'])
                g.vs[b]['checklist'] = 'done'
                names.append(g.vs[b]['label'])
                position.append(g.vs[b]['id'])
                if g.vs[b + 1]['label'][-2:] == '00':
                    break

    # SOLUÇÃO PREGUIÇOSA
    for d in range(len(id)):
        likelihood.append(g.vs[id[d]]['A'])
        likelihood.append(g.vs[id[d]]['B'])
        likelihood.append(g.vs[id[d]]['C'])
        likelihood.append(g.vs[id[d]]['D'])
        likelihood.append(g.vs[id[d]]['F'])
        nota_array.append(como_passou(prior, likelihood, mode_2))
        credito_array.append(int(g.vs[id[d]]['credito']))
        likelihood = []
    cr = crcalculo(nota_array, credito_array)
    # print(f'O CR no quadrimestre final é {cr:.3f}')

    edges = []
    for a in range(len(menor)):
        for x in range(len(g.es)):
            try:
                if g.es[x]['og'] == menor[a] and g.es[x]['end'] == 'fim':
                    edges.append(g.es[x]['id'])
                if g.es[x]['og'] == menor[a] and g.es[x]['end'] == menor[a + 1]:
                    edges.append(g.es[x]['id'])
            except:
                break

    # frufru da interface

    for a in range(len(edges)):
        g.es[edges[a]]['label'] = g.es[edges[a]]['weight']
        g.es[edges[a]]["color"] = 'black'  # color[k]
        g.es[edges[a]]["width"] = 4
        g.es[edges[a]]["label_size"] = 15
        g.es[edges[a]]['arrow_size'] = 1

    # print(nota_array)
print(menor)

# PLOT DA IMAGEM

# layout = g.layout("kk")
igraph.plot(g, bbox=(1000, 1000), autocurve=False)  # , layout=layout)

# INICIO TESTES


# FIM TESTES
