#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import json
import urllib.parse
import math
import csv
import os
from pathlib import Path
from io import BytesIO
import openpyxl
from openpyxl.styles import Font, Alignment
import multiprocessing as mp
from functools import lru_cache
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

# Configuração do servidor
PORT = 8000

# Cache global para tábuas de comutação (otimização de performance)
TABUAS_CACHE = {}

class TabuladeComutacao:
    def __init__(self, taxa_juros, tabua_selecionada=None):
        self.taxa_juros = taxa_juros
        self.v = 1 / (1 + taxa_juros)
        self.tabuas_disponiveis = {}
        self.tabua_padrao = None
        self.carregar_todas_tabuas()
        self.tabua_selecionada = tabua_selecionada if tabua_selecionada else self.tabua_padrao
        self.dados = self.obter_dados_tabua()
        self.calcular_tabua_comutacao()
    
    def carregar_todas_tabuas(self):
        try:
            # Tentar carregar do arquivo CSV
            csv_path = Path(__file__).parent / "tabuas_mortalidade_completas.csv"
            if csv_path.exists():
                with open(csv_path, "r", encoding="utf-8") as f:
                    linhas = f.readlines()
                
                for linha in linhas[1:]:
                    partes = linha.strip().split(",")
                    if len(partes) == 4:
                        tabua_nome = partes[0]
                        idade = int(partes[1])
                        qx_masc = float(partes[2])
                        qx_fem = float(partes[3])
                        
                        if tabua_nome not in self.tabuas_disponiveis:
                            self.tabuas_disponiveis[tabua_nome] = {"masculino": {}, "feminino": {}}
                            # Define a primeira tábua como padrão
                            if self.tabua_padrao is None:
                                self.tabua_padrao = tabua_nome
                        
                        self.tabuas_disponiveis[tabua_nome]["masculino"][idade] = qx_masc
                        self.tabuas_disponiveis[tabua_nome]["feminino"][idade] = qx_fem
            else:
                print("Arquivo de tábuas não encontrado. Usando tábua padrão.")
                self.carregar_tabua_padrao()
        except Exception as e:
            print(f"Erro ao carregar tábuas: {e}. Usando tábua padrão.")
            self.carregar_tabua_padrao()
    
    def carregar_tabua_padrao(self):
        # Cria uma tábua padrão genérica
        tabua_padrao_nome = "Tábua Padrão"
        self.tabuas_disponiveis[tabua_padrao_nome] = {
            "masculino": {},
            "feminino": {}
        }
        dados_padrao = self.carregar_tabua_mortalidade()
        self.tabuas_disponiveis[tabua_padrao_nome] = dados_padrao
        self.tabua_padrao = tabua_padrao_nome
    
    def obter_dados_tabua(self):
        if self.tabua_selecionada in self.tabuas_disponiveis:
            return self.tabuas_disponiveis[self.tabua_selecionada]
        else:
            return self.carregar_tabua_mortalidade()
    
    def carregar_tabua_mortalidade(self):
        dados = {
            'masculino': {},
            'feminino': {}
        }
        # Dados da tábua BR-EMS 2021 (simplificada)
        tabua_data = [
            (0, 0.000371, 0.000355), (1, 0.000242, 0.000226), (2, 0.000213, 0.000195),
            (3, 0.000199, 0.000180), (4, 0.000192, 0.000171), (5, 0.000188, 0.000165),
            (6, 0.000186, 0.000162), (7, 0.000185, 0.000160), (8, 0.000185, 0.000159),
            (9, 0.000186, 0.000159), (10, 0.000188, 0.000160), (11, 0.000191, 0.000162),
            (12, 0.000195, 0.000165), (13, 0.000200, 0.000169), (14, 0.000206, 0.000174),
            (15, 0.000213, 0.000180), (16, 0.000221, 0.000187), (17, 0.000230, 0.000195),
            (18, 0.000240, 0.000204), (19, 0.000251, 0.000214), (20, 0.000263, 0.000225),
            (21, 0.000276, 0.000237), (22, 0.000290, 0.000250), (23, 0.000305, 0.000264),
            (24, 0.000321, 0.000279), (25, 0.000338, 0.000295), (26, 0.000356, 0.000312),
            (27, 0.000375, 0.000330), (28, 0.000395, 0.000349), (29, 0.000416, 0.000369),
            (30, 0.000438, 0.000390), (31, 0.000461, 0.000412), (32, 0.000485, 0.000435),
            (33, 0.000510, 0.000459), (34, 0.000536, 0.000484), (35, 0.000563, 0.000510),
            (36, 0.000591, 0.000537), (37, 0.000620, 0.000565), (38, 0.000650, 0.000594),
            (39, 0.000681, 0.000624), (40, 0.000713, 0.000655), (41, 0.000746, 0.000687),
            (42, 0.000780, 0.000720), (43, 0.000815, 0.000754), (44, 0.000851, 0.000789),
            (45, 0.000888, 0.000825), (46, 0.000926, 0.000862), (47, 0.000965, 0.000900),
            (48, 0.001005, 0.000939), (49, 0.001046, 0.000979), (50, 0.001088, 0.001020),
            (51, 0.001131, 0.001062), (52, 0.001175, 0.001105), (53, 0.001220, 0.001149),
            (54, 0.001266, 0.001194), (55, 0.001313, 0.001240), (56, 0.001361, 0.001287),
            (57, 0.001410, 0.001335), (58, 0.001460, 0.001384), (59, 0.001511, 0.001434),
            (60, 0.001563, 0.001485), (61, 0.001616, 0.001537), (62, 0.001670, 0.001590),
            (63, 0.001725, 0.001644), (64, 0.001781, 0.001699), (65, 0.001838, 0.001755),
            (66, 0.001896, 0.001812), (67, 0.001955, 0.001870), (68, 0.002015, 0.001989),
            (69, 0.002076, 0.001989), (70, 0.002138, 0.002050), (71, 0.002201, 0.002112),
            (72, 0.002265, 0.002175), (73, 0.002330, 0.002239), (74, 0.002396, 0.002304),
            (75, 0.002463, 0.002370), (76, 0.002531, 0.002437), (77, 0.002600, 0.002505),
            (78, 0.002670, 0.002574), (79, 0.002741, 0.002644), (80, 0.002813, 0.002715),
            (81, 0.002886, 0.002787), (82, 0.002960, 0.002860), (83, 0.003035, 0.002934),
            (84, 0.003111, 0.003009), (85, 0.003188, 0.003085), (86, 0.003266, 0.003162),
            (87, 0.003345, 0.003240), (88, 0.003425, 0.003319), (89, 0.003506, 0.003399),
            (90, 0.003588, 0.003480), (91, 0.003671, 0.003562), (92, 0.003755, 0.003645),
            (93, 0.003840, 0.003729), (94, 0.003926, 0.003814), (95, 0.004013, 0.003900),
            (96, 0.004101, 0.003987), (97, 0.004190, 0.004075), (98, 0.004280, 0.004164),
            (99, 0.004371, 0.004254), (100, 0.004463, 0.004345), (101, 0.004556, 0.004437),
            (102, 0.004650, 0.004530), (103, 0.004745, 0.004624), (104, 0.004841, 0.004719),
            (105, 0.004938, 0.004815), (106, 0.005036, 0.004912), (107, 0.005135, 0.005010),
            (108, 0.005235, 0.005109), (109, 0.005336, 0.005209), (110, 0.005438, 0.005310),
            (111, 0.005541, 0.005412), (112, 0.005645, 0.005515), (113, 0.005750, 0.005619),
            (114, 0.005856, 0.005724), (115, 0.005963, 0.005830), (116, 0.006071, 0.005937),
            (117, 0.006180, 0.006045), (118, 0.006290, 0.006154), (119, 0.006401, 0.006264),
            (120, 0.006513, 0.006375), (121, 0.006626, 0.006487), (122, 0.006740, 0.006600),
            (123, 0.006855, 0.006714), (124, 0.006971, 0.006829), (125, 1.000000, 1.000000)
        ]
        for idade, qx_masc, qx_fem in tabua_data:
            dados['masculino'][idade] = qx_masc
            dados['feminino'][idade] = qx_fem
        return dados
    
    def obter_qx(self, idade, sexo):
        if sexo == 'M':
            return self.dados['masculino'].get(idade, 1.0)
        else:
            return self.dados['feminino'].get(idade, 1.0)
    
    def calcular_tabua_comutacao(self):
        self.l_x = {0: 100000}  # Radix
        self.d_x = {}
        self.D_x = {}
        self.C_x = {}
        self.N_x = {}
        self.M_x = {}
        self.v_x = {}
        
        sexo = 'M'  # Default para cálculo inicial, será ajustado na chamada
        
        # Calcular l_x e d_x
        for idade in range(0, 126):
            if idade > 0:
                qx_anterior = self.obter_qx(idade - 1, sexo)
                self.l_x[idade] = self.l_x[idade - 1] * (1 - qx_anterior)
            
            qx = self.obter_qx(idade, sexo)
            self.d_x[idade] = self.l_x[idade] * qx
        
        # Calcular D_x, C_x e v_x
        for idade in range(0, 126):
            self.D_x[idade] = self.l_x[idade] * (self.v ** idade)
            self.C_x[idade] = self.d_x[idade] * (self.v ** (idade + 1))
            self.v_x[idade] = self.v ** idade
        
        # Calcular N_x e M_x
        for idade in range(0, 126):
            self.N_x[idade] = sum(self.D_x.get(x, 0) for x in range(idade, 126))
            self.M_x[idade] = sum(self.C_x.get(x, 0) for x in range(idade, 126))

def calcular_seguro_anual(tabua_obj, idade, sexo, periodo):
    tabua_obj.dados = tabua_obj.tabuas_disponiveis[tabua_obj.tabua_selecionada]
    tabua_obj.calcular_tabua_comutacao()  # Recalcular com o sexo correto
    seguro_anual = (tabua_obj.M_x[idade] - tabua_obj.M_x[idade + periodo]) / tabua_obj.D_x[idade]
    return seguro_anual

def calcular_seguro_fracionado_total(taxa_juros, fracionamento, seguro_anual):
    taxa_fracionada = fracionamento * ((1 + taxa_juros)**(1/fracionamento) - 1)
    fator_ajuste = taxa_juros / taxa_fracionada
    seguro_fracionado_total = fator_ajuste * seguro_anual
    return seguro_fracionado_total, fator_ajuste, taxa_fracionada

def calcular_premio_mensal(tabua_obj, idade, periodo, valor_fracionado_total, taxa_juros, fracionamento, soma_segurada):
    N_x = tabua_obj.N_x[idade]
    N_x_n = tabua_obj.N_x[idade + periodo]
    D_x = tabua_obj.D_x[idade]
    D_x_n = tabua_obj.D_x[idade + periodo]
    
    anuidade_ajustada = ((N_x - N_x_n) / D_x + (11/24 * (1 - D_x_n / D_x))) * fracionamento
    valor_mensal = valor_fracionado_total / anuidade_ajustada if anuidade_ajustada != 0 else 0
    
    percentual_mensal = calcular_percentual_mensal(valor_mensal, taxa_juros, fracionamento, periodo, soma_segurada)
    
    return valor_mensal, N_x, N_x_n, anuidade_ajustada, percentual_mensal

def calcular_percentual_mensal(valor_mensal, taxa_juros, fracionamento, periodo, soma_segurada):
    taxa_fracionada = (1 + taxa_juros)**(1/fracionamento) - 1
    num_pagamentos = fracionamento * periodo
    
    if taxa_fracionada == 0:
        pgto = soma_segurada / num_pagamentos
    else:
        pgto = soma_segurada * taxa_fracionada * (1 + taxa_fracionada)**num_pagamentos / ((1 + taxa_fracionada)**num_pagamentos - 1)
    
    if pgto == 0:
        return 0, taxa_fracionada, num_pagamentos, pgto
    
    percentual = valor_mensal / pgto
    return percentual, taxa_fracionada, num_pagamentos, pgto

@lru_cache(maxsize=1000)
def calcular_taxas_seguro_cached(tabua_nome, idade, sexo, periodo, taxa_juros, soma_segurada=100000):
    """
    Versão otimizada com cache da função calcular_taxas_seguro.
    Cache baseado nos parâmetros de entrada para evitar recálculos.
    """
    try:
        # Usar cache global para tábuas
        cache_key = f"{tabua_nome}_{taxa_juros}_{sexo}"
        
        if cache_key not in TABUAS_CACHE:
            # Criar nova instância da tábua
            tabua_obj = TabuladeComutacao(taxa_juros, tabua_nome)
            tabua_obj.tabua_selecionada = tabua_nome
            tabua_obj.dados = tabua_obj.tabuas_disponiveis[tabua_nome]
            tabua_obj.calcular_tabua_comutacao()
            TABUAS_CACHE[cache_key] = tabua_obj
        else:
            tabua_obj = TABUAS_CACHE[cache_key]
        
        # Calcular seguro anual
        seguro_anual = calcular_seguro_anual(tabua_obj, idade, sexo, periodo)
        
        # Calcular seguro fracionado total (taxa à vista)
        seguro_fracionado_total, _, _ = calcular_seguro_fracionado_total(taxa_juros, 12, seguro_anual)
        
        # Calcular valor monetário à vista
        valor_monetario_vista = soma_segurada * seguro_fracionado_total
        
        # Calcular prêmio mensal
        valor_mensal, _, _, _, percentual_mensal_calc = calcular_premio_mensal(
            tabua_obj, idade, periodo, valor_monetario_vista, taxa_juros, 12, soma_segurada
        )
        
        return {
            'taxa_vista': seguro_fracionado_total,
            'taxa_mensal': percentual_mensal_calc[0] if percentual_mensal_calc else 0
        }
        
    except Exception as e:
        return {
            'taxa_vista': 0.0,
            'taxa_mensal': 0.0
        }

def calcular_taxas_seguro(tabua_obj, idade, sexo, periodo, taxa_juros, soma_segurada=100000):
    """
    Wrapper para manter compatibilidade com código existente.
    Agora usa a versão otimizada com cache.
    """
    return calcular_taxas_seguro_cached(
        tabua_obj.tabua_selecionada, idade, sexo, periodo, taxa_juros, soma_segurada
    )

def processar_combinacao_paralela(args):
    """
    Função para processar uma única combinação em paralelo.
    Args: (tabua_nome, idade, sexo, periodo, taxa_juros, tipo_tabua, soma_segurada)
    """
    try:
        tabua_nome, idade, sexo, periodo, taxa_juros, tipo_tabua, soma_segurada = args
        
        # Calcular taxas usando a versão otimizada
        taxas = calcular_taxas_seguro_cached(tabua_nome, idade, sexo, periodo, taxa_juros, soma_segurada)
        
        return {
            "idade": idade,
            "sexo": sexo,
            "periodo": periodo,
            "tipo_tabua": tipo_tabua,
            "tabua": tabua_nome,
            "taxa_vista": f"{taxas['taxa_vista']*100:.4f}%",
            "taxa_mensal": f"{taxas['taxa_mensal']*100:.4f}%"
        }
    except Exception as e:
        return None

def calcular_coletivo_paralelo(idade_min, idade_max, sexos, periodo_min, periodo_max, 
                              taxa_juros, tabuas_validas, tabuas_invalidas, max_workers=None):
    """
    Versão otimizada do cálculo coletivo usando paralelismo.
    """
    if max_workers is None:
        max_workers = min(mp.cpu_count(), 8)  # Limitar a 8 workers para não sobrecarregar
    
    # Preparar todas as combinações
    combinacoes = []
    
    # Adicionar combinações para tábuas válidas
    for tabua in tabuas_validas:
        for idade in range(idade_min, idade_max + 1):
            for sexo in sexos:
                for periodo in range(periodo_min, periodo_max + 1):
                    combinacoes.append((tabua, idade, sexo, periodo, taxa_juros, "Válido", 100000))
    
    # Adicionar combinações para tábuas inválidas
    for tabua in tabuas_invalidas:
        for idade in range(idade_min, idade_max + 1):
            for sexo in sexos:
                for periodo in range(periodo_min, periodo_max + 1):
                    combinacoes.append((tabua, idade, sexo, periodo, taxa_juros, "Inválido", 100000))
    
    print(f"🚀 Processando {len(combinacoes)} combinações com {max_workers} workers paralelos...")
    inicio = time.time()
    
    # Processar em paralelo
    resultados = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submeter todas as tarefas
        future_to_combinacao = {
            executor.submit(processar_combinacao_paralela, comb): comb 
            for comb in combinacoes
        }
        
        # Coletar resultados conforme completam
        for i, future in enumerate(as_completed(future_to_combinacao)):
            resultado = future.result()
            if resultado is not None:
                resultados.append(resultado)
            
            # Mostrar progresso
            if (i + 1) % 50 == 0 or i == len(combinacoes) - 1:
                progresso = ((i + 1) / len(combinacoes)) * 100
                print(f"Progresso: {progresso:.1f}% ({i + 1}/{len(combinacoes)})")
    
    fim = time.time()
    tempo_total = fim - inicio
    print(f"✅ Processamento concluído em {tempo_total:.2f} segundos")
    print(f"⚡ Velocidade: {len(combinacoes)/tempo_total:.1f} combinações/segundo")
    
    return resultados

def limpar_cache_tabuas():
    """Limpa o cache de tábuas para liberar memória."""
    global TABUAS_CACHE
    TABUAS_CACHE.clear()
    calcular_taxas_seguro_cached.cache_clear()
    print("🧹 Cache de tábuas limpo")

def obter_estatisticas_cache():
    """Retorna estatísticas do cache."""
    return {
        "tabulas_em_cache": len(TABUAS_CACHE),
        "cache_hits": calcular_taxas_seguro_cached.cache_info().hits,
        "cache_misses": calcular_taxas_seguro_cached.cache_info().misses,
        "tamanho_cache": calcular_taxas_seguro_cached.cache_info().currsize
    }

class CalculadoraHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
            return super().do_GET()
        elif self.path == '/index.html':
            return super().do_GET()
        elif self.path == '/calculadora_individual.html':
            return super().do_GET()
        elif self.path == '/calculadora_coletiva.html':
            return super().do_GET()
        elif self.path == '/tabuas':
            self.obter_tabuas_disponiveis()
        elif self.path == '/download_excel':
            self.handle_download_excel()
        elif self.path == '/cache_stats':
            self.handle_cache_stats()
        elif self.path == '/limpar_cache':
            self.handle_limpar_cache()
        else:
            return super().do_GET()
    
    def obter_tabuas_disponiveis(self):
        try:
            # Criar instância temporária para obter tábuas
            tabua_obj = TabuladeComutacao(0.1)  # Taxa temporária
            tabuas = list(tabua_obj.tabuas_disponiveis.keys())
            
            response = {
                "success": True,
                "tabuas": tabuas,
                "tabua_padrao": tabua_obj.tabua_padrao
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            error_response = {"success": False, "error": str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def handle_calcular_coletivo(self):
        try:
            # Ler dados do POST
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                raise ValueError("Content-Length is 0")
            
            post_data = self.rfile.read(content_length)
            if not post_data:
                raise ValueError("No data received")
            
            data = json.loads(post_data.decode('utf-8'))
            
            # Extrair parâmetros
            idade_min = int(data['idade_min'])
            idade_max = int(data['idade_max'])
            sexos = data['sexos']
            periodo_min = int(data['periodo_min'])
            periodo_max = int(data['periodo_max'])
            taxa_juros = float(data['taxa_juros']) / 100
            tabuas_validas = data['tabuas_validas']
            tabuas_invalidas = data['tabuas_invalidas']
            
            # Validação dos limites
            if not (0 <= idade_min <= idade_max <= 110):
                raise ValueError("As idades devem estar entre 0 e 110 anos, e a idade mínima deve ser menor ou igual à máxima.")
            
            if not (1 <= periodo_min <= periodo_max <= 10):
                raise ValueError("Os períodos devem estar entre 1 e 10 anos, e o período mínimo deve ser menor ou igual ao máximo.")
            
            if not (0 <= taxa_juros <= 0.20):  # 0% a 20%
                raise ValueError("A taxa de juros deve estar entre 0% e 20%.")
            
            if len(sexos) == 0:
                raise ValueError("Selecione pelo menos um sexo.")
            
            if len(tabuas_validas) == 0 and len(tabuas_invalidas) == 0:
                raise ValueError("Selecione pelo menos uma tábua válida ou inválida.")
            
            # Calcular total de combinações
            total_idades = idade_max - idade_min + 1
            total_periodos = periodo_max - periodo_min + 1
            total_sexos = len(sexos)
            total_tabuas = len(tabuas_validas) + len(tabuas_invalidas)
            total_combinacoes = total_idades * total_periodos * total_sexos * total_tabuas
            
            print(f"📊 Iniciando cálculo coletivo otimizado:")
            print(f"   • Idades: {idade_min}-{idade_max} ({total_idades} idades)")
            print(f"   • Períodos: {periodo_min}-{periodo_max} ({total_periodos} períodos)")
            print(f"   • Sexos: {sexos} ({total_sexos} sexos)")
            print(f"   • Tábuas: {len(tabuas_validas)} válidas + {len(tabuas_invalidas)} inválidas")
            print(f"   • Total: {total_combinacoes} combinações")
            
            # Usar versão paralela otimizada
            resultados = calcular_coletivo_paralelo(
                idade_min, idade_max, sexos, periodo_min, periodo_max,
                taxa_juros, tabuas_validas, tabuas_invalidas
            )
            
            # Filtrar resultados válidos
            resultados_validos = [r for r in resultados if r is not None]
            
            # Preparar resposta
            response = {
                "success": True,
                "resultados": resultados_validos,
                "total_combinacoes": total_combinacoes,
                "combinacoes_processadas": len(resultados_validos),
                "progresso": 100.0,
                "idade_min": idade_min,
                "idade_max": idade_max,
                "periodo_min": periodo_min,
                "periodo_max": periodo_max,
                "tabuas_utilizadas": list(set(tabuas_validas + tabuas_invalidas)),
                "otimizado": True,
                "cache_hits": len(TABUAS_CACHE)
            }
            
            # Enviar resposta
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            error_response = {"success": False, "error": str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def handle_calcular_coletivo_progress(self):
        try:
            # Ler dados do POST
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                raise ValueError("Content-Length is 0")
            
            post_data = self.rfile.read(content_length)
            if not post_data:
                raise ValueError("No data received")
            
            data = json.loads(post_data.decode('utf-8'))
            
            # Extrair parâmetros
            idade_min = int(data['idade_min'])
            idade_max = int(data['idade_max'])
            sexos = data['sexos']
            periodo_min = int(data['periodo_min'])
            periodo_max = int(data['periodo_max'])
            taxa_juros = float(data['taxa_juros']) / 100
            tabuas_validas = data['tabuas_validas']
            tabuas_invalidas = data['tabuas_invalidas']
            
            # Validação dos limites
            if not (0 <= idade_min <= idade_max <= 110):
                raise ValueError("As idades devem estar entre 0 e 110 anos, e a idade mínima deve ser menor ou igual à máxima.")
            
            if not (1 <= periodo_min <= periodo_max <= 10):
                raise ValueError("Os períodos devem estar entre 1 e 10 anos, e o período mínimo deve ser menor ou igual ao máximo.")
            
            if not (0 <= taxa_juros <= 0.20):  # 0% a 20%
                raise ValueError("A taxa de juros deve estar entre 0% e 20%.")
            
            if len(sexos) == 0:
                raise ValueError("Selecione pelo menos um sexo.")
            
            if len(tabuas_validas) == 0 and len(tabuas_invalidas) == 0:
                raise ValueError("Selecione pelo menos uma tábua válida ou inválida.")
            
            # Calcular total de combinações para progresso
            total_idades = idade_max - idade_min + 1
            total_periodos = periodo_max - periodo_min + 1
            total_sexos = len(sexos)
            total_tabuas = len(tabuas_validas) + len(tabuas_invalidas)
            total_combinacoes = total_idades * total_periodos * total_sexos * total_tabuas
            
            # Configurar Server-Sent Events
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Calcular todas as combinações
            resultados = []
            tabuas_utilizadas = set()
            combinacoes_processadas = 0
            
            # Processar tábuas válidas
            for tabua in tabuas_validas:
                tabuas_utilizadas.add(tabua)
                for idade in range(idade_min, idade_max + 1):
                    for sexo in sexos:
                        for periodo in range(periodo_min, periodo_max + 1):
                            try:
                                # Calcular seguro usando a nova função unificada
                                tabua_obj = TabuladeComutacao(taxa_juros, tabua)
                                tabua_obj.tabua_selecionada = tabua
                                
                                if tabua not in tabua_obj.tabuas_disponiveis:
                                    # Se a tábua não for encontrada, usar AT-83 como padrão
                                    if 'AT-83' in tabua_obj.tabuas_disponiveis:
                                        tabua = 'AT-83'
                                        tabua_obj.tabua_selecionada = tabua
                                    elif tabua_obj.tabuas_disponiveis:
                                        tabua = list(tabua_obj.tabuas_disponiveis.keys())[0]
                                        tabua_obj.tabua_selecionada = tabua
                                    else:
                                        continue
                                
                                # Usar a função unificada para calcular as taxas
                                taxas = calcular_taxas_seguro(tabua_obj, idade, sexo, periodo, taxa_juros, 100000)
                                
                                resultado = {
                                    "idade": idade,
                                    "sexo": sexo,
                                    "periodo": periodo,
                                    "tipo_tabua": "Válido",
                                    "tabua": tabua,
                                    "taxa_vista": f"{taxas['taxa_vista']*100:.4f}%",
                                    "taxa_mensal": f"{taxas['taxa_mensal']*100:.4f}%"
                                }
                                resultados.append(resultado)
                                
                            except Exception as e:
                                pass
                            
                            # Atualizar progresso e enviar via SSE
                            combinacoes_processadas += 1
                            progresso = (combinacoes_processadas / total_combinacoes) * 100
                            
                            # Enviar atualização de progresso
                            progress_data = {
                                "progresso": progresso,
                                "combinacoes_processadas": combinacoes_processadas,
                                "total_combinacoes": total_combinacoes,
                                "completo": False
                            }
                            
                            self.wfile.write(f"data: {json.dumps(progress_data)}\n\n".encode('utf-8'))
                            self.wfile.flush()
            
            # Processar tábuas inválidas
            for tabua in tabuas_invalidas:
                tabuas_utilizadas.add(tabua)
                for idade in range(idade_min, idade_max + 1):
                    for sexo in sexos:
                        for periodo in range(periodo_min, periodo_max + 1):
                            try:
                                # Calcular seguro usando a nova função unificada
                                tabua_obj = TabuladeComutacao(taxa_juros, tabua)
                                tabua_obj.tabua_selecionada = tabua
                                
                                if tabua not in tabua_obj.tabuas_disponiveis:
                                    # Se a tábua não for encontrada, usar AT-83 como padrão
                                    if 'AT-83' in tabua_obj.tabuas_disponiveis:
                                        tabua = 'AT-83'
                                        tabua_obj.tabua_selecionada = tabua
                                    elif tabua_obj.tabuas_disponiveis:
                                        tabua = list(tabua_obj.tabuas_disponiveis.keys())[0]
                                        tabua_obj.tabua_selecionada = tabua
                                    else:
                                        continue
                                
                                # Usar a função unificada para calcular as taxas
                                taxas = calcular_taxas_seguro(tabua_obj, idade, sexo, periodo, taxa_juros, 100000)
                                
                                resultado = {
                                    "idade": idade,
                                    "sexo": sexo,
                                    "periodo": periodo,
                                    "tipo_tabua": "Inválido",
                                    "tabua": tabua,
                                    "taxa_vista": f"{taxas['taxa_vista']*100:.4f}%",
                                    "taxa_mensal": f"{taxas['taxa_mensal']*100:.4f}%"
                                }
                                resultados.append(resultado)
                                
                            except Exception as e:
                                pass
                            
                            # Atualizar progresso e enviar via SSE
                            combinacoes_processadas += 1
                            progresso = (combinacoes_processadas / total_combinacoes) * 100
                            
                            # Enviar atualização de progresso
                            progress_data = {
                                "progresso": progresso,
                                "combinacoes_processadas": combinacoes_processadas,
                                "total_combinacoes": total_combinacoes,
                                "completo": False
                            }
                            
                            self.wfile.write(f"data: {json.dumps(progress_data)}\n\n".encode('utf-8'))
                            self.wfile.flush()
            
            # Enviar resultado final
            final_data = {
                "success": True,
                "resultados": resultados,
                "total_combinacoes": total_combinacoes,
                "combinacoes_processadas": combinacoes_processadas,
                "progresso": 100.0,
                "idade_min": idade_min,
                "idade_max": idade_max,
                "periodo_min": periodo_min,
                "periodo_max": periodo_max,
                "tabuas_utilizadas": list(tabuas_utilizadas),
                "completo": True
            }
            
            self.wfile.write(f"data: {json.dumps(final_data)}\n\n".encode('utf-8'))
            self.wfile.flush()
            
        except Exception as e:
            error_data = {
                "success": False,
                "error": f"Erro no cálculo coletivo: {str(e)}",
                "completo": True
            }
            self.wfile.write(f"data: {json.dumps(error_data)}\n\n".encode('utf-8'))
            self.wfile.flush()
    
    def handle_download_excel(self):
        try:
            # Ler dados do POST
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                raise ValueError("Content-Length is 0")
            
            post_data = self.rfile.read(content_length)
            if not post_data:
                raise ValueError("No data received")
            
            data = json.loads(post_data.decode('utf-8'))
            resultados = data.get('resultados', [])
            
            if not resultados:
                raise ValueError("Nenhum resultado para exportar")
            
            # Criar arquivo Excel
            excel_data = self.create_excel_data(resultados)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            self.send_header('Content-Disposition', 'attachment; filename="resultados_analise_coletiva.xlsx"')
            self.send_header('Content-Length', str(len(excel_data)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(excel_data)
            
        except Exception as e:
            error_response = {
                "success": False,
                "error": f"Erro ao gerar arquivo: {str(e)}"
            }
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def create_excel_data(self, resultados):
        """Cria dados Excel a partir dos resultados"""
        try:
            # Criar workbook e worksheet
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Resultados Análise Coletiva"
            
            # Definir cabeçalhos
            headers = ['Idade', 'Sexo', 'Período', 'Tipo Tábua', 'Tábua', 'Taxa à Vista', 'Taxa Mensal']
            
            # Escrever cabeçalhos (sem formatação complexa por enquanto)
            for col, header in enumerate(headers, 1):
                ws.cell(row=1, column=col, value=header)
            
            # Escrever dados
            for row, resultado in enumerate(resultados, 2):
                sexo_texto = 'Masculino' if resultado['sexo'] == 'M' else 'Feminino'
                
                ws.cell(row=row, column=1, value=resultado['idade'])
                ws.cell(row=row, column=2, value=sexo_texto)
                ws.cell(row=row, column=3, value=resultado['periodo'])
                ws.cell(row=row, column=4, value=resultado['tipo_tabua'])
                ws.cell(row=row, column=5, value=resultado['tabua'])
                ws.cell(row=row, column=6, value=resultado['taxa_vista'])
                ws.cell(row=row, column=7, value=resultado['taxa_mensal'])
            
            # Ajustar largura das colunas
            column_widths = [8, 12, 10, 12, 15, 15, 15]
            for col, width in enumerate(column_widths, 1):
                ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = width
            
            # Salvar em BytesIO
            output = BytesIO()
            wb.save(output)
            output.seek(0)
            
            # Retornar os dados como bytes
            excel_bytes = output.getvalue()
            output.close()
            
            return excel_bytes
            
        except Exception as e:
            print(f"Erro ao criar Excel: {e}")
            # Fallback: criar um arquivo simples
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Resultados"
            
            # Cabeçalhos simples
            headers = ['Idade', 'Sexo', 'Período', 'Tipo Tábua', 'Tábua', 'Taxa à Vista', 'Taxa Mensal']
            for col, header in enumerate(headers, 1):
                ws.cell(row=1, column=col, value=header)
            
            # Dados simples
            for row, resultado in enumerate(resultados, 2):
                sexo_texto = 'Masculino' if resultado['sexo'] == 'M' else 'Feminino'
                ws.cell(row=row, column=1, value=resultado['idade'])
                ws.cell(row=row, column=2, value=sexo_texto)
                ws.cell(row=row, column=3, value=resultado['periodo'])
                ws.cell(row=row, column=4, value=resultado['tipo_tabua'])
                ws.cell(row=row, column=5, value=resultado['tabua'])
                ws.cell(row=row, column=6, value=resultado['taxa_vista'])
                ws.cell(row=row, column=7, value=resultado['taxa_mensal'])
            
            output = BytesIO()
            wb.save(output)
            output.seek(0)
            excel_bytes = output.getvalue()
            output.close()
            
            return excel_bytes
    
    def handle_cache_stats(self):
        """Retorna estatísticas do cache."""
        try:
            stats = obter_estatisticas_cache()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(stats, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            error_response = {"success": False, "error": str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def handle_limpar_cache(self):
        """Limpa o cache de tábuas."""
        try:
            limpar_cache_tabuas()
            
            response = {"success": True, "message": "Cache limpo com sucesso"}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            error_response = {"success": False, "error": str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        if self.path == '/calcular':
            try:
                # Ler dados do POST
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length == 0:
                    raise ValueError("Content-Length is 0")
                
                post_data = self.rfile.read(content_length)
                if not post_data:
                    raise ValueError("No data received")
                
                data = json.loads(post_data.decode('utf-8'))
                
                # Extrair parâmetros
                idade = int(data['idade'])
                sexo = data['sexo']
                periodo = int(data['periodo'])
                taxa_juros = float(data['taxa_juros']) / 100
                soma_segurada = float(data['soma_segurada'])
                tabua_selecionada = data['tabua_mortalidade']
                
                # Validação dos limites
                if not (0 <= idade <= 110):
                    raise ValueError("A idade deve estar entre 0 e 110 anos.")
                
                if not (1 <= periodo <= 10):
                    raise ValueError("O período deve estar entre 1 e 10 anos.")
                
                if not (0 <= taxa_juros <= 0.20):  # 0% a 20%
                    raise ValueError("A taxa de juros deve estar entre 0% e 20%.")
                
                if not (0 <= soma_segurada <= 200000):
                    raise ValueError("A soma segurada deve estar entre R$ 0,00 e R$ 200.000,00.")
                
                fracionamento = 12  # Mensal
                
                # Calcular
                tabua_obj = TabuladeComutacao(taxa_juros, tabua_selecionada)
                tabua_obj.tabua_selecionada = tabua_selecionada
                
                # Verificar se a tábua existe
                if tabua_selecionada not in tabua_obj.tabuas_disponiveis:
                    raise KeyError(f"Tábua '{tabua_selecionada}' não encontrada. Tábuas disponíveis: {list(tabua_obj.tabuas_disponiveis.keys())}")
                
                tabua_obj.dados = tabua_obj.tabuas_disponiveis[tabua_selecionada]
                tabua_obj.calcular_tabua_comutacao()
                
                seguro_anual = calcular_seguro_anual(tabua_obj, idade, sexo, periodo)
                seguro_fracionado_total, fator_ajuste, taxa_fracionada_calc = calcular_seguro_fracionado_total(taxa_juros, fracionamento, seguro_anual)
                valor_monetario_vista = soma_segurada * seguro_fracionado_total
                
                valor_mensal, N_x, N_x_n, anuidade_ajustada, percentual_mensal_calc = calcular_premio_mensal(tabua_obj, idade, periodo, valor_monetario_vista, taxa_juros, fracionamento, soma_segurada)
                
                # Preparar resposta
                response = {
                    "success": True,
                    "valor_total": f"R$ {valor_monetario_vista:,.2f}",
                    "percentual_total": f"{seguro_fracionado_total*100:.4f}%",
                    "valor_mensal": f"R$ {valor_mensal:,.2f}",
                    "percentual_mensal": f"{percentual_mensal_calc[0]*100:.4f}%",
                    "detalhes": {
                        "dados_entrada": {
                            "idade": idade,
                            "sexo": "Masculino" if sexo == 'M' else "Feminino",
                            "periodo": periodo,
                            "taxa_juros": f"{taxa_juros*100:.4f}%",
                            "fracionamento": "12 vezes por ano (mensal)",
                            "soma_segurada": f"R$ {soma_segurada:,.2f}"
                        },
                        "calculo_seguro_anual": {
                            "M_x": f"{tabua_obj.M_x[idade]:.2f}",
                            "M_x_n": f"{tabua_obj.M_x[idade + periodo]:.2f}",
                            "D_x": f"{tabua_obj.D_x[idade]:.2f}",
                            "formula": r"A_{x:n}^1 = \frac{M_x - M_{x+n}}{D_x}",
                            "valor": f"{seguro_anual:.8f}"
                        },
                        "calculo_seguro_fracionado": {
                            "taxa_fracionada_formula": r"\text{Taxa fracionada} = k \times ((1+i)^{1/k} - 1)",
                            "taxa_fracionada_valor": f"{taxa_fracionada_calc:.6f} ({taxa_fracionada_calc*100:.4f}%)",
                            "fator_ajuste_formula": r"\text{Fator de ajuste} = \frac{i}{k \times ((1+i)^{1/k} - 1)}",
                            "fator_ajuste_valor": f"{fator_ajuste:.6f}",
                            "formula": r"A_{x:n}^{(k)} = \left( \frac{i}{k \times ((1+i)^{1/k} - 1)} \right) \times A_{x:n}^1",
                            "valor": f"{seguro_fracionado_total:.8f}"
                        },
                        "calculo_premio_vista": {
                            "valor_unitario": f"{seguro_fracionado_total:.8f}",
                            "valor_monetario": f"R$ {valor_monetario_vista:,.2f}"
                        },
                        "calculo_premio_mensal": {
                            "N_x": f"{N_x:.2f}",
                            "N_x_n": f"{N_x_n:.2f}",
                            "D_x": f"{tabua_obj.D_x[idade]:.2f}",
                            "D_x_n": f"{tabua_obj.D_x[idade + periodo]:.2f}",
                            "anuidade_ajustada_formula": r"\text{Anuidade Ajustada} = \left( \frac{N_x - N_{x+n}}{D_x} + \frac{11}{24} \times \left(1 - \frac{D_{x+n}}{D_x}\right) \right) \times k",
                            "anuidade_ajustada_valor": f"{anuidade_ajustada:.6f}",
                            "valor_mensal_formula": r"\text{Valor Mensal} = \frac{\text{Valor Monetário (à vista)}}{\text{Anuidade Ajustada}}",
                            "valor_mensal_valor": f"R$ {valor_mensal:,.2f}",
                            "percentual_mensal_formula": r"\text{Percentual Mensal} = \frac{\text{Valor Mensal}}{\text{PGTO}(\text{taxa_fracionada}, \text{num_pagamentos}, -\text{Soma Segurada})}",
                            "percentual_mensal_valor": f"{percentual_mensal_calc[0]*100:.4f}%"
                        },
                        "tabua_comutacao": {
                            "l_x": {str(k): f"{v:.2f}" for k, v in tabua_obj.l_x.items()},
                            "d_x": {str(k): f"{v:.2f}" for k, v in tabua_obj.d_x.items()},
                            "D_x": {str(k): f"{v:.2f}" for k, v in tabua_obj.D_x.items()},
                            "C_x": {str(k): f"{v:.2f}" for k, v in tabua_obj.C_x.items()},
                            "N_x": {str(k): f"{v:.2f}" for k, v in tabua_obj.N_x.items()},
                            "M_x": {str(k): f"{v:.2f}" for k, v in tabua_obj.M_x.items()},
                            "v_x": {str(k): f"{v:.6f}" for k, v in tabua_obj.v_x.items()}
                        }
                    }
                }
                
                # Enviar resposta
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
            except Exception as e:
                error_response = {"success": False, "error": str(e)}
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
        elif self.path == '/calcular_coletivo':
            self.handle_calcular_coletivo()
        elif self.path == '/calcular_coletivo_progress':
            self.handle_calcular_coletivo_progress()
        elif self.path == '/download_excel':
            self.handle_download_excel()
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), CalculadoraHandler) as httpd:
        print(f"🚀 Servidor rodando em http://localhost:{PORT}")
        print("📊 Calculadora de Seguro de Vida - Web")
        print("🔗 Abra o navegador e acesse a URL acima")
        print("⏹️  Pressione Ctrl+C para parar o servidor")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor parado.")
