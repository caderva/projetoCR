# !!! TESTAR ALPHA DISTRIBUTION !!!
from numpy import ones

from numpy.random import dirichlet
Quantidade_De_Alunos = 500

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
    while 0.05 >= o[0][4] or\
            o[0][4] >= 0.15 or\
            o[0][0] + o[0][1] <= o[0][2] + o[0][3] or\
            o[0][0] <= 0.30 or\
            o[0][0] >= 0.6 or\
            o[0][3] > o[0][2]:

        o = dirichlet(ones(5), size=1)
    dirimean = 4*o[0][0] + 3*o[0][1] + 2*o[0][2] + 1*o[0][3] + 0*o[0][4]
    print(dirimean)
    if dirimean >= 2.4:
        tipo = 'F'
    if dirimean >= 2.6:
        tipo = 'D'
    if dirimean >= 2.8:
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

#  !!!!!Para Apresentar (COLOCARA DPS DO FOR DOS ALUNOS)!!!!!

demonstra = ['ID', 'Tipo', 'Prior', 'Turmas', 'TurmasID', 'Notas', 'CR']
aaa = 0
bbb = 0
ccc = 0
ddd = 0
fff = 0
for m in range(len(Alunos['Tipo'])):
    if Alunos['Tipo'][m] == 'A':
        aaa = aaa + 1
    if Alunos['Tipo'][m] == 'B':
        bbb = bbb + 1
    if Alunos['Tipo'][m] == 'C':
        ccc = ccc + 1
    if Alunos['Tipo'][m] == 'D':
        ddd = ddd + 1
    if Alunos['Tipo'][m] == 'F':
        fff = fff + 1
    #print(Alunos[demonstra[m]][0])
print(aaa)
print(bbb)
print(ccc)
print(ddd)
print(fff)
