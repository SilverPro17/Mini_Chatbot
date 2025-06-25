#!/usr/bin/env python3
"""
Chatbot RAG com Debug para identificar problemas
"""

import os
import sys
import traceback

class DebugCulinariaRAGBot:
    def __init__(self):
        self.vectorstore_loaded = False
        self.documents = []
        self.vectorizer = None
        self.tfidf_matrix = None
        
    def debug_files(self):
        """Debug: verifica arquivos"""
        print("🔍 DEBUG: Verificando arquivos...")
        
        text_files = [
            "data/texts/receitas_brasileiras.txt",
            "data/texts/ingredientes_brasileiros.txt", 
            "data/texts/tecnicas_culinarias.txt"
        ]
        
        for file_path in text_files:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"✅ {file_path} - {size} bytes")
            else:
                print(f"❌ {file_path} - Não encontrado")
        
        return text_files
    
    def load_documents_debug(self):
        """Carrega documentos com debug"""
        print("📚 DEBUG: Carregando documentos...")
        
        text_files = self.debug_files()
        documents = []
        
        for file_path in text_files:
            if os.path.exists(file_path):
                try:
                    print(f"📄 Lendo: {file_path}")
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    print(f"   Tamanho: {len(content)} caracteres")
                    
                    # Divide em parágrafos simples
                    paragraphs = content.split('\n\n')
                    valid_paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 50]
                    
                    print(f"   Parágrafos válidos: {len(valid_paragraphs)}")
                    
                    for i, paragraph in enumerate(valid_paragraphs):
                        documents.append({
                            'content': paragraph,
                            'source': file_path,
                            'id': f"{file_path}_{i}"
                        })
                        
                except Exception as e:
                    print(f"❌ Erro ao ler {file_path}: {e}")
                    traceback.print_exc()
        
        print(f"📊 Total de documentos: {len(documents)}")
        if documents:
            print(f"📝 Exemplo: {documents[0]['content'][:100]}...")
        
        return documents
    
    def create_vectorstore_debug(self):
        """Cria vectorstore com debug"""
        print("🗃️ DEBUG: Criando vectorstore...")
        
        # Carrega documentos
        self.documents = self.load_documents_debug()
        
        if not self.documents:
            print("❌ Nenhum documento carregado!")
            return False
        
        # Prepara textos
        texts = [doc['content'] for doc in self.documents]
        print(f"📝 Textos para vetorização: {len(texts)}")
        
        try:
            # Importa sklearn
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            print("✅ Sklearn importado")
            
            # Cria vectorizer
            self.vectorizer = TfidfVectorizer(
                max_features=500,
                lowercase=True,
                stop_words='english',
                ngram_range=(1, 1),  # Simplificado
                max_df=0.9,
                min_df=1
            )
            print("✅ Vectorizer criado")
            
            # Treina
            self.tfidf_matrix = self.vectorizer.fit_transform(texts)
            print(f"✅ TF-IDF Matrix: {self.tfidf_matrix.shape}")
            
            self.vectorstore_loaded = True
            return True
            
        except Exception as e:
            print(f"❌ Erro na vetorização: {e}")
            traceback.print_exc()
            return False
    
    def search_debug(self, query, k=3):
        """Busca com debug"""
        print(f"🔍 DEBUG: Buscando por '{query}'")
        
        if not self.vectorstore_loaded:
            print("❌ Vectorstore não carregado")
            return []
        
        try:
            # Importa sklearn novamente para garantir
            from sklearn.metrics.pairwise import cosine_similarity
            
            # Transforma query
            print("🔧 Transformando query...")
            query_vector = self.vectorizer.transform([query])
            print(f"✅ Query vector shape: {query_vector.shape}")
            
            # Calcula similaridade
            print("🔧 Calculando similaridades...")
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            print(f"✅ Similaridades: {len(similarities)} valores")
            print(f"📊 Max similarity: {max(similarities):.4f}")
            
            # Pega top k
            top_indices = similarities.argsort()[-k:][::-1]
            print(f"🎯 Top indices: {top_indices}")
            
            results = []
            for idx in top_indices:
                sim_score = similarities[idx]
                print(f"   Índice {idx}: similaridade {sim_score:.4f}")
                
                if sim_score > 0.01:  # Threshold baixo para debug
                    results.append({
                        'content': self.documents[idx]['content'],
                        'similarity': sim_score,
                        'source': self.documents[idx]['source'],
                        'id': self.documents[idx]['id']
                    })
            
            print(f"✅ Resultados encontrados: {len(results)}")
            return results
            
        except Exception as e:
            print(f"❌ Erro na busca: {e}")
            traceback.print_exc()
            return []
    
    def ask_debug(self, question):
        """Pergunta com debug completo"""
        print(f"\n🤔 DEBUG: Processando '{question}'")
        
        try:
            # Busca
            results = self.search_debug(question, k=3)
            
            if not results:
                return "❌ Nenhum resultado encontrado."
            
            # Gera resposta
            print("🤖 Gerando resposta...")
            
            combined_text = ""
            for i, result in enumerate(results):
                print(f"   Resultado {i+1}: {result['content'][:50]}...")
                combined_text += f"{result['content']}\n\n"
            
            # Resposta simples
            response = f"📚 Encontrei estas informações:\n\n{combined_text[:500]}..."
            
            if len(combined_text) > 500:
                response += f"\n\n(Mostrando primeiros 500 caracteres de {len(combined_text)} total)"
            
            print("✅ Resposta gerada")
            return response
            
        except Exception as e:
            error_msg = f"❌ Erro detalhado: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return error_msg
    
    def setup_debug(self):
        """Setup com debug"""
        print("🚀 DEBUG: Configurando chatbot...")
        
        # Verifica diretório atual
        print(f"📁 Diretório atual: {os.getcwd()}")
        
        # Verifica se pasta data existe
        if os.path.exists("data"):
            print("✅ Pasta data encontrada")
        else:
            print("❌ Pasta data não encontrada")
            return False
        
        # Verifica pasta texts
        if os.path.exists("data/texts"):
            print("✅ Pasta data/texts encontrada")
            files = os.listdir("data/texts")
            print(f"📁 Arquivos em data/texts: {files}")
        else:
            print("❌ Pasta data/texts não encontrada")
            return False
        
        # Cria vectorstore
        return self.create_vectorstore_debug()
    
    def chat_loop_debug(self):
        """Loop de chat com debug"""
        print("\n🍽️ Chatbot DEBUG - Culinária Brasileira")
        print("Digite 'debug' para informações do sistema")
        print("Digite 'sair' para encerrar.\n")
        
        while True:
            try:
                question = input("🤔 Você: ").strip()
                
                if question.lower() in ['sair', 'exit', 'quit']:
                    print("👋 Tchau!")
                    break
                
                if question.lower() == 'debug':
                    print(f"📊 Vectorstore carregado: {self.vectorstore_loaded}")
                    print(f"📚 Documentos: {len(self.documents)}")
                    if hasattr(self, 'tfidf_matrix') and self.tfidf_matrix is not None:
                        print(f"🗃️ TF-IDF Matrix: {self.tfidf_matrix.shape}")
                    continue
                
                if not question:
                    continue
                
                answer = self.ask_debug(question)
                print(f"🤖 Resposta: {answer}")
                print("-" * 50)
                
            except KeyboardInterrupt:
                print("\n👋 Tchau!")
                break
            except Exception as e:
                print(f"❌ Erro no loop: {e}")
                traceback.print_exc()

def main():
    print("🔧 CHATBOT DEBUG - Identificando Problemas")
    print("=" * 50)
    
    bot = DebugCulinariaRAGBot()
    
    if bot.setup_debug():
        print("✅ Setup concluído com sucesso!")
        
        # Teste manual
        print("\n🧪 Teste manual:")
        test_result = bot.ask_debug("brigadeiro")
        print(f"Resultado do teste: {test_result[:100]}...")
        
        # Inicia chat
        bot.chat_loop_debug()
    else:
        print("❌ Falha no setup")

if __name__ == "__main__":
    main()