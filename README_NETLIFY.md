# Calculadora de Seguro Prestamista - Netlify

Sistema especializado para cálculos atuariais de seguro prestamista com reavaliação anual.

## 🚀 Deploy no Netlify

### Arquivos Necessários

Para fazer o deploy no Netlify, você precisa dos seguintes arquivos:

1. **`index.html`** - Página principal (renomeie `index_netlify.html` para `index.html`)
2. **`calculadora_prestamista_netlify.html`** - Calculadora individual
3. **`calculadora_coletiva_netlify.html`** - Calculadora coletiva
4. **`tabuas_mortalidade.js`** - Dados das tábuas de mortalidade

### 📁 Estrutura de Arquivos

```
/
├── index.html                          # Página principal
├── calculadora_prestamista_netlify.html # Calculadora individual
├── calculadora_coletiva_netlify.html    # Calculadora coletiva
├── tabuas_mortalidade.js               # Dados das tábuas
└── README_NETLIFY.md                   # Este arquivo
```

### 🔧 Configuração do Netlify

1. **Acesse o Netlify**: https://netlify.com
2. **Faça login** na sua conta
3. **Clique em "New site from Git"**
4. **Conecte seu repositório** ou faça upload dos arquivos
5. **Configure as seguintes opções**:

#### Build Settings
- **Build command**: (deixe vazio)
- **Publish directory**: (deixe vazio ou coloque `/`)

#### Environment Variables
- Não são necessárias variáveis de ambiente

### 📋 Checklist de Deploy

- [ ] Renomear `index_netlify.html` para `index.html`
- [ ] Verificar se todos os arquivos estão presentes
- [ ] Testar localmente antes do deploy
- [ ] Fazer upload dos arquivos para o Netlify
- [ ] Verificar se o site está funcionando

### 🎯 Funcionalidades

#### Calculadora Individual
- ✅ Cálculo para uma pessoa específica
- ✅ Reavaliação anual automática
- ✅ 21 tábuas de mortalidade disponíveis
- ✅ Prêmio anual e mensal nivelado
- ✅ Taxa de risco anual e mensal
- ✅ Memória de cálculo detalhada

#### Calculadora Coletiva
- ✅ Análise para múltiplas combinações
- ✅ Intervalos de idade e parcelas
- ✅ Múltiplos sexos e tábuas
- ✅ Exportação para Excel
- ✅ Estatísticas resumidas
- ✅ Progresso em tempo real

### 🔍 Testes

Após o deploy, teste as seguintes funcionalidades:

1. **Página Principal**
   - [ ] Carregamento correto
   - [ ] Links funcionando
   - [ ] Design responsivo

2. **Calculadora Individual**
   - [ ] Carregamento das tábuas
   - [ ] Validação dos campos
   - [ ] Cálculo correto
   - [ ] Memória de cálculo

3. **Calculadora Coletiva**
   - [ ] Seleção múltipla
   - [ ] Cálculo em lote
   - [ ] Progresso visual
   - [ ] Download Excel

### 🐛 Solução de Problemas

#### Erro: "Tábuas não carregadas"
- Verifique se o arquivo `tabuas_mortalidade.js` está presente
- Verifique se o arquivo está sendo carregado corretamente

#### Erro: "Cálculo não funciona"
- Verifique o console do navegador para erros
- Verifique se todas as dependências estão carregando

#### Erro: "Download não funciona"
- Verifique se o navegador permite downloads
- Verifique se há dados para download

### 📞 Suporte

Se encontrar problemas:

1. Verifique o console do navegador (F12)
2. Verifique se todos os arquivos estão presentes
3. Teste em diferentes navegadores
4. Verifique a conexão com a internet

### 🎉 Pronto!

Após seguir estes passos, sua calculadora estará funcionando no Netlify!

**URL do site**: https://seu-site.netlify.app

**Funcionalidades disponíveis**:
- ✅ Cálculo individual
- ✅ Cálculo coletivo
- ✅ 21 tábuas de mortalidade
- ✅ Exportação Excel
- ✅ Interface responsiva
- ✅ Sem dependências de servidor

