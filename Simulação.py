import igraph
from crcalculo import crcalculo
from como_passou import como_passou
from numpy import genfromtxt, argsort, ones, flip, where, array
from numpy.random import dirichlet
from random import shuffle
import matplotlib.pyplot as plt
from statistics import mean, variance

# Entrada de Dados

mode = 1  # mode(0) = fweigth; mode(1) = Mean(abcdf)
mode_2 = 1  # mode_2(0) = max(statistics) ; mode_2(1) = mean(statistics)
Quantidade_De_Alunos = 1800  # Quantidade de alunos no modelo

# Início

my_data = genfromtxt('CSV2019.csv', delimiter=',', dtype=None, encoding=None)

# Criação dos vértices

g = igraph.Graph(len(my_data[0]) + 1, directed=True)

quant_prof = []
disciplina = []

j = 1

for i in range(len(g.vs)):
    try:
        g.vs[i]['id'] = i
        g.vs[i]['label'] = my_data[0][i]
        g.vs[i]['A'] = my_data[1][i]
        g.vs[i]['B'] = my_data[2][i]
        g.vs[i]['C'] = my_data[3][i]
        g.vs[i]['D'] = my_data[4][i]
        g.vs[i]['F'] = my_data[5][i]
        g.vs[i]['credito'] = my_data[6][i]

        g.vs[i]['peso'] = my_data[5][i]
        if mode == 1:
            g.vs[i]['peso'] = 4 - (
                    4 * float(g.vs[i]['A']) + 3 * float(g.vs[i]['B']) + 2 * float(g.vs[i]['C']) + 1 * float(
                g.vs[i]['D']) + 0 * float(g.vs[i]['F']))

        if my_data[0][i][:-2] == my_data[0][i + 1][:-2]:
            j = j + 1
        else:
            quant_prof.append(j)
            disciplina.append(g.vs[i]['label'][:-2])
            j = 1

    except:
        if i == len(my_data[0]):
            quant_prof.append(j)
            disciplina.append(g.vs[i - 1]['label'][:-2])
            g.vs[i]['id'] = i + 1
            g.vs[i]['label'] = 'fim'

print(quant_prof)

# Criação das arestas

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

# Structure dos alunos // Data acess

Alunos = {
    'ID': [],  # []
    'Tipo': [],  # ['']
    'Prior': [],  # [ [] ]
    'TurmasID': [],  # [ [''] ]
    'TurmasCre': [],  # [ [] ]
    'Notas': [],  # [ [] ]
    'CR': [],  # [ [] ]
}

for u in range(Quantidade_De_Alunos):  # PARAMETROS DE ESCOLHA SEMI-ALEATORIA
    o = dirichlet(ones(5), size=1)
    while o[0][4] <= 0.05 or \
            o[0][4] >= 0.15 or \
            o[0][0] + o[0][1] <= o[0][2] + o[0][3] or \
            o[0][0] <= 0.30 or \
            o[0][0] >= 0.65 or \
            o[0][3] > o[0][2]:
        o = dirichlet(ones(5), size=1)
    dirimean = 4 * o[0][0] + 3 * o[0][1] + 2 * o[0][2] + 1 * o[0][3] + 0 * o[0][4]
    print(dirimean)
    if dirimean >= 2.2:
        tipo = 'F'
    if dirimean >= 2.5:
        tipo = 'D'
    if dirimean >= 2.7:
        tipo = 'C'
    if dirimean >= 3.0:
        tipo = 'B'
    if dirimean >= 3.2:
        tipo = 'A'
    Alunos['ID'].append(u)
    Alunos['Tipo'].append(tipo)
    Alunos['Prior'].append(o[0])
    Alunos['TurmasID'].append([])
    Alunos['TurmasCre'].append([])
    Alunos['Notas'].append([])
    Alunos['CR'].append([])

#  Simulação

cr_division = [6, 5, 4, 5, 3, 3]
materia_counter = 0

materia_idtemp = []
materia_weighttemp = []
materia_contadorTemp = 0

