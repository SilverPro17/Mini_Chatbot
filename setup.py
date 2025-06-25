#!/usr/bin/env python3
"""
Setup script para instalar dependências do projeto RAG Culinária Brasileira
"""

import subprocess
import sys
import os

def install_package(package):
    """Instala um pacote usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado com sucesso")
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar {package}")

def main():
    print("🚀 Configurando ambiente para RAG Culinária Brasileira")
    print("=" * 50)
    
    # Lista de dependências
    packages = [
        "langchain",
        "langchain-community",
        "langchain-huggingface",
        "sentence-transformers",
        "faiss-cpu",
        "transformers",
        "torch",
        "pypdf2",
        "python-dotenv",
        "streamlit",
        "huggingface_hub"
    ]
    
    print("📦 Instalando dependências...")
    for package in packages:
        install_package(package)
    
    print("\n🎯 Criando estrutura de diretórios...")
    directories = [
        "data/texts",
        "data/vectorstore",
        "models",
        "src"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Criado: {directory}")
    
    print("\n✅ Setup concluído!")
    print("📋 Próximos passos:")
    print("1. Execute: python src/download_model.py")
    print("2. Adicione arquivos de texto em data/texts/")
    print("3. Execute: python src/create_vectorstore.py")
    print("4. Execute: python src/chatbot.py")

if __name__ == "__main__":
    main()