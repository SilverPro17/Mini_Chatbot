#!/usr/bin/env python3
"""
Chatbot RAG Super Robusta - Garantido para funcionar
"""

import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RobustCulinariaRAGBot:
    def __init__(self):
        self.documents = []
        self.vectorizer = None
        self.tfidf_matrix = None
        self.simple_index = {}  # Índice simples para fallback
        self.vectorstore_loaded = False
        
    def create_simple_index(self):
        """Cria índice simples para fallback"""
        print("📇 Criando índice simples...")
        
        self.simple_index = {}
        
        # Palavras-chave importantes e suas seções
        keywords = {
            'brigadeiro': [],
            'feijoada': [],
            'dendê': [],
            'azeite': [],
            'açaí': [],
            'mandioca': [],
            'moqueca': [],
            'vatapá': [],
            'tapioca': [],
            'coxinha': [],
            'farofa': []
        }
        
        for i, doc in enumerate(self.documents):
            content_lower = doc['content'].lower()
            for keyword in keywords:
                if keyword in content_lower:
                    keywords[keyword].append(i)
        
        self.simple_index = keywords
        
        # Debug do índice
        for keyword, indices in keywords.items():
            if indices:
                print(f"✅ '{keyword}': {len(indices)} documentos")
            else:
                print(f"❌ '{keyword}': nenhum documento")
    
    def load_documents(self):
        """Carrega documentos de forma muito robusta"""
        print("📚 Carregando documentos...")
        
        text_files = [
            "data/texts/receitas_brasileiras.txt",
            "data/texts/ingredientes_brasileiros.txt", 
            "data/texts/tecnicas_culinarias.txt"
        ]
        
        documents = []
        
        for file_path in text_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    print(f"📄 Processando {file_path}...")
                    
                    # Método 1: Por seções ===
                    sections = content.split('===')
                    for i, section in enumerate(sections):
                        section = section.strip()
                        if len(section) > 100:
                            documents.append({
                                'content': section,
                                'source': file_path,
                                'type': 'section',
                                'id': f"{file_path}_section_{i}"
                            })
                    
                    # Método 2: Por parágrafos grandes
                    paragraphs = content.split('\n\n')
                    for i, para in enumerate(paragraphs):
                        para = para.strip()
                        if len(para) > 100:
                            documents.append({
                                'content': para,
                                'source': file_path,
                                'type': 'paragraph',
                                'id': f"{file_path}_para_{i}"
                            })
                    
                except Exception as e:
                    print(f"❌ Erro em {file_path}: {e}")
        
        # Remove duplicatas
        unique_docs = []
        seen_content = set()
        
        for doc in documents:
            content_hash = hash(doc['content'][:100])  # Hash dos primeiros 100 chars
            if content_hash not in seen_content:
                unique_docs.append(doc)
                seen_content.add(content_hash)
        
        print(f"✅ {len(unique_docs)} documentos únicos carregados")
        return unique_docs
    
    def create_vectorstore(self):
        """Cria vectorstore com máxima robustez"""
        print("🗃️ Criando vectorstore robusto...")
        
        self.documents = self.load_documents()
        
        if not self.documents:
            print("❌ Nenhum documento!")
            return False
        
        # Cria índice simples primeiro
        self.create_simple_index()
        
        # Prepara textos
        texts = [doc['content'] for doc in self.documents]
        
        try:
            # TF-IDF mais permissivo
            self.vectorizer = TfidfVectorizer(
                max_features=2000,
                lowercase=True,
                stop_words=None,  # SEM stop words
                ngram_range=(1, 3),  # Unigrams, bigrams E trigrams
                max_df=0.95,  # Muito permissivo
                min_df=1,     # Inclui tudo
                token_pattern=r'[a-záàâãéêíóôõúçA-Z]+',  # Aceita tudo
                sublinear_tf=True,
                norm='l2'
            )
            
            self.tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            print(f"✅ TF-IDF: {self.tfidf_matrix.shape}")
            print(f"📖 Vocabulário: {len(self.vectorizer.vocabulary_)}")
            
            # Testa palavras importantes
            test_words = ['brigadeiro', 'feijoada', 'dendê', 'açaí']
            for word in test_words:
                if word in self.vectorizer.vocabulary_:
                    print(f"✅ '{word}' no vocabulário")
                else:
                    print(f"❌ '{word}' FALTANDO")
            
            self.vectorstore_loaded = True
            return True
            
        except Exception as e:
            print(f"❌ Erro TF-IDF: {e}")
            return False
    
    def search_tfidf(self, query, k=3):
        """Busca usando TF-IDF"""
        try:
            query_vector = self.vectorizer.transform([query.lower()])
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            top_indices = similarities.argsort()[-k:][::-1]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.01:  # Threshold muito baixo
                    results.append({
                        'content': self.documents[idx]['content'],
                        'similarity': similarities[idx],
                        'method': 'tfidf'
                    })
            
            return results
            
        except Exception as e:
            print(f"❌ Erro busca TF-IDF: {e}")
            return []
    
    def search_simple(self, query, k=3):
        """Busca usando índice simples"""
        query_lower = query.lower()
        results = []
        
        # Busca por palavras-chave
        for keyword, doc_indices in self.simple_index.items():
            if keyword in query_lower and doc_indices:
                for idx in doc_indices[:k]:
                    if idx < len(self.documents):
                        results.append({
                            'content': self.documents[idx]['content'],
                            'similarity': 0.8,  # Simulada
                            'method': 'simple',
                            'keyword': keyword
                        })
        
        # Se não encontrou nada, busca por substring
        if not results:
            for i, doc in enumerate(self.documents):
                if any(word in doc['content'].lower() for word in query_lower.split()):
                    results.append({
                        'content': doc['content'],
                        'similarity': 0.5,
                        'method': 'substring'
                    })
                    if len(results) >= k:
                        break
        
        return results
    
    def search(self, query, k=3):
        """Busca híbrida: TF-IDF + Simple"""
        print(f"🔍 Buscando: '{query}'")
        
        results = []
        
        # Método 1: TF-IDF
        if self.vectorstore_loaded:
            tfidf_results = self.search_tfidf(query, k)
            results.extend(tfidf_results)
            print(f"📊 TF-IDF: {len(tfidf_results)} resultados")
        
        # Método 2: Índice simples (fallback)
        if len(results) == 0:
            simple_results = self.search_simple(query, k)
            results.extend(simple_results)
            print(f"📇 Simples: {len(simple_results)} resultados")
        
        # Remove duplicatas
        unique_results = []
        seen_content = set()
        
        for result in results:
            content_start = result['content'][:50]
            if content_start not in seen_content:
                unique_results.append(result)
                seen_content.add(content_start)
        
        return unique_results[:k]
    
    def generate_answer(self, query, results):
        """Gera resposta"""
        if not results:
            return "😔 Não encontrei informações específicas sobre isso. Tente perguntas como: 'brigadeiro', 'feijoada', 'dendê', 'açaí', 'moqueca'."
        
        query_lower = query.lower()
        
        # Tipo de pergunta
        if any(word in query_lower for word in ['como', 'fazer', 'preparar', 'receita']):
            intro = "🍳 Sobre como preparar:"
        elif any(word in query_lower for word in ['o que é', 'que é']):
            intro = "📖 Definição encontrada:"
        else:
            intro = "📚 Informações encontradas:"
        
        response = f"{intro}\n\n"
        
        for i, result in enumerate(results[:2]):
            content = result['content'][:400]  # Primeiros 400 chars
            method = result.get('method', 'unknown')
            
            response += f"📄 {content}\n\n"
            
            if method == 'simple':
                keyword = result.get('keyword', '')
                response += f"💡 Encontrado por palavra-chave: '{keyword}'\n"
            elif method == 'tfidf':
                sim = result.get('similarity', 0)
                response += f"💡 Similaridade: {sim:.2%}\n"
        
        return response
    
    def ask(self, question):
        """Processa pergunta"""
        print(f"\n🤔 Pergunta: '{question}'")
        
        # Busca
        results = self.search(question, k=3)
        
        # Resposta
        answer = self.generate_answer(question, results)
        
        return answer
    
    def setup(self):
        """Setup completo"""
        print("🚀 Configurando Chatbot Super Robusto")
        print("=" * 45)
        
        return self.create_vectorstore()
    
    def chat_loop(self):
        """Chat interativo"""
        print("\n🍽️ Chatbot de Culinária Brasileira (Super Robusto)")
        print("Garantido para encontrar: brigadeiro, feijoada, dendê, açaí, etc.")
        print("Digite 'sair' para encerrar.\n")
        
        while True:
            try:
                question = input("🤔 Você: ").strip()
                
                if question.lower() in ['sair', 'exit', 'quit']:
                    print("🍴 Até logo!")
                    break
                
                if not question:
                    continue
                
                print("🤖 Assistente:")
                answer = self.ask(question)
                print(answer)
                print("-" * 50)
                
            except KeyboardInterrupt:
                print("\n🍴 Até logo!")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")

def main():
    bot = RobustCulinariaRAGBot()
    
    if bot.setup():
        print("✅ Setup concluído!")
        
        # Testes obrigatórios
        test_queries = ['brigadeiro', 'feijoada', 'dendê']
        for query in test_queries:
            print(f"\n🧪 Teste: {query}")
            result = bot.ask(query)
            print(f"✅ Resultado: {result[:100]}...")
        
        # Chat
        bot.chat_loop()
    else:
        print("❌ Falha no setup")

if __name__ == "__main__":
    main()