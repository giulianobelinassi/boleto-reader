# Boleto reader: OCR para leitura dos números de boleto

Uso: clique em 'Ler Código', e selecione o número do boleto. Em seguida,
copie o código lido em uma das caixas e cole no sistema de pagamentos.

## Dependencias:
### Linux

Instale o python3, gnome-screenshot, tesseract-ocr e tesseract-ocr-por:

```
$ sudo apt install python3 gnome-screenshot tesseract-ocr tesseract-ocr-por
```

em seguida, abra o boleto-reader.py com

```
python3 boleto-reader.py
```
### Windows

Baixe o pacote em releases, extraia e execute o 'boleto-reader.exe'.

Porém, para construir o binário, você precisará do pyinstaller. Instale
usando o pip e execute o 'build-windows.bat'. Os arquivos serão gerados
na pasta `dist`.