for c in range(len(cr_division) + 1):  # Calcular Cr
    if c != 0:
        for cr in range(len(Alunos['CR'])):  # usa Alunos notas, Turma ID e crédito
            Alunos['CR'][cr].append(crcalculo(Alunos['Notas'][cr], Alunos['TurmasCre'][cr]))

        temporario = []
        temporario2 = []

        for temp in range(len(Alunos['CR'])):
            temporario = (Alunos['CR'][temp][-1:])
            temporario2.append(temporario[0])
            temporario = []
        crtemp = flip(argsort(temporario2))
        crtemp = crtemp.tolist()
    if c == len(cr_division):
        break
    for m in range(cr_division[c] + 1):  # atribuir os professores para os alunos para calcular "Como_passa"
        if m != 0 and c == 0:  # PRIMEIRO QUAD CALCULO DAS NOTAS POR MATÉRIA
            vamover = 0
            while vamover != len(Alunos['ID']):
                if (Alunos['ID'].index(vamover) + 1) / cap == round((Alunos['ID'].index(vamover) + 1) / cap):
                    temporario = materia_idtemp[int((Alunos['ID'].index(vamover) + 1) / cap) - 1]
                    Alunos['TurmasID'][vamover].append(temporario)
                    Alunos['TurmasCre'][vamover].append(int(g.vs[temporario]['credito']))
                    likelihood = [g.vs[temporario]['A'], g.vs[temporario]['B'], g.vs[temporario]['C'],
                                  g.vs[temporario]['D'], g.vs[temporario]['F']]
                    Alunos['Notas'][vamover].append(como_passou(Alunos['Prior'][vamover], likelihood, mode_2))
                else:
                    temporario = materia_idtemp[int((Alunos['ID'].index(vamover) + 1) / cap)]
                    Alunos['TurmasID'][vamover].append(temporario)
                    Alunos['TurmasCre'][vamover].append(int(g.vs[temporario]['credito']))
                    likelihood = [g.vs[temporario]['A'], g.vs[temporario]['B'], g.vs[temporario]['C'],
                                  g.vs[temporario]['D'], g.vs[temporario]['F']]
                    Alunos['Notas'][vamover].append(como_passou(Alunos['Prior'][vamover], likelihood, mode_2))

                vamover = vamover + 1

            materia_counter = materia_counter + 1

            print(materia_counter)

            materia_idtemp = []
            materia_weighttemp = []
            materia_contadorTemp = 0

        if m != 0 and c != 0:  # DEMAIS QUADS CALCULO DAS NOTAS POR MATÉRIA

            vamover = 0  # vamover = temp
            while vamover != len(Alunos['ID']):
                if (crtemp.index(vamover) + 1) / cap == round((crtemp.index(vamover) + 1) / cap):
                    temporario = materia_idtemp[materia_indice[int((crtemp.index(vamover) + 1) / cap) - 1]]
                    Alunos['TurmasID'][vamover].append(temporario)
                    Alunos['TurmasCre'][vamover].append(int(g.vs[temporario]['credito']))
                    likelihood = [g.vs[temporario]['A'], g.vs[temporario]['B'], g.vs[temporario]['C'],
                                  g.vs[temporario]['D'], g.vs[temporario]['F']]
                    Alunos['Notas'][vamover].append(como_passou(Alunos['Prior'][vamover], likelihood, mode_2))
                else:
                    temporario = materia_idtemp[materia_indice[int((crtemp.index(vamover) + 1) / cap)]]
                    Alunos['TurmasID'][vamover].append(temporario)
                    Alunos['TurmasCre'][vamover].append(int(g.vs[temporario]['credito']))
                    likelihood = [g.vs[temporario]['A'], g.vs[temporario]['B'], g.vs[temporario]['C'],
                                  g.vs[temporario]['D'], g.vs[temporario]['F']]
                    Alunos['Notas'][vamover].append(como_passou(Alunos['Prior'][vamover], likelihood, mode_2))
                vamover = vamover + 1

            materia_counter = materia_counter + 1
            if materia_counter == 26:  # limite de matérias
                break
            print(materia_counter)

            materia_idtemp = []
            materia_weighttemp = []
            materia_contadorTemp = 0

        if m == cr_division[c]:
            continue
        for p in range(len(my_data[0])):  # Organizar os professores para o For anterior
            if c == 0:  # Primeiro Quad
                if g.vs[p]['label'][:-2] == disciplina[materia_counter]:  # Agrupar todos os professores da matéria X para distribuir os alunos
                    materia_idtemp.append(g.vs[p]['id'])
                    materia_contadorTemp = materia_contadorTemp + 1

                    if materia_contadorTemp == quant_prof[
                        materia_counter]:  # Organizar os professores de forma aleatoria para distribuir os alunos...
                        materia_indice = shuffle(materia_idtemp)
                        cap = len(Alunos['ID']) / quant_prof[materia_counter]
                        round(cap)

                        break

            else:  # Outros Quads
                if g.vs[p]['label'][:-2] == disciplina[materia_counter]:  # Agrupar todos os professores da matéria X para distribuir os alunos
                    materia_idtemp.append(g.vs[p]['id'])
                    materia_weighttemp.append(g.vs[p]['peso'])
                    materia_contadorTemp = materia_contadorTemp + 1

                    if materia_contadorTemp == quant_prof[
                        materia_counter]:  # Organizar os professores em peso crescente para distribuir os alunos...
                        materia_indice = argsort(materia_weighttemp)
                        materia_indice = materia_indice.tolist()
                        cap = len(Alunos['ID']) / quant_prof[materia_counter]
                        round(cap)

                        break

# Plot dos gráficos de forma ineficiente

t = array(Alunos['Tipo'])
a = where(t == 'A')[0]
b = where(t == 'B')[0]
c = where(t == 'C')[0]
d = where(t == 'D')[0]
f = where(t == 'F')[0]

ordem = [a, b, c, d, f]

a1 = []
for aa in range(len(a)):
    a1.append(Alunos['CR'][a[aa]][0])
a2 = []
for aa in range(len(a)):
    a2.append(Alunos['CR'][a[aa]][1])
a3 = []
for aa in range(len(a)):
    a3.append(Alunos['CR'][a[aa]][2])
a4 = []
for aa in range(len(a)):
    a4.append(Alunos['CR'][a[aa]][3])
a5 = []
for aa in range(len(a)):
    a5.append(Alunos['CR'][a[aa]][4])
a6 = []
for aa in range(len(a)):
    a6.append(Alunos['CR'][a[aa]][5])

# media
am1 = mean(a1)
am2 = mean(a2)
am3 = mean(a3)
am4 = mean(a4)
am5 = mean(a5)
am6 = mean(a6)

# variabilidade
av1 = variance(a1)
av2 = variance(a2)
av3 = variance(a3)
av4 = variance(a4)
av5 = variance(a5)
av6 = variance(a6)

b1 = []
for aa in range(len(b)):
    b1.append(Alunos['CR'][b[aa]][0])
b2 = []
for aa in range(len(b)):
    b2.append(Alunos['CR'][b[aa]][1])
b3 = []
for aa in range(len(b)):
    b3.append(Alunos['CR'][b[aa]][2])
b4 = []
for aa in range(len(b)):
    b4.append(Alunos['CR'][b[aa]][3])
b5 = []
for aa in range(len(b)):
    b5.append(Alunos['CR'][b[aa]][4])
b6 = []
for aa in range(len(b)):
    b6.append(Alunos['CR'][b[aa]][5])

bm1 = mean(b1)
bm2 = mean(b2)
bm3 = mean(b3)
bm4 = mean(b4)
bm5 = mean(b5)
bm6 = mean(b6)

bv1 = variance(b1)
bv2 = variance(b2)
bv3 = variance(b3)
bv4 = variance(b4)
bv5 = variance(b5)
bv6 = variance(b6)

c1 = []
for aa in range(len(c)):
    c1.append(Alunos['CR'][c[aa]][0])
c2 = []
for aa in range(len(c)):
    c2.append(Alunos['CR'][c[aa]][1])
c3 = []
for aa in range(len(c)):
    c3.append(Alunos['CR'][c[aa]][2])
c4 = []
for aa in range(len(c)):
    c4.append(Alunos['CR'][c[aa]][3])
c5 = []
for aa in range(len(c)):
    c5.append(Alunos['CR'][c[aa]][4])
c6 = []
for aa in range(len(c)):
    c6.append(Alunos['CR'][c[aa]][5])

cm1 = mean(c1)
cm2 = mean(c2)
cm3 = mean(c3)
cm4 = mean(c4)
cm5 = mean(c5)
cm6 = mean(c6)

cv1 = variance(c1)
cv2 = variance(c2)
cv3 = variance(c3)
cv4 = variance(c4)
cv5 = variance(c5)
cv6 = variance(c6)

d1 = []
for aa in range(len(d)):
    d1.append(Alunos['CR'][d[aa]][0])
d2 = []
for aa in range(len(d)):
    d2.append(Alunos['CR'][d[aa]][1])
d3 = []
for aa in range(len(d)):
    d3.append(Alunos['CR'][d[aa]][2])
