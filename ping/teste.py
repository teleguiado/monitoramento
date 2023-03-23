uma_lista = [1, 2, 3, 4,]
outra_lista = [1, 2, 8, 3, 4, 5]

diferente = [elemento for elemento in outra_lista if elemento not in uma_lista]

print(diferente)