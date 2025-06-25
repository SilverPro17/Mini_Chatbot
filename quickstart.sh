#!/bin/bash

# 🚀 Script de Início Rápido - RAG Culinária Brasileira
# Execute: chmod +x quickstart.sh && ./quickstart.sh

echo "🍽️ Configurando RAG Culinária Brasileira"
echo "========================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir com cor
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verifica Python
echo "🐍 Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_status "Python $PYTHON_VERSION encontrado"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    print_status "Python $PYTHON_VERSION encontrado"
    PYTHON_CMD="python"
else
    print_error "Python não encontrado! Instale Python 3.8+ primeiro."
    exit 1
fi

# Verifica pip
echo "📦 Verificando pip..."
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    print_error "pip não encontrado!"
    exit 1
fi

print_status "pip encontrado"

# Cria ambiente virtual (opcional)
echo "🔧 Configurando ambiente..."
read -p "Deseja criar um ambiente virtual? (recomendado) [y/N]: " create_venv

if [[ $create_venv =~ ^[Yy]$ ]]; then
    if [[ ! -d "venv" ]]; then
        print_info "Criando ambiente virtual..."
        $PYTHON_CMD -m venv venv
        print_status "Ambiente virtual criado"
    fi
    
    print_info "Ativando ambiente virtual..."
    source venv/bin/activate
    print_status "Ambiente virtual ativado"
fi

# Instala dependências
echo "📥 Instalando dependências..."
$PIP_CMD install -r requirements.txt

if [ $? -eq 0 ]; then
    print_status "Dependências instaladas"
else
    print_error "Falha ao instalar dependências"
    exit 1
fi

# Executa setup
echo "🛠️ Executando setup..."
$PYTHON_CMD setup.py

# Verifica se existem arquivos de texto
echo "📄 Verificando base de conhecimento..."
txt_files=$(find data/texts/ -name "*.txt" 2>/dev/null | wc -l)

if [ $txt_files -gt 0 ]; then
    print_status "$txt_files arquivos de texto encontrados"
else
    print_warning "Nenhum arquivo .txt encontrado em data/texts/"
    print_info "Os arquivos de exemplo já foram criados no setup"
fi

# Baixa modelos
echo "🤖 Configurando modelos..."
$PYTHON_CMD src/download_model.py

if [ $? -eq 0 ]; then
    print_status "Modelos configurados"
else
    print_warning "Alguns modelos podem não ter sido baixados (isso é normal)"
fi

# Cria vector store
echo "🗃️ Criando vector store..."
$PYTHON_CMD src/create_vectorstore.py

if [ $? -eq 0 ]; then
    print_status "Vector store criado com sucesso"
else
    print_error "Falha ao criar vector store"
    exit 1
fi

echo ""
echo "🎉 Configuração concluída!"
echo "========================"

# Menu de opções
echo ""
echo "🚀 Como usar:"
echo "1. Chatbot no terminal:"
echo "   $PYTHON_CMD src/chatbot.py"
echo ""
echo "2. Interface web (recomendado):"
echo "   streamlit run src/app_streamlit.py"
echo ""

# Pergunta qual executar
read -p "Qual interface deseja usar agora? [1=Terminal, 2=Web, N=Nenhuma]: " interface_choice

case $interface_choice in
    1)
        print_info "Iniciando chatbot no terminal..."
        $PYTHON_CMD src/chatbot.py
        ;;
    2)
        print_info "Iniciando interface web..."
        print_info "Acesse: http://localhost:8501"
        streamlit run src/app_streamlit.py
        ;;
    *)
        print_info "Setup concluído! Execute os comandos acima quando quiser usar o chatbot."
        ;;
esac

echo ""
print_status "Obrigado por usar o RAG Culinária Brasileira! 🇧🇷"