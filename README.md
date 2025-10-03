# Calculadora de Seguro Prestamista

Sistema web completo para cálculo de seguros de vida, com foco especial em seguro prestamista.

## 🚀 Características

- **Calculadora atuarial** para seguros de vida individuais, coletivos e prestamistas
- **Interface web moderna** com cálculos em tempo real
- **Múltiplas tábuas de mortalidade** para diferentes cenários
- **Cálculos precisos** usando fórmulas atuariais padrão
- **Exportação de resultados** para Excel
- **Reserva matemática** (provisão prospectiva)

## 📋 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/danilodeteixeira/seguro_prestamista.git
   cd seguro_prestamista
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

   Ou instale manualmente:
   ```bash
   pip install openpyxl numpy scipy
   ```

## 🚀 Como Executar

1. **Inicie o servidor:**
   ```bash
   python servidor_web.py
   ```

2. **Acesse no navegador:**
   - **Local:** http://localhost:8001
   - **Rede local:** http://[SEU_IP]:8001

## 📊 Tipos de Cálculo

### 1. Seguro Individual
- Cálculo tradicional de seguro de vida
- Baseado em idade, sexo, período e tábua de mortalidade

### 2. Seguro Prestamista
- **Seguro onde o valor segurado diminui** seguindo a amortização de um financiamento Price
- **Cobertura adequada**: se o segurado falecer, o beneficiário recebe exatamente o saldo devedor
- **Custo menor** que seguro tradicional
- **Sincronização perfeita** com a evolução da dívida

### 3. Cálculo Coletivo
- Análise em massa de múltiplas combinações
- Exportação para Excel
- Processamento paralelo otimizado

## 🏠 Seguro Prestamista - Conceito

O **seguro prestamista** é um tipo especial de seguro onde:
- O valor segurado **diminui ao longo do tempo**
- Segue exatamente a **amortização de um financiamento Price**
- Se o segurado falecer, o beneficiário recebe o **saldo devedor atual**
- É mais **econômico** que um seguro tradicional
- **Sincroniza perfeitamente** com a evolução da dívida

## 📈 Funcionalidades Avançadas

- **Reserva matemática**: Cálculo da provisão em qualquer momento
- **Evolução detalhada**: Tabela mês a mês do saldo devedor
- **Taxa de quitação de risco**: Custo efetivo do seguro
- **Múltiplas tábuas**: BR-EMS 2021, AT-83, etc.
- **Validação rigorosa**: Limites de idade, período, valores

## 🔧 Dependências

- **openpyxl**: Para exportação de Excel
- **numpy**: Para cálculos numéricos
- **scipy**: Para otimização e funções matemáticas avançadas

## 📱 Acesso Mobile

O sistema é totalmente responsivo e pode ser acessado de qualquer dispositivo na mesma rede WiFi.

## ⚠️ Importante

- Certifique-se de que o firewall permite conexões na porta 8001
- Ambos os dispositivos devem estar na mesma rede WiFi
- Se não funcionar, verifique as configurações do firewall

## 🛑 Parar o Servidor

Pressione `Ctrl+C` no terminal para parar o servidor.

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação do código ou entre em contato com o desenvolvedor.

