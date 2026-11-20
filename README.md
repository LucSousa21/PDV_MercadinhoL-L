# PDV Mercadinho L&L

Sistema de Ponto de Venda (PDV) desenvolvido em Python para auxiliar no gerenciamento de vendas de uma mercearia de bairro, oferecendo uma interface desktop intuitiva e recursos para agilizar as operações de caixa.

O projeto busca facilitar o atendimento no estabelecimento, permitindo consultar produtos, registrar vendas, gerenciar pagamentos e integrar funcionalidades importantes para a rotina comercial.

## Funcionalidades

### Frente de Caixa
- Pesquisa de produtos por código de barras ou nome.
- Adição de produtos à venda.
- Gerenciamento dos itens da venda.
- Alteração de quantidades.
- Remoção de produtos.
- Cancelamento de vendas.
- Cálculo automático do valor total.

### Gerenciamento de Produtos
- Cadastro de produtos.
- Consulta de produtos para utilização no caixa.
- Identificação de produtos por código de barras.
- Alerta de estoque baixo.

### Processamento de Pagamentos
- Pagamento em dinheiro.
- Pagamento via PIX.
- Pagamento com cartão de débito.
- Pagamento com cartão de crédito.
- Pagamento com cartão alimentação.
- Divisão do pagamento entre diferentes formas.
- Cálculo automático de troco.

### Recursos Adicionais
- Atalhos de teclado para agilizar as operações.
- Integração com serviço de impressão.
- Verificação de novas versões do sistema.
- Download e preparação de atualizações.
- Empacotamento da aplicação para distribuição no Windows.

## Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Desenvolvimento da aplicação |
| CustomTkinter | Construção da interface gráfica |
| SQLAlchemy | Mapeamento objeto-relacional e acesso ao banco de dados |
| Pydantic | Estruturação e validação de dados |
| Requests | Comunicação HTTP |
| PyInstaller | Geração do executável |
| Git e GitHub | Versionamento e gerenciamento do código |

## Organização do Projeto

```text
PDV_MercadinhoL-L/
│
├── src/
│   ├── core/           # Serviços de infraestrutura
│   ├── schemas/        # Estruturas e validação de dados
│   ├── service/        # Regras e operações do sistema
│   └── views/          # Interface gráfica e componentes
│
├── assets/             # Recursos visuais
├── .github/
│   └── workflows/      # Automações do GitHub
│
├── main.py             # Ponto de entrada da aplicação
├── requirements.txt    # Dependências do projeto
├── PDV-Mercadinho.spec  # Configuração do PyInstaller
└── version.json        # Controle de versão
```

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/LucSousa21/PDV_MercadinhoL-L.git
```

### 2. Acessar a pasta do projeto

```bash
cd PDV_MercadinhoL-L
```

### 3. Criar um ambiente virtual

```bash
python -m venv .venv
```

### 4. Ativar o ambiente virtual

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Executar a aplicação

```bash
python main.py
```

## Gerar Executável

O projeto utiliza PyInstaller para empacotar a aplicação e permitir sua distribuição como executável no Windows.

Com as dependências instaladas, execute:

```bash
pyinstaller PDV-Mercadinho.spec
```

Os arquivos gerados pelo processo de compilação ficam no diretório `dist/`.

## Objetivo do Projeto

Desenvolver uma solução de software voltada para uma necessidade real de um pequeno comércio, aplicando conceitos de programação orientada a objetos, organização de código, persistência de dados, construção de interfaces gráficas e integração entre diferentes módulos de uma aplicação.

O projeto também proporciona experiência prática no desenvolvimento, manutenção e distribuição de aplicações desktop utilizando Python.

## Autor

Desenvolvido por [Lucas Carvalho](https://github.com/LucSousa21).
