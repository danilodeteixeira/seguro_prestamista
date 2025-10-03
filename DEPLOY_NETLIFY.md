# 🚀 Deploy no Netlify - Instruções Completas

## 📋 Pré-requisitos

- Conta no Netlify (gratuita)
- Arquivos preparados (já estão prontos!)

## 📁 Arquivos Necessários

### ✅ Arquivos que você precisa enviar para o Netlify:

1. **`index.html`** (renomeie `index_netlify.html` para `index.html`)
2. **`calculadora_prestamista_netlify.html`**
3. **`calculadora_coletiva_netlify.html`**
4. **`tabuas_mortalidade.js`**
5. **`netlify.toml`** (opcional, mas recomendado)

### ❌ Arquivos que NÃO precisa enviar:

- `servidor_web.py` (não funciona no Netlify)
- `tabuas_mortalidade_completas.csv` (dados já estão em JS)
- `calculadora_prestamista_postalis.html` (versão com servidor)
- `calculadora_coletiva_postalis.html` (versão com servidor)
- Qualquer arquivo `.py`

## 🔧 Passo a Passo

### 1. Preparar Arquivos

```bash
# Renomear arquivo principal
mv index_netlify.html index.html

# Verificar se todos os arquivos estão presentes
ls -la
```

### 2. Acessar Netlify

1. Vá para https://netlify.com
2. Clique em **"Sign up"** ou **"Log in"**
3. Faça login com GitHub, GitLab ou email

### 3. Criar Novo Site

#### Opção A: Upload Manual (Mais Fácil)
1. Clique em **"Add new site"**
2. Selecione **"Deploy manually"**
3. Arraste os arquivos para a área de upload:
   - `index.html`
   - `calculadora_prestamista_netlify.html`
   - `calculadora_coletiva_netlify.html`
   - `tabuas_mortalidade.js`
   - `netlify.toml` (opcional)

#### Opção B: Conectar Repositório Git
1. Clique em **"Add new site"**
2. Selecione **"Import an existing project"**
3. Conecte seu repositório GitHub/GitLab
4. Configure:
   - **Build command**: (deixe vazio)
   - **Publish directory**: (deixe vazio)

### 4. Configurar Site

#### Build Settings
- **Build command**: (deixe vazio)
- **Publish directory**: (deixe vazio)
- **Functions directory**: (deixe vazio)

#### Environment Variables
- Não são necessárias

### 5. Deploy

1. Clique em **"Deploy site"**
2. Aguarde o deploy (1-2 minutos)
3. Seu site estará disponível em: `https://nome-aleatorio.netlify.app`

### 6. Configurar Domínio (Opcional)

1. Vá para **"Site settings"**
2. Clique em **"Domain management"**
3. Adicione seu domínio personalizado

## 🧪 Testar o Site

### Testes Básicos

1. **Página Principal**
   - [ ] Carrega corretamente
   - [ ] Links funcionam
   - [ ] Design responsivo

2. **Calculadora Individual**
   - [ ] Carrega tábuas
   - [ ] Valida campos
   - [ ] Calcula corretamente
   - [ ] Mostra memória de cálculo

3. **Calculadora Coletiva**
   - [ ] Seleção múltipla funciona
   - [ ] Cálculo em lote funciona
   - [ ] Progresso visual
   - [ ] Download Excel

### Testes Avançados

1. **Performance**
   - [ ] Carregamento rápido
   - [ ] Sem erros no console
   - [ ] Funciona em mobile

2. **Funcionalidades**
   - [ ] Todas as tábuas carregam
   - [ ] Cálculos corretos
   - [ ] Exportação funciona

## 🐛 Solução de Problemas

### Erro: "Site não carrega"
- Verifique se todos os arquivos foram enviados
- Verifique se `index.html` está na raiz
- Verifique o console do navegador

### Erro: "Tábuas não carregam"
- Verifique se `tabuas_mortalidade.js` está presente
- Verifique se o arquivo está sendo carregado
- Verifique o console do navegador

### Erro: "Cálculo não funciona"
- Verifique se todas as dependências carregam
- Verifique o console do navegador
- Teste em diferentes navegadores

### Erro: "Download não funciona"
- Verifique se há dados para download
- Verifique se o navegador permite downloads
- Teste em diferentes navegadores

## 📊 Monitoramento

### Netlify Dashboard
- Acesse seu dashboard no Netlify
- Monitore deploys e performance
- Configure notificações

### Analytics
- Ative analytics no Netlify
- Monitore uso e performance
- Configure alertas

## 🎉 Pronto!

Após seguir estes passos, sua calculadora estará funcionando no Netlify!

### ✅ Checklist Final

- [ ] Arquivos enviados corretamente
- [ ] Site carrega sem erros
- [ ] Calculadora individual funciona
- [ ] Calculadora coletiva funciona
- [ ] Download Excel funciona
- [ ] Design responsivo
- [ ] Performance adequada

### 🔗 Links Úteis

- **Netlify**: https://netlify.com
- **Documentação**: https://docs.netlify.com
- **Suporte**: https://netlify.com/support

### 📞 Suporte

Se encontrar problemas:

1. Verifique este guia
2. Consulte a documentação do Netlify
3. Verifique o console do navegador
4. Teste em diferentes navegadores

**Boa sorte com seu deploy! 🚀**

