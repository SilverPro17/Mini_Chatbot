#!/usr/bin/env python3
"""
Interface web para o Chatbot RAG de Culinária Brasileira usando Streamlit
"""

import streamlit as st
import sys
import os

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from chatbot import CulinariaRAGBot

# Configuração da página
st.set_page_config(
    page_title="🍽️ Culinária Brasileira RAG",
    page_icon="🇧🇷",
    layout="wide"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E8B57;
        font-size: 3em;
        margin-bottom: 10px;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
    }
    .bot-message {
        background-color: #E8F5E8;
        border-left: 4px solid #4CAF50;
    }
    .sidebar-content {
        background-color: #F5F5F5;
        padding: 20px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_chatbot():
    """Inicializa o chatbot (cached para performance)"""
    bot = CulinariaRAGBot()
    if bot.setup():
        return bot
    else:
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🍽️ Culinária Brasileira RAG</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Seu assistente especializado em receitas e ingredientes brasileiros</p>', unsafe_allow_html=True)
    
    # Sidebar com informações
    with st.sidebar:
        st.markdown("### 📋 Sobre o Sistema")
        st.markdown("""
        Este chatbot usa **RAG (Retrieval-Augmented Generation)** para responder perguntas sobre:
        
        - 🥘 **Receitas tradicionais**
        - 🌿 **Ingredientes típicos**
        - 🍳 **Técnicas culinárias**
        - 🏛️ **História dos pratos**
        """)
        
        st.markdown("### 💡 Exemplos de Perguntas")
        examples = [
            "Como fazer feijoada?",
            "O que é dendê?",
            "Receita de brigadeiro",
            "Ingredientes do açaí",
            "Como preparar moqueca?",
            "O que é pequi?"
        ]
        
        for example in examples:
            if st.button(f"💬 {example}", key=f"example_{example}"):
                st.session_state.question_input = example
        
        st.markdown("---")
        st.markdown("### 🛠️ Tecnologias")
        st.markdown("""
        - **LangChain** para RAG
        - **FAISS** para busca vetorial
        - **HuggingFace** para embeddings
        - **Streamlit** para interface
        """)
    
    # Inicializa o chatbot
    if 'chatbot' not in st.session_state:
        with st.spinner('🚀 Inicializando chatbot...'):
            st.session_state.chatbot = init_chatbot()
    
    if st.session_state.chatbot is None:
        st.error("❌ Erro ao inicializar o chatbot. Verifique se o vector store foi criado.")
        st.info("💡 Execute: `python src/create_vectorstore.py`")
        return
    
    # Inicializa histórico de chat
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Input da pergunta
    col1, col2 = st.columns([4, 1])
    
    with col1:
        question = st.text_input(
            "🤔 Faça sua pergunta sobre culinária brasileira:",
            placeholder="Ex: Como fazer brigadeiro?",
            key="question_input"
        )
    
    with col2:
        ask_button = st.button("🔍 Perguntar", type="primary")
    
    # Processa a pergunta
    if ask_button and question:
        with st.spinner('🤖 Pensando...'):
            answer = st.session_state.chatbot.ask(question)
            
            # Adiciona ao histórico
            st.session_state.chat_history.append({
                "question": question,
                "answer": answer
            })
        
        # Limpa o input
        st.session_state.question_input = ""
    
    # Exibe histórico de chat
    if st.session_state.chat_history:
        st.markdown("## 💬 Conversa")
        
        # Exibe mensagens (mais recente primeiro)
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            # Pergunta do usuário
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>🤔 Você:</strong> {chat['question']}
            </div>
            """, unsafe_allow_html=True)
            
            # Resposta do bot
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>🤖 Assistente:</strong> {chat['answer']}
            </div>
            """, unsafe_allow_html=True)
            
            if i < len(st.session_state.chat_history) - 1:
                st.markdown("---")
        
        # Botão para limpar histórico
        if st.button("🗑️ Limpar Conversa"):
            st.session_state.chat_history = []
            st.rerun()
    
    else:
        # Mensagem inicial
        st.markdown("## 🚀 Como começar")
        st.info("👆 Digite uma pergunta sobre culinária brasileira acima ou clique em um dos exemplos na barra lateral!")
        
        # Estatísticas do sistema
        st.markdown("## 📊 Informações do Sistema")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📚 Base de Conhecimento", "Culinária Brasileira")
        
        with col2:
            st.metric("🔍 Modelo de Busca", "FAISS + HuggingFace")
        
        with col3:
            st.metric("🤖 Status", "✅ Online")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 50px;">
        🇧🇷 Desenvolvido com ❤️ para preservar a culinária brasileira
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()