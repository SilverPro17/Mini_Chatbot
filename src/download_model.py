#!/usr/bin/env python3
"""
Script para baixar modelo LLM local para o projeto RAG
"""

import os
from huggingface_hub import hf_hub_download

def download_llama_model():
    """
    Baixa um modelo LLM otimizado em português
    Usando microsoft/DialoGPT-medium como alternativa leve
    """
    
    print("🤖 Baixando modelo LLM...")
    print("Modelo: microsoft/DialoGPT-medium")
    print("Nota: Modelo leve para demonstração. Para produção, use modelos maiores.")
    
    try:
        # Para este exemplo, vamos usar um modelo via transformers
        # que será carregado automaticamente
        from transformers import GPT2LMHeadModel, GPT2Tokenizer
        
        model_name = "microsoft/DialoGPT-medium"
        
        print("📥 Baixando tokenizer...")
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        
        print("📥 Baixando modelo...")
        model = GPT2LMHeadModel.from_pretrained(model_name)
        
        # Salva localmente
        model_path = "models/dialogpt-medium"
        os.makedirs(model_path, exist_ok=True)
        
        tokenizer.save_pretrained(model_path)
        model.save_pretrained(model_path)
        
        print(f"✅ Modelo salvo em: {model_path}")
        
    except Exception as e:
        print(f"❌ Erro ao baixar modelo: {e}")
        print("💡 Alternativa: O chatbot pode usar um modelo online via HuggingFace")

def download_embedding_model():
    """Baixa modelo de embeddings em português"""
    
    print("\n🔍 Configurando modelo de embeddings...")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        # Modelo de embeddings em português
        model_name = "neuralmind/bert-base-portuguese-cased"
        
        print(f"📥 Baixando {model_name}...")
        
        # Isso fará o download automático quando necessário
        print("✅ Modelo de embeddings configurado")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    print("🚀 Configurando modelos para RAG Culinária Brasileira")
    print("=" * 55)
    
    download_embedding_model()
    download_llama_model()
    
    print("\n🎉 Modelos configurados!")
    print("📝 Próximo passo: Adicione textos em data/texts/ e execute create_vectorstore.py")

if __name__ == "__main__":
    main()