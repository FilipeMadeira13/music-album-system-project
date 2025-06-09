# 🎵 Projeto de Análise de Álbuns Musicais

Este projeto coleta, organiza e analisa dados de álbuns musicais com foco em visualização interativa e estatísticas por gênero, artista e década.

## 🧠 O que você aprende neste projeto

- Leitura e escrita de arquivos JSON
- Estruturação de CRUD em Python
- Organização modular de código
- Análise de dados com Pandas
- Visualização interativa com Plotly
- Boas práticas com funções e tipagem
- Estrutura profissional de projetos de dados

## 📌 Tecnologias utilizadas

- Python 3.11
- Pandas
- Plotly
- JSON (armazenamento)
- Jupyter Notebook

## 🧱 Estrutura do Projeto

```
src/ # Módulos Python (CRUD, análise, visualização)
data/ # Arquivo albums.json
notebooks/ # Análises exploratórias
main.py # Aplicação interativa em terminal
```

## 📊 Funcionalidades

- Adicionar, listar, filtrar e remover álbuns
- Armazenamento em JSON
- Estatísticas descritivas com Pandas
- Visualização com Plotly (gênero, artista, ano, década)

## 📷 Exemplos

### Lançamentos por Década

![plot](img/plot_decada.png)

### Álbuns por Gênero

![plot](img/plot_genero.png)

## 🛠️ Como executar

```bash
git clone https://github.com/FilipeMadeira13/music-album-system-project.git
cd music-album-system-project
poetry install --no-root
python main.py
```

## 📈 Para análise via notebook

```
Abra o notebooks/exploratory_analysis.ipynb
```

## 🚀 Próximos passos

- 🔄 Migrar de JSON para SQLite
- 📊 Criar análises com SQL e Pandas
- 🌐 Integrar com API do Spotify
- 🖼️ Criar dashboard com Streamlit

Feito por Filipe Madeira – 2025
