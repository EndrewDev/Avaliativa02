import os, sys

# Digite o nome do caminho do arquivo da imagens
diretorio = input("Digite o caminho do diretório: ")
if os.path.isdir(diretorio):
    processar_diretorio(diretorio)
else:
    print("O caminho especificado não é um diretório válido.")
