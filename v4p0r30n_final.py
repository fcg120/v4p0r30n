import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pandas as pd
import webbrowser
from bs4 import BeautifulSoup  # Importar BeautifulSoup para análise HTML

# Função para abrir o link do mestrado profissional
def abrir_link_mestrado():
    webbrowser.open("https://mpeh.unifei.edu.br")

# Função para abrir o link da logo da universidade
def abrir_link_universidade():
    webbrowser.open("https://unifei.edu.br")

# Função para selecionar o arquivo HEC-HAS
def selecionar_arquivo_hechas():
    arquivo_hechas = filedialog.askopenfilename(filetypes=[("Arquivos do HEC-HAS", "*.res")])
    if arquivo_hechas:
        # Ler os dados do arquivo HEC-HAS
        dados = ler_dados_hechas(arquivo_hechas)

        # Caminho de saída CSV
        arquivo_csv = 'dados_convertidos_hechas.csv'

        # Escrever os dados no arquivo CSV
        dados.to_csv(arquivo_csv, index=False)

        # Mensagem de conclusão
        resultado_label.config(text=f"Dados do HEC-HAS convertidos e salvos em {arquivo_csv}")

# Função para ler os dados do arquivo HEC-HAS
def ler_dados_hechas(arquivo):
    dados = []
    Lendo_dados = False
    with open(arquivo, 'r') as f:
        for linha in f:
            linha = linha.strip()
            if linha.startswith("BEGIN DSS'"):
                Lendo_dados = True
                continue
            if linha.startswith("END DSS"):
                Lendo_dados = False
                continue
            if Lendo_dados and not linha.startswith("Pathname") and not linha.startswith("Type") and not linha.startswith("Units") and not linha.startswith("X Ordinate") and not linha.startswith("Y Ordinate") and linha:
                partes = linha.split()
                data_hora = partes[0] +""+ partes[1]
                valor = partes[2]
                dados.append([data_hora, valor])
    return pd.DataFrame(dados, columns=["Data_hora", "Valor"])

# Função para selecionar o arquivo HEC-HMS
def selecionar_arquivo_hmshms():
    arquivo_hmshms = filedialog.askopenfilename(filetypes=[("Arquivos do HEC-HMS", "*.html;*.txt")])
    if arquivo_hmshms:
        # Ler os dados do arquivo HEC-HMS
        dados = ler_dados_hmshms(arquivo_hmshms)

        # Caminho de saída CSV
        arquivo_csv = 'dados_convertidos_hmshms.csv'

        # Escrever os dados no arquivo CSV
        dados.to_csv(arquivo_csv, index=False)

        # Mensagem de conclusão
        resultado_label.config(text=f"Dados do HEC-HMS convertidos e salvos em {arquivo_csv}")

# Função para ler os dados do arquivo HEC-HMS
def ler_dados_hmshms(arquivo):
    # Verifica a extensão do arquivo para determinar o tipo de processamento necessário
    if arquivo.endswith('.html'):
        return ler_dados_hmshms_html(arquivo)
    elif arquivo.endswith('.txt'):
        return ler_dados_hmshms_txt(arquivo)
    else:
        raise ValueError("Formato de arquivo não suportado")

# Função para ler os dados do arquivo HEC-HMS em formato HTML
def ler_dados_hmshms_html(arquivo):
    with open(arquivo, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
        # Suponha que os dados estejam em uma tabela com uma classe específica
        table = soup.find('table', class_='dados-hechms')
        
        # Extrair os dados da tabela
        dados = []
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) == 2:  # Supondo que há duas colunas: data/hora e valor
                data_hora = cols[0].text.strip()
                valor = cols[1].text.strip()
                dados.append([data_hora, valor])
                
        # Converter para DataFrame pandas
        return pd.DataFrame(dados, columns=["Data_hora", "Valor"])

# Função para ler os dados do arquivo HEC-HMS em formato TXT
def ler_dados_hmshms_txt(arquivo):
    dados = []
    with open(arquivo, 'r') as f:
        for linha in f:
            partes = linha.split()
            if len(partes) == 2:  # Supondo que há duas colunas: data/hora e valor
                data_hora = partes[0]
                valor = partes[1]
                dados.append([data_hora, valor])
    
    # Converter para DataFrame pandas
    return pd.DataFrame(dados, columns=["Data_hora", "Valor"])

# Inicializar a interface gráfica
root = tk.Tk()
root.title("Addon v4p0r30n")

# Adicionar o texto e a imagem centralizada
texto = "Olá, bem-vindo ao addon v4p0r30n de transformação de arquivos do HEC-HAS e HEC-HMS em tabela CSV"
label_texto = tk.Label(root, text=texto, font=("Arial", 16), wraplength=500, justify="center")
label_texto.pack()

imagem_centralizada = Image.open("G:\\Meu Drive\\Mestrado UNIFEI\\00 - TESE\\01-PYTHON\\01-v4p0r30n\\A.png")  # Substitua "sua_imagem_centralizada.png" pelo caminho da sua imagem centralizada
photo_centralizada = ImageTk.PhotoImage(imagem_centralizada)
label_imagem_centralizada = tk.Label(root, image=photo_centralizada)
label_imagem_centralizada.pack()

# Botões para selecionar os arquivos do HEC-HAS e do HEC-HMS
botao_selecionar_hechas = tk.Button(root, text="Selecionar Arquivo HEC-HAS", command=selecionar_arquivo_hechas)
botao_selecionar_hechas.pack()

botao_selecionar_hmshms = tk.Button(root, text="Selecionar Arquivo HEC-HMS", command=selecionar_arquivo_hmshms)
botao_selecionar_hmshms.pack()

# Label para exibir o resultado
resultado_label = tk.Label(root, text="")
resultado_label.pack()

# Adicionar as imagens no rodapé com links
frame_rodape = tk.Frame(root)
frame_rodape.pack(side=tk.BOTTOM, pady=20)

# Adicionar a imagem do mestrado
imagem_mestrado = Image.open("G:\\Meu Drive\\Mestrado UNIFEI\\00 - TESE\\01-PYTHON\\01-v4p0r30n\\c.png")  
imagem_mestrado.thumbnail((150, 150))  # Redimensionar a imagem se necessário
photo_mestrado = ImageTk.PhotoImage(imagem_mestrado)
label_imagem_mestrado = tk.Label(frame_rodape, image=photo_mestrado, cursor="hand2")
label_imagem_mestrado.bind("<Button-1>", lambda e: abrir_link_mestrado())
label_imagem_mestrado.pack(side=tk.LEFT, padx=10)

# Adicionar a imagem da universidade
imagem_universidade = Image.open("G:\\Meu Drive\\Mestrado UNIFEI\\00 - TESE\\01-PYTHON\\01-v4p0r30n\\b.png")  
imagem_universidade.thumbnail((150, 150))  # Redimensionar a imagem se necessário
photo_universidade = ImageTk.PhotoImage(imagem_universidade)
label_imagem_universidade = tk.Label(frame_rodape, image=photo_universidade, cursor="hand2")
label_imagem_universidade.bind("<Button-1>", lambda e: abrir_link_universidade())
label_imagem_universidade.pack(side=tk.RIGHT, padx=10)

# Executar a interface gráfica
root.mainloop()