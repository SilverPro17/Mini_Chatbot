#!/usr/bin/env python3
"""
Interface Web para o Chatbot RAG de Culinária Brasileira
"""

import streamlit as st
import sys
import os

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(__file__))

# Importa o chatbot robusto
try:
    from robust_chatbot import RobustCulinariaRAGBot
    CHATBOT_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Erro ao importar chatbot: {e}")
    CHATBOT_AVAILABLE = False

# Configuração da página
st.set_page_config(
    page_title="🍽️ Culinária Brasileira RAG",
    page_icon="🇧🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #228B22, #32CD32);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5em;
        font-weight: 700;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.3em;
        margin-bottom: 40px;
        font-weight: 300;
        line-height: 1.6;
    }
    
    .feature-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.18);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    .chat-message {
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
        border-left: 5px solid #2196F3;
        color: #0D47A1;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
        border-left: 5px solid #4CAF50;
        color: #1B5E20;
    }
    
    .success-box {
        background: linear-gradient(135deg, #d4f6d4, #a8e6a8);
        border: none;
        border-radius: 12px;
        color: #1B5E20;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
        font-weight: 500;
    }
    
    .info-box {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        border: none;
        border-radius: 12px;
        color: #0D47A1;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.2);
        font-weight: 500;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3e0, #ffcc80);
        border: none;
        border-radius: 12px;
        color: #E65100;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.2);
        font-weight: 500;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        background: linear-gradient(135deg, #45a049, #4CAF50);
    }
    
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 12px 16px;
        font-size: 16px;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.25);
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 20px;
        margin: 15px 0;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5em;
        }
        
        .chat-message {
            padding: 15px;
        }
        
        .feature-card {
            padding: 15px;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_chatbot():
    """Inicializa o chatbot (cached para performance)"""
    if not CHATBOT_AVAILABLE:
        return None
        
    try:
        bot = RobustCulinariaRAGBot()
        if bot.setup():
            return bot
        else:
            return None
    except Exception as e:
        st.error(f"Erro ao inicializar chatbot: {e}")
        return None

def display_example_buttons():
    """Exibe botões de exemplo na sidebar"""
    st.markdown("### 💡 Perguntas de Exemplo")
    
    examples = [
        ("🍫", "Como fazer brigadeiro?", "como fazer brigadeiro"),
        ("🍲", "Receita de feijoada", "receita de feijoada"), 
        ("🌴", "O que é dendê?", "o que é dendê"),
        ("🥥", "Informações sobre açaí", "açaí"),
        ("🐟", "Como preparar moqueca?", "como preparar moqueca"),
        ("🥘", "Técnicas de farofa", "como fazer farofa"),
        ("🌿", "O que é pequi?", "o que é pequi"),
        ("🥖", "Receita de coxinha", "coxinha"),
        ("🌾", "Sobre mandioca", "mandioca"),
        ("🍳", "Técnicas culinárias", "técnicas de cozimento")
    ]
    
    for emoji, display_text, query in examples:
        if st.button(f"{emoji} {display_text}", key=f"btn_{query}", use_container_width=True):
            st.session_state.question_input = query
            st.rerun()

def display_system_info():
    """Exibe informações do sistema"""
    st.markdown("### 🛠️ Sistema RAG")
    
    with st.expander("ℹ️ Como funciona", expanded=False):
        st.markdown("""
        **🔄 RAG (Retrieval-Augmented Generation)**
        
        1. **🔍 Busca:** Encontra informações relevantes na base de dados
        2. **📖 Recupera:** Pega o conteúdo mais similar à pergunta
        3. **🤖 Gera:** Cria resposta contextualizada e inteligente
        
        **🔧 Tecnologias Utilizadas:**
        - 🗃️ TF-IDF
        - 🔍 Cosine Similarity
        - 📚 Scikit-learn
        - 🐍 Python
        """)
    
    with st.expander("📊 Estatísticas do Sistema", expanded=False):
        if 'chatbot' in st.session_state and st.session_state.chatbot:
            bot = st.session_state.chatbot
            
            col1, col2 = st.columns(2)
            
            with col1:
                docs_count = len(bot.documents) if bot.documents else 0
                st.metric("📚 Documentos", docs_count)
                
                vocab_count = len(bot.vectorizer.vocabulary_) if bot.vectorizer else 0
                st.metric("📖 Palavras no Vocabulário", vocab_count)
            
            with col2:
                keywords_count = len(bot.simple_index) if bot.simple_index else 0
                st.metric("🔍 Palavras-chave", keywords_count)
                
                st.metric("⚡ Método", "TF-IDF + Fallback")
        else:
            st.warning("⚠️ Chatbot não inicializado")

def main():
    # Header
    st.markdown('<h1 class="main-header">🍽️ Culinária Brasileira RAG</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Seu assistente inteligente para receitas e ingredientes brasileiros</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🇧🇷 Sobre o Projeto")
        st.markdown("""
        Sistema **RAG** especializado em culinária brasileira que combina:
        
        - 🥘 **Receitas tradicionais**
        - 🌿 **Ingredientes típicos** 
        - 🍳 **Técnicas culinárias**
        - 🏛️ **História dos pratos**
        """)
        
        display_example_buttons()
        
        st.markdown("---")
        display_system_info()
    
    # Verifica disponibilidade do chatbot
    if not CHATBOT_AVAILABLE:
        st.error("❌ Chatbot não disponível")
        st.info("💡 Execute: `python src/robust_chatbot.py` no terminal")
        return
    
    # Inicializa o chatbot
    if 'chatbot' not in st.session_state:
        with st.spinner('🚀 Inicializando sistema RAG...'):
            st.session_state.chatbot = init_chatbot()
    
    if st.session_state.chatbot is None:
        st.error("❌ Erro ao inicializar o chatbot")
        st.info("💡 Verifique se os arquivos estão em data/texts/")
        
        if st.button("🔄 Tentar Novamente"):
            st.session_state.chatbot = init_chatbot()
            st.rerun()
        return
    
    # Status de sucesso
    st.markdown("""
    <div class="success-box">
        ✅ <strong>Sistema RAG ativo!</strong> O chatbot está pronto para responder suas perguntas sobre culinária brasileira.
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializa histórico de chat
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Input da pergunta
    st.markdown("## 💬 Faça sua Pergunta")
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        question = st.text_input(
            "🤔 Digite sua pergunta:",
            placeholder="Ex: Como fazer brigadeiro?",
            key="question_input",
            label_visibility="collapsed"
        )
    
    with col2:
        ask_button = st.button("🔍 Perguntar", type="primary", use_container_width=True)
    
    # Processa a pergunta
    if (ask_button and question) or (question and question != st.session_state.get('last_question', '')):
        if question.strip():
            with st.spinner('🤖 Processando sua pergunta...'):
                try:
                    answer = st.session_state.chatbot.ask(question)
                    
                    # Adiciona ao histórico
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": answer
                    })
                    
                    # Atualiza última pergunta
                    st.session_state.last_question = question
                    
                except Exception as e:
                    st.error(f"❌ Erro ao processar pergunta: {str(e)}")
    
    # Exibe histórico de chat
    if st.session_state.chat_history:
        st.markdown("## 📝 Histórico da Conversa")
        
        # Controles do chat
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🗑️ Limpar", type="secondary"):
                st.session_state.chat_history = []
                st.session_state.last_question = ""
                st.rerun()
        
        with col2:
            st.metric("💬 Mensagens", len(st.session_state.chat_history))
        
        with col3:
            if st.button("📄 Exportar Conversa"):
                chat_text = ""
                for i, chat in enumerate(st.session_state.chat_history):
                    chat_text += f"Pergunta {i+1}: {chat['question']}\n"
                    chat_text += f"Resposta {i+1}: {chat['answer']}\n\n"
                
                st.download_button(
                    label="💾 Baixar Conversa",
                    data=chat_text,
                    file_name="conversa_culinaria_brasileira.txt",
                    mime="text/plain"
                )
        
        # Exibe mensagens (mais recente primeiro)
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            # Pergunta do usuário
            st.markdown(f"""
            <div class="chat-message user-message">
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <div style="background: #2196F3; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; margin-right: 10px; font-weight: bold;">
                        🤔
                    </div>
                    <strong style="color: #0D47A1;">Você perguntou:</strong>
                </div>
                <div style="margin-left: 40px; font-size: 1.1em;">
                    {chat['question']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Resposta do bot
            formatted_answer = chat['answer'].replace('\n', '<br>')
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <div style="background: #4CAF50; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; margin-right: 10px; font-weight: bold;">
                        🤖
                    </div>
                    <strong style="color: #1B5E20;">Assistente respondeu:</strong>
                </div>
                <div style="margin-left: 40px; line-height: 1.6;">
                    {formatted_answer}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if i < len(st.session_state.chat_history) - 1:
                st.markdown("---")
    
    else:
        # Mensagem inicial
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #4CAF50; text-align: center; margin-bottom: 20px;">
                🚀 Como Começar
            </h3>
            
            <div class="info-box">
                <div style="text-align: center; margin-bottom: 15px;">
                    <div style="font-size: 3em;">👆</div>
                </div>
                <strong>Dicas para usar o sistema:</strong><br><br>
                • <strong>Digite uma pergunta</strong> sobre culinária brasileira acima<br>
                • <strong>Clique nos exemplos</strong> da barra lateral<br>
                • <strong>Pergunte sobre receitas</strong>, ingredientes ou técnicas<br>
                • <strong>O sistema busca</strong> na base de conhecimento e responde automaticamente
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Grid de exemplos na tela principal
        st.markdown("### 🎯 Categorias de Perguntas")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="glass-card">
                <div style="text-align: center; margin-bottom: 15px;">
                    <div style="font-size: 3em;">🍽️</div>
                </div>
                <h4 style="color: #4CAF50; text-align: center;">Receitas</h4>
                <p>• Como fazer brigadeiro?</p>
                <p>• Receita de feijoada</p>
                <p>• Preparo de moqueca</p>
                <p>• Técnica da coxinha</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="glass-card">
                <div style="text-align: center; margin-bottom: 15px;">
                    <div style="font-size: 3em;">🌿</div>
                </div>
                <h4 style="color: #FF8C00; text-align: center;">Ingredientes</h4>
                <p>• O que é dendê?</p>
                <p>• Sobre o açaí</p>
                <p>• Benefícios da mandioca</p>
                <p>• Uso do pequi</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="glass-card">
                <div style="text-align: center; margin-bottom: 15px;">
                    <div style="font-size: 3em;">🍳</div>
                </div>
                <h4 style="color: #9370DB; text-align: center;">Técnicas</h4>
                <p>• Como fazer farofa?</p>
                <p>• Técnicas de refogado</p>
                <p>• Cozimento no vapor</p>
                <p>• Marinada brasileira</p>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #f8f9fa, #ffffff); border-radius: 15px; margin-top: 40px;">
        <div style="font-size: 2em; margin-bottom: 15px;">🇧🇷</div>
        <h3 style="color: #4CAF50; margin-bottom: 10px;">RAG Culinária Brasileira</h3>
        <p style="color: #666; margin-bottom: 15px; line-height: 1.6;">
            Sistema desenvolvido para preservar e compartilhar nossa rica tradição culinária<br>
            Tecnologia de ponta aplicada à valorização da cultura brasileira
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()