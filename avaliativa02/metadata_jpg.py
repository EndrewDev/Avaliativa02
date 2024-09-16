import os, sys

# ------------------------------------------------------------------------------------------
DIR_APP = os.path.dirname(os.path.abspath(__file__))
DIR_IMG = DIR_APP + '\\Imagens'

# ------------------------------------------------------------------------------------------
# Opção escolher uma imagem para verificar
opcao = input("Qual prefere:\n1 - vista_natal_rn.jp\n2 - LMC_20221219_202142_v7.jpg\nDigite a opção: ")

if  opcao == "1":
    strNomeArq = DIR_IMG + "\\vista_natal_rn.jpg"
elif opcao == "2":
    strNomeArq = DIR_IMG + "\\LMC_20221219_202142_v7.jpg"
else:
    print("\nOpção Inválida! Tente novamente.")

try:
    fileContent = open(strNomeArq, 'rb')
except FileNotFoundError:
    print('\nERRO: Arquivo Não Existe...\n')
    sys.exit()
except:
    print(f'\nERRO: {sys.exc_info()[1]}...\n')
    sys.exit()
else:
    # Verificando se o arquivo informado é JPG 
    if fileContent.read(2) != b'\xFF\xD8':
        print('\nERRO: Arquivo informado não é JPG...\n')
        sys.exit()

    # Verifica se o arquivo possui metadados
    if fileContent.read(2) != b'\xFF\xE1':
        fileContent.close()
        print('\nAVISO: Este arquivo não possui metadados...\n')
        sys.exit()

    # Obtendo EXIF
    exifSize      = fileContent.read(2)
    exifHeader    = fileContent.read(4) # EXIF Header (marcador EXIF)
    temp1         = fileContent.read(2) # EXIF Header (fixo)
    tiffHeader    = fileContent.read(2) # (49 49: Little Endian - Intel / 4D 4D: Big Endian - Motorola)
    temp2         = fileContent.read(2) # TIFF Header (fixo)
    temp3         = fileContent.read(4) # TIFF Header (fixo)
    countMetadata = fileContent.read(2) # Metadata Count

    if tiffHeader == b'\x49\x49':
        exifSize      = int.from_bytes(exifSize, byteorder='little')
        countMetadata = int.from_bytes(countMetadata, byteorder='little')
    else:
        exifSize      = int.from_bytes(exifSize, byteorder='big')
        countMetadata = int.from_bytes(countMetadata, byteorder='big')

    dicEXIF = { 'exifSize' : exifSize, 'exifMarker': exifHeader, 
                'temp1'    : temp1   , 'tiffHeader': tiffHeader, 
                'temp2'    : temp2   , 'temp3'     : temp3,
                'metaCount': countMetadata}

    # Obtendo os Metadados
    lstMetadata   = list()
    lstMetaHeader = ['TAGNumber', 'DataFormat', 'NumberComponents', 'DataValue']
    for _ in range(countMetadata):
        idTAGNumber      = fileContent.read(2) # Identificador do Metadado
        idDataFormat     = fileContent.read(2) # Tipo do Metadado
        numberComponents = fileContent.read(4) # Qt. Repetições do Metadado
        dataValue        = fileContent.read(4) # Valor do Metadado / Se maior que 4 bytes -> indica Offset
        lstTemp = [idTAGNumber, idDataFormat, numberComponents, dataValue]
        lstMetadata.append(dict(zip(lstMetaHeader, lstTemp)))

    # Imprimindo os resultados
    print('\n\n', dicEXIF, '\n\n')
    
    # Imprimindo os metadatas lidos
    for metaData in lstMetadata: print(metaData)
    print('\n\n')