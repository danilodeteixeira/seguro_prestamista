# 📦 Arquivos para Deploy no Netlify

## ✅ Arquivos Obrigatórios (4 arquivos principais)

### 1. **`index.html`** 
- Página principal da aplicação
- **Renomeie:** `index_netlify.html` → `index.html`

### 2. **`calculadora_prestamista_netlify.html`**
- Calculadora individual (seguro prestamista por pessoa)
- ✅ Inclui paginação (1000 resultados por página)
- ✅ Botão de download movido para cima
- ✅ Todas as 21 tábuas de mortalidade integradas

### 3. **`calculadora_coletiva_netlify.html`**
- Calculadora coletiva (análise em massa)
- ✅ Inclui paginação (1000 resultados por página)
- ✅ Botão de download movido para cima
- ✅ Todas as 21 tábuas de mortalidade integradas

### 4. **`tabuas_mortalidade.js`**
- Dados de todas as 21 tábuas de mortalidade
- ✅ Funciona 100% offline
- ✅ Sem dependências de servidor

## 🔧 Arquivos de Configuração (Opcionais)

### 5. **`netlify.toml`** (Opcional)
- Configurações de cache e headers
- Melhora performance do site

### 6. **`login.html`** (Opcional)
- Página de login (se quiser manter autenticação)
- Credenciais: `conde` / `c@nde13`

## 📋 Arquivos de Documentação (Não enviar)

- `README_NETLIFY.md` - Instruções gerais
- `DEPLOY_NETLIFY.md` - Guia de deploy
- `NETLIFY_READY.md` - Status de preparação
- `ARQUIVOS_NETLIFY.md` - Este arquivo

## 🚀 Instruções de Deploy

### Passo 1: Preparar Arquivos
```bash
# Renomear arquivo principal
mv index_netlify.html index.html
```

### Passo 2: Upload no Netlify
1. Acesse https://netlify.com
2. Clique em "Add new site"
3. Selecione "Deploy manually"
4. Arraste os 4-6 arquivos principais
5. Clique em "Deploy site"

### Passo 3: Testar
- ✅ Página principal carrega
- ✅ Calculadora individual funciona
- ✅ Calculadora coletiva funciona
- ✅ Download Excel funciona
- ✅ Paginação funciona (1000 por página)

## 🎯 Funcionalidades Incluídas

### ✅ Calculadora Individual
- Cálculo atuarial preciso
- 21 tábuas de mortalidade
- Prêmio anual e mensal
- Taxa de risco anual e mensal
- Memória de cálculo detalhada
- Reavaliação anual automática

### ✅ Calculadora Coletiva
- Análise em massa
- Intervalos de idade e parcelas
- Múltiplos sexos e tábuas
- Exportação Excel completa
- Paginação (1000 resultados por página)
- Estatísticas resumidas

### ✅ Características Técnicas
- 100% client-side (sem servidor)
- Performance otimizada
- Interface responsiva
- Compatível com todos os navegadores
- Dados das tábuas integrados

## 🎉 Status: PRONTO PARA DEPLOY!

Todos os arquivos estão preparados e testados. A aplicação está 100% funcional e pronta para o Netlify! 🚀