d4 = []
for aa in range(len(d)):
    d4.append(Alunos['CR'][d[aa]][3])
d5 = []
for aa in range(len(d)):
    d5.append(Alunos['CR'][d[aa]][4])
d6 = []
for aa in range(len(d)):
    d6.append(Alunos['CR'][d[aa]][5])

dm1 = mean(d1)
dm2 = mean(d2)
dm3 = mean(d3)
dm4 = mean(d4)
dm5 = mean(d5)
dm6 = mean(d6)

dv1 = variance(d1)
dv2 = variance(d2)
dv3 = variance(d3)
dv4 = variance(d4)
dv5 = variance(d5)
dv6 = variance(d6)

f1 = []
for aa in range(len(f)):
    f1.append(Alunos['CR'][f[aa]][0])
f2 = []
for aa in range(len(f)):
    f2.append(Alunos['CR'][f[aa]][1])
f3 = []
for aa in range(len(f)):
    f3.append(Alunos['CR'][f[aa]][2])
f4 = []
for aa in range(len(f)):
    f4.append(Alunos['CR'][f[aa]][3])
f5 = []
for aa in range(len(f)):
    f5.append(Alunos['CR'][f[aa]][4])
f6 = []
for aa in range(len(f)):
    f6.append(Alunos['CR'][f[aa]][5])

fm1 = mean(f1)
fm2 = mean(f2)
fm3 = mean(f3)
fm4 = mean(f4)
fm5 = mean(f5)
fm6 = mean(f6)

fv1 = variance(f1)
fv2 = variance(f2)
fv3 = variance(f3)
fv4 = variance(f4)
fv5 = variance(f5)
fv6 = variance(f6)

plt.figure(50)
x = [1, 2, 3, 4, 5, 6]
x1 = [0.9, 1.9, 2.9, 3.9, 4.9, 5.9]
x2 = [0.95, 1.95, 2.95, 3.95, 4.95, 5.95]
x3 = [1.05, 2.05, 3.05, 4.05, 5.05, 6.05]
x4 = [1.1, 2.1, 3.1, 4.1, 5.1, 6.1]

y1 = [am1, am2, am3, am4, am5, am6]
plt.plot(x, y1, 'black', label="Tipo A")
plt.plot(x1, [a1, a2, a3, a4, a5, a6], 'k*', markersize=2)

y2 = [bm1, bm2, bm3, bm4, bm5, bm6]
plt.plot(x, y2, 'g', label="Tipo B")
plt.plot(x2, [b1, b2, b3, b4, b5, b6], 'g*', markersize=2)

y3 = [cm1, cm2, cm3, cm4, cm5, cm6]
plt.plot(x, y3, 'cyan', label="Tipo C")
plt.plot(x, [c1, c2, c3, c4, c5, c6], 'c*', markersize=2)

y4 = [dm1, dm2, dm3, dm4, dm5, dm6]
plt.plot(x, y4, 'b', label="Tipo D")
plt.plot(x3, [d1, d2, d3, d4, d5, d6], 'b*', markersize=2)

y10 = [fm1, fm2, fm3, fm4, fm5, fm6]
plt.plot(x, y10, 'r', label="Tipo F")
plt.plot(x4, [f1, f2, f3, f4, f5, f6], 'r*', markersize=2)

plt.xlabel('Quadrimestres')
plt.ylabel('CR')
plt.title('Variação média do CR entre Tipos')

plt.ylim(0, 4)
plt.xlim(0.85, 6.15)
plt.legend()
plt.show()

plt.figure(100)
x = [1, 2, 3, 4, 5, 6]
y5 = [av1, av2, av3, av4, av5, av6]
plt.plot(x, y5, 'black', label="Tipo A")

y6 = [bv1, bv2, bv3, bv4, bv5, bv6]
plt.plot(x, y6, 'g', label="Tipo B")

y7 = [cv1, cv2, cv3, cv4, cv5, cv6]
plt.plot(x, y7, 'cyan', label="Tipo C")

y8 = [dv1, dv2, dv3, dv4, dv5, dv6]
plt.plot(x, y8, 'b', label="Tipo D")

y11 = [fv1, fv2, fv3, fv4, fv5, fv6]
plt.plot(x, y11, 'r', label="Tipo F")

plt.xlabel('Quadrimestres')
plt.ylabel('Variance')
plt.title('Variancia do Cr por Quadrimestres e Tipos')

plt.legend()
plt.show()
