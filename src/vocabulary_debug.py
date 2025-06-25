#!/usr/bin/env python3
"""
Debug específico para entender por que 'brigadeiro' não funciona
"""

import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer

def load_text_content():
    """Carrega conteúdo dos arquivos"""
    print("📚 Carregando conteúdo dos arquivos...")
    
    files = [
        "data/texts/receitas_brasileiras.txt",
        "data/texts/ingredientes_brasileiros.txt",
        "data/texts/tecnicas_culinarias.txt"
    ]
    
    all_content = ""
    
    for file_path in files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                all_content += content + "\n"
                print(f"✅ {file_path}: {len(content)} caracteres")
    
    return all_content

def search_word_in_content(content, word):
    """Procura uma palavra específica no conteúdo"""
    print(f"\n🔍 Procurando '{word}' no conteúdo...")
    
    # Busca case-insensitive
    matches = re.finditer(word.lower(), content.lower())
    positions = list(matches)
    
    print(f"📊 Encontradas {len(positions)} ocorrências de '{word}'")
    
    for i, match in enumerate(positions[:3]):  # Mostra as primeiras 3
        start = max(0, match.start() - 50)
        end = min(len(content), match.end() + 50)
        context = content[start:end].replace('\n', ' ')
        print(f"{i+1}. ...{context}...")

def test_vectorizer_steps():
    """Testa cada passo do vectorizer"""
    print("\n🔧 Testando passos do vectorizer...")
    
    # Carrega conteúdo
    content = load_text_content()
    
    # Procura brigadeiro no texto original
    search_word_in_content(content, "brigadeiro")
    
    # Divide em seções
    sections = content.split('===')
    brigadeiro_sections = []
    
    print(f"\n📄 Total de seções: {len(sections)}")
    
    for i, section in enumerate(sections):
        if 'brigadeiro' in section.lower():
            brigadeiro_sections.append((i, section.strip()))
            print(f"✅ Seção {i} contém 'brigadeiro'")
    
    if not brigadeiro_sections:
        print("❌ Nenhuma seção contém 'brigadeiro'!")
        return
    
    # Testa preprocessamento
    print(f"\n🔧 Testando preprocessamento da primeira seção com brigadeiro...")
    section_content = brigadeiro_sections[0][1]
    print(f"📝 Seção original: {section_content[:200]}...")
    
    # Preprocessamento simples
    processed = section_content.lower()
    processed = re.sub(r'[^\w\sáàâãéêíóôõúç]', ' ', processed)
    processed = re.sub(r'\s+', ' ', processed)
    
    print(f"📝 Seção processada: {processed[:200]}...")
    
    # Verifica se brigadeiro ainda está lá
    if 'brigadeiro' in processed:
        print("✅ 'brigadeiro' ainda está presente após preprocessamento")
    else:
        print("❌ 'brigadeiro' foi removido no preprocessamento!")
    
    # Testa TF-IDF
    print(f"\n🗃️ Testando TF-IDF...")
    
    # Todas as seções processadas
    all_sections = []
    for section in sections:
        if len(section.strip()) > 50:
            processed = section.lower()
            processed = re.sub(r'[^\w\sáàâãéêíóôõúç]', ' ', processed)
            processed = re.sub(r'\s+', ' ', processed)
            all_sections.append(processed)
    
    print(f"📊 Seções para TF-IDF: {len(all_sections)}")
    
    # Cria vectorizer simples
    vectorizer = TfidfVectorizer(
        max_features=1000,
        lowercase=True,
        stop_words=None,  # SEM stop words para testar
        token_pattern=r'[a-záàâãéêíóôõúç]+',
        min_df=1
    )
    
    # Treina
    try:
        tfidf_matrix = vectorizer.fit_transform(all_sections)
        print(f"✅ TF-IDF criado: {tfidf_matrix.shape}")
        print(f"📖 Vocabulário: {len(vectorizer.vocabulary_)} palavras")
        
        # Verifica se brigadeiro está no vocabulário
        if 'brigadeiro' in vectorizer.vocabulary_:
            idx = vectorizer.vocabulary_['brigadeiro']
            print(f"✅ 'brigadeiro' encontrado no vocabulário (índice {idx})")
            
            # Testa query
            query_vector = vectorizer.transform(['brigadeiro'])
            print(f"✅ Query 'brigadeiro' transformada: {query_vector.shape}")
            
            # Calcula similaridades
            from sklearn.metrics.pairwise import cosine_similarity
            similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
            max_sim = max(similarities)
            print(f"📊 Similaridade máxima: {max_sim:.4f}")
            
            if max_sim > 0:
                best_idx = similarities.argmax()
                print(f"🎯 Melhor match na seção {best_idx}")
                print(f"📝 Conteúdo: {all_sections[best_idx][:100]}...")
            
        else:
            print("❌ 'brigadeiro' NÃO está no vocabulário!")
            
            # Mostra algumas palavras do vocabulário
            vocab_sample = list(vectorizer.vocabulary_.keys())[:20]
            print(f"📖 Amostra do vocabulário: {vocab_sample}")
            
            # Procura palavras similares
            similar_words = [word for word in vectorizer.vocabulary_.keys() if 'brig' in word or 'doce' in word]
            print(f"🔍 Palavras relacionadas: {similar_words}")
        
    except Exception as e:
        print(f"❌ Erro no TF-IDF: {e}")

def main():
    print("🕵️ DEBUG VOCABULÁRIO - Investigando problema do 'brigadeiro'")
    print("=" * 60)
    
    test_vectorizer_steps()

if __name__ == "__main__":
    main()