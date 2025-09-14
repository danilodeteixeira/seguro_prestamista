# 🏥 Calculadora de Seguro de Vida - Web

Sistema web para cálculo de seguros de vida com análise individual e coletiva, desenvolvido em Python com otimizações de performance.

## 🚀 Funcionalidades

### 📊 Cálculo Individual
- Interface web intuitiva
- Cálculo de prêmios à vista e mensais
- Suporte a múltiplas tábuas de mortalidade
- Resultados detalhados com fórmulas atuariais

### 📈 Cálculo Coletivo (Otimizado)
- **Análise em lote** de múltiplas combinações
- **Cache inteligente** para tábuas de comutação
- **Processamento paralelo** com multiprocessing
- **Exportação em Excel** (.xlsx)
- **Logs de performance** em tempo real

### ⚡ Otimizações de Performance
- **Cache LRU** (Least Recently Used) com 1000 entradas
- **Processamento paralelo** usando todos os cores da CPU
- **Cache global** de tábuas de comutação
- **Velocidade 3-5x maior** para cálculos repetitivos

## 🛠️ Tecnologias

- **Backend**: Python 3.10+ com http.server
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Cálculos**: Matemática atuarial com tábuas de mortalidade
- **Otimização**: multiprocessing, functools.lru_cache
- **Exportação**: openpyxl para arquivos Excel

## 📦 Instalação

1. **Clone o repositório**:
```bash
git clone https://github.com/seu-usuario/seguro-prestamista.git
cd seguro-prestamista
```

2. **Instale as dependências**:
```bash
pip install openpyxl
```

3. **Execute o servidor**:
```bash
python servidor_web.py
```

4. **Acesse no navegador**:
```
http://localhost:8000
```

## 🎯 Como Usar

### Cálculo Individual
1. Acesse a página inicial
2. Clique em "Cálculo Individual"
3. Preencha os dados (idade, sexo, período, taxa de juros, soma segurada)
4. Selecione a tábua de mortalidade
5. Clique em "Calcular"

### Cálculo Coletivo
1. Acesse a página inicial
2. Clique em "Cálculo Coletivo"
3. Configure os intervalos:
   - **Idades**: 0 a 110 anos
   - **Períodos**: 1 a 10 anos
   - **Sexos**: Masculino, Feminino ou ambos
   - **Tábuas**: Válidas e/ou inválidas
   - **Taxa de juros**: 0% a 20%
4. Clique em "Calcular"
5. Aguarde o processamento (logs no terminal)
6. Baixe os resultados em Excel

## 📊 Tábuas de Mortalidade

O sistema suporta múltiplas tábuas de mortalidade carregadas do arquivo `tabuas_mortalidade_completas.csv`:
- **Tábuas Válidas**: AT-83, BR-EMS 2021, etc.
- **Tábuas Inválidas**: IBGE 2023, etc.

## ⚡ Performance

### Benchmarks de Otimização
- **Antes**: ~2-5 segundos para 100 combinações
- **Depois**: ~0.5-1 segundo para 100 combinações
- **Melhoria**: 3-5x mais rápido

### Recursos de Monitoramento
- **Endpoint `/cache_stats`**: Estatísticas do cache
- **Endpoint `/limpar_cache`**: Limpar cache quando necessário
- **Logs detalhados** de performance no terminal

## 🔧 API Endpoints

- `GET /` - Página inicial
- `GET /calculadora_individual.html` - Interface individual
- `GET /calculadora_coletiva.html` - Interface coletiva
- `GET /tabuas` - Lista tábuas disponíveis
- `POST /calcular` - Cálculo individual
- `POST /calcular_coletivo` - Cálculo coletivo otimizado
- `POST /download_excel` - Download resultados em Excel
- `GET /cache_stats` - Estatísticas do cache
- `GET /limpar_cache` - Limpar cache

## 📈 Exemplo de Uso

### Cálculo Coletivo Otimizado
```bash
📊 Iniciando cálculo coletivo otimizado:
   • Idades: 20-25 (6 idades)
   • Períodos: 1-3 (3 períodos)
   • Sexos: ['M', 'F'] (2 sexos)
   • Tábuas: 2 válidas + 1 inválidas
   • Total: 54 combinações

🚀 Processando 54 combinações com 4 workers paralelos...
Progresso: 100.0% (54/54)
✅ Processamento concluído em 0.8 segundos
⚡ Velocidade: 67.5 combinações/segundo
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

Desenvolvido com ❤️ para cálculos atuariais eficientes e precisos.
