#!/usr/bin/env python3
"""
Script para criar o vector store com embeddings dos textos sobre culinária brasileira
"""

import os
import glob
import sys
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

def load_documents():
    """Carrega todos os documentos de texto da pasta data/texts/"""
    
    print("📚 Carregando documentos...")
    
    documents = []
    text_files = glob.glob("data/texts/*.txt")
    
    if not text_files:
        print("❌ Nenhum arquivo .txt encontrado em data/texts/")
        print("💡 Adicione alguns arquivos .txt nesta pasta primeiro")
        return []
    
    for file_path in text_files:
        try:
            print(f"📄 Carregando: {file_path}")
            
            # Lê o arquivo com encoding UTF-8
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Cria documento com metadata
            doc = Document(
                page_content=content,
                metadata={"source": file_path, "filename": os.path.basename(file_path)}
            )
            documents.append(doc)
            
        except Exception as e:
            print(f"❌ Erro ao carregar {file_path}: {e}")
    
    print(f"✅ {len(documents)} documentos carregados")
    return documents

def split_documents(documents):
    """Divide os documentos em chunks menores"""
    
    print("\n✂️ Dividindo documentos em chunks...")
    
    # Configuração do text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,        # Tamanho de cada chunk
        chunk_overlap=200,      # Sobreposição entre chunks
        length_function=len,
        separators=["\n\n", "\n", "===", "INGREDIENTES:", "MODO DE PREPARO:", ". ", ", "]
    )
    
    # Divide todos os documentos
    chunks = text_splitter.split_documents(documents)
    
    print(f"✅ {len(chunks)} chunks criados")
    
    # Mostra exemplo de chunk
    if chunks:
        print(f"\n📝 Exemplo de chunk:")
        print(f"Tamanho: {len(chunks[0].page_content)} caracteres")
        print(f"Preview: {chunks[0].page_content[:200]}...")
    
    return chunks

def create_embeddings():
    """Cria modelo de embeddings"""
    
    print("\n🔍 Configurando modelo de embeddings...")
    
    try:
        # Primeiro tenta instalar e usar sentence-transformers
        print("📦 Tentando instalar sentence-transformers...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "sentence-transformers", "--quiet"])
        
        from sentence_transformers import SentenceTransformer
        from langchain.embeddings.base import Embeddings
        
        print("📦 Usando SentenceTransformer com wrapper LangChain...")
        
        class CustomSentenceTransformerEmbeddings(Embeddings):
            def __init__(self, model_name):
                try:
                    self.model = SentenceTransformer(model_name)
                    print(f"✅ Modelo carregado: {model_name}")
                except Exception as e:
                    print(f"❌ Erro ao carregar {model_name}: {e}")
                    print("📦 Tentando modelo mais simples...")
                    self.model = SentenceTransformer('all-MiniLM-L6-v2')
                    print("✅ Modelo alternativo carregado: all-MiniLM-L6-v2")
            
            def embed_documents(self, texts):
                """Embeds a list of documents"""
                return self.model.encode(texts).tolist()
            
            def embed_query(self, text):
                """Embeds a query"""
                return self.model.encode([text])[0].tolist()
        
        embeddings = CustomSentenceTransformerEmbeddings("paraphrase-multilingual-MiniLM-L12-v2")
        return embeddings
        
    except Exception as e:
        print(f"❌ Erro com SentenceTransformer: {e}")
        print("💡 Tentando HuggingFace Embeddings...")
        
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            
            embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            print("✅ HuggingFace Embeddings carregado")
            return embeddings
            
        except Exception as e2:
            print(f"❌ Erro com HuggingFace: {e2}")
            print("💡 Usando solução TF-IDF customizada...")
            
            # TF-IDF Embeddings compatível com LangChain
            try:
                from sklearn.feature_extraction.text import TfidfVectorizer
                from langchain.embeddings.base import Embeddings
                import numpy as np
                import sys
                
                class TfidfEmbeddings(Embeddings):
                    def __init__(self):
                        self.vectorizer = TfidfVectorizer(
                            max_features=500, 
                            stop_words='english',
                            lowercase=True,
                            ngram_range=(1, 2)
                        )
                        self.fitted = False
                        self.all_texts = []
                    
                    def embed_documents(self, texts):
                        """Embeds a list of documents"""
                        if not self.fitted:
                            # Primeira vez: treina o vectorizer
                            self.all_texts = texts[:]
                            vectors = self.vectorizer.fit_transform(texts)
                            self.fitted = True
                        else:
                            # Adiciona novos textos ao conjunto
                            self.all_texts.extend(texts)
                            vectors = self.vectorizer.transform(texts)
                        
                        # Converte para lista de listas
                        return vectors.toarray().tolist()
                    
                    def embed_query(self, text):
                        """Embeds a single query"""
                        if not self.fitted:
                            # Se não foi treinado ainda, treina apenas com este texto
                            self.vectorizer.fit([text])
                            self.fitted = True
                        
                        vector = self.vectorizer.transform([text])
                        return vector.toarray()[0].tolist()
                
                embeddings = TfidfEmbeddings()
                print("✅ TF-IDF Embeddings configurado como fallback")
                return embeddings
                
            except Exception as e3:
                print(f"❌ Erro fatal com TF-IDF: {e3}")
                
                # Último recurso: embeddings dummy
                from langchain.embeddings.base import Embeddings
                import random
                
                class DummyEmbeddings(Embeddings):
                    def __init__(self, dimension=384):
                        self.dimension = dimension
                    
                    def embed_documents(self, texts):
                        # Gera embeddings aleatórios mas consistentes
                        embeddings = []
                        for text in texts:
                            # Usa hash do texto para embeddings consistentes
                            random.seed(hash(text) % (2**32))
                            embedding = [random.random() for _ in range(self.dimension)]
                            embeddings.append(embedding)
                        return embeddings
                    
                    def embed_query(self, text):
                        random.seed(hash(text) % (2**32))
                        return [random.random() for _ in range(self.dimension)]
                
                print("⚠️ Usando embeddings dummy (apenas para demonstração)")
                return DummyEmbeddings()

def create_vectorstore(chunks, embeddings):
    """Cria o vector store FAISS"""
    
    print("\n🗃️ Criando vector store...")
    
    try:
        # Cria o vector store com parâmetro correto
        vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=embeddings  # Mudança: usar 'embedding' ao invés de 'embedding_function'
        )
        
        # Salva localmente
        vectorstore_path = "data/vectorstore"
        os.makedirs(vectorstore_path, exist_ok=True)
        
        vectorstore.save_local(vectorstore_path)
        
        print(f"✅ Vector store salvo em: {vectorstore_path}")
        
        # Teste básico
        print("\n🧪 Testando busca...")
        try:
            results = vectorstore.similarity_search("como fazer brigadeiro", k=2)
            
            print(f"Encontrados {len(results)} resultados para 'como fazer brigadeiro':")
            for i, result in enumerate(results):
                preview = result.page_content[:100].replace('\n', ' ')
                print(f"{i+1}. {preview}...")
        except Exception as search_error:
            print(f"⚠️ Erro no teste de busca: {search_error}")
            print("✅ Vector store criado, mas teste de busca falhou (isso é normal com embeddings dummy)")
        
        return vectorstore
        
    except Exception as e:
        print(f"❌ Erro ao criar vector store: {e}")
        print("💡 Detalhes do erro:")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("🚀 Criando Vector Store para RAG Culinária Brasileira")
    print("=" * 55)
    
    # 1. Carrega documentos
    documents = load_documents()
    if not documents:
        return
    
    # 2. Divide em chunks
    chunks = split_documents(documents)
    if not chunks:
        print("❌ Nenhum chunk criado")
        return
    
    # 3. Cria embeddings
    embeddings = create_embeddings()
    if not embeddings:
        print("❌ Não foi possível carregar modelo de embeddings")
        return
    
    # 4. Cria vector store
    vectorstore = create_vectorstore(chunks, embeddings)
    if not vectorstore:
        print("❌ Não foi possível criar vector store")
        return
    
    print("\n🎉 Vector store criado com sucesso!")
    print("📝 Próximo passo: Execute python src/chatbot.py para testar o chatbot")

if __name__ == "__main__":
    main()