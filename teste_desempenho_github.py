"""
Teste de Desempenho do GitHub usando Selenium
Mede o tempo de carregamento de páginas e ações no GitHub
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import traceback

class TesteDesempenhoGitHub:
    def __init__(self):
        """Inicializa o driver do Selenium"""
        chrome_options = Options()
        # Descomente a linha abaixo para executar em modo headless (sem abrir o navegador)
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Usa webdriver-manager para gerenciar o ChromeDriver automaticamente
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.resultados = {}
        
    def medir_tempo_carregamento(self, url, nome_teste):
        """
        Mede o tempo de carregamento de uma página
        
        Args:
            url: URL da página a ser testada
            nome_teste: Nome identificador do teste
        """
        print(f"\n🔄 Testando: {nome_teste}")
        print(f"   URL: {url}")
        
        inicio = time.time()
        try:
            self.driver.get(url)
            
            # Aguarda até que a página esteja completamente carregada
            WebDriverWait(self.driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            
            # Pequena pausa adicional para garantir que tudo carregou
            time.sleep(1)
            
            fim = time.time()
            tempo_carregamento = fim - inicio
            
            # Verifica a URL atual para confirmar navegação
            url_atual = self.driver.current_url
            print(f"   URL atual: {url_atual}")
            
            self.resultados[nome_teste] = {
                'url': url_atual,
                'tempo_segundos': round(tempo_carregamento, 2),
                'tempo_milissegundos': round(tempo_carregamento * 1000, 2)
            }
            
            print(f"   ✅ Tempo de carregamento: {tempo_carregamento:.2f}s ({tempo_carregamento*1000:.2f}ms)")
            return tempo_carregamento
        except Exception as e:
            print(f"   ❌ Erro ao carregar página: {str(e)}")
            traceback.print_exc()
            return None
    
    def testar_pagina_inicial(self):
        """Testa o tempo de carregamento da página inicial do GitHub"""
        return self.medir_tempo_carregamento(
            'https://github.com',
            'Página Inicial do GitHub'
        )
    
    def testar_busca_repositorio(self, termo_busca='selenium'):
        """
        Testa o tempo de busca e carregamento de resultados
        
        Args:
            termo_busca: Termo a ser pesquisado
        """
        print(f"\n🔍 Testando busca por: '{termo_busca}'")
        
        inicio = time.time()
        try:
            # Navega diretamente para a URL de busca (mais confiável)
            url_busca = f'https://github.com/search?q={termo_busca}&type=repositories'
            print(f"   URL: {url_busca}")
            
            self.driver.get(url_busca)
            
            # Aguarda a página carregar completamente
            WebDriverWait(self.driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            
            # Aguarda os resultados aparecerem (tenta vários seletores possíveis)
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="results-list"]')),
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.repo-list-item')),
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.Box-row')),
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="search-result"]')),
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'h3 a[href*="/"]'))
                    )
                )
            except:
                # Se não encontrar resultados específicos, pelo menos espera que a página carregue
                time.sleep(2)
            
            fim = time.time()
            tempo_busca = fim - inicio
            
            # Verifica se realmente navegou
            url_atual = self.driver.current_url
            print(f"   URL atual: {url_atual}")
            
            self.resultados[f'Busca: {termo_busca}'] = {
                'url': url_atual,
                'tempo_segundos': round(tempo_busca, 2),
                'tempo_milissegundos': round(tempo_busca * 1000, 2)
            }
            
            print(f"   ✅ Tempo de busca: {tempo_busca:.2f}s ({tempo_busca*1000:.2f}ms)")
            return tempo_busca
        except Exception as e:
            print(f"   ❌ Erro na busca: {str(e)}")
            traceback.print_exc()
            return None
    
    def testar_pagina_repositorio(self, repo='microsoft/vscode'):
        """
        Testa o tempo de carregamento de uma página de repositório específica
        
        Args:
            repo: Nome do repositório (formato: usuario/repositorio)
        """
        url = f'https://github.com/{repo}'
        return self.medir_tempo_carregamento(url, f'Repositório: {repo}')
    
    def executar_todos_testes(self):
        """Executa todos os testes de desempenho"""
        print("=" * 60)
        print("🚀 INICIANDO TESTES DE DESEMPENHO DO GITHUB")
        print("=" * 60)
        
        # Teste 1: Página inicial
        print("\n📍 Teste 1/4")
        self.testar_pagina_inicial()
        time.sleep(3)  # Pausa entre testes
        
        # Teste 2: Busca de repositório
        print("\n📍 Teste 2/4")
        self.testar_busca_repositorio('python')
        time.sleep(3)
        
        # Teste 3: Página de repositório específico
        print("\n📍 Teste 3/4")
        self.testar_pagina_repositorio('microsoft/vscode')
        time.sleep(3)
        
        # Teste 4: Outro repositório popular
        print("\n📍 Teste 4/4")
        self.testar_pagina_repositorio('facebook/react')
        time.sleep(2)
        
        self.exibir_resultados()
    
    def exibir_resultados(self):
        """Exibe um resumo dos resultados dos testes"""
        print("\n" + "=" * 60)
        print("📊 RESULTADOS DOS TESTES DE DESEMPENHO")
        print("=" * 60)
        
        tempos = []
        for teste, dados in self.resultados.items():
            tempo_s = dados['tempo_segundos']
            tempo_ms = dados['tempo_milissegundos']
            tempos.append(tempo_s)
            print(f"\n{teste}:")
            print(f"  ⏱️  Tempo: {tempo_s:.2f}s ({tempo_ms:.2f}ms)")
            print(f"  🔗 URL: {dados['url']}")
        
        if tempos:
            print("\n" + "-" * 60)
            print(f"📈 Estatísticas:")
            print(f"  ⏱️  Tempo médio: {sum(tempos)/len(tempos):.2f}s")
            print(f"  ⚡ Tempo mínimo: {min(tempos):.2f}s")
            print(f"  🐌 Tempo máximo: {max(tempos):.2f}s")
            print("=" * 60)
        
        # Salva resultados em JSON
        with open('resultados_teste.json', 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
        print("\n💾 Resultados salvos em 'resultados_teste.json'")
    
    def fechar(self):
        """Fecha o navegador"""
        self.driver.quit()
        print("\n✅ Testes concluídos e navegador fechado!")


def main():
    """Função principal"""
    teste = TesteDesempenhoGitHub()
    
    try:
        teste.executar_todos_testes()
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro durante os testes: {str(e)}")
    finally:
        teste.fechar()


if __name__ == '__main__':
    main()

