# Teste de Desempenho do GitHub

Script simples para medir o tempo de carregamento de páginas do GitHub usando Selenium.

## 📋 Pré-requisitos

- Python 3.7 ou superior
- Google Chrome instalado
- ChromeDriver (pode ser instalado automaticamente com webdriver-manager)

## 🚀 Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 💻 Como usar

Execute o script:
```bash
python teste_desempenho_github.py
```

O script irá:
- Abrir o navegador Chrome
- Testar o tempo de carregamento da página inicial do GitHub
- Testar o tempo de busca de repositórios
- Testar o tempo de carregamento de páginas de repositórios específicos
- Exibir os resultados e salvar em `resultados_teste.json`

## 📊 O que é medido

- Tempo de carregamento da página inicial
- Tempo de busca e carregamento de resultados
- Tempo de carregamento de páginas de repositórios

## 📝 Personalização

Você pode modificar o arquivo `teste_desempenho_github.py` para:
- Adicionar mais testes
- Mudar os repositórios testados
- Alterar os termos de busca
- Executar em modo headless (sem abrir o navegador)

Para executar em modo headless, descomente a linha no código:
```python
chrome_options.add_argument('--headless')
```

## 📄 Resultados

Os resultados são salvos automaticamente em `resultados_teste.json` com os tempos medidos em segundos e milissegundos.

