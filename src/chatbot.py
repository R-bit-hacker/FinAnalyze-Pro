import streamlit as st
from groq import Groq
from utils import GROQ_API_KEY

def show_chatbot():
    st.title("FinBot Assistant")
    
    # --- ENTERPRISE AI GUARDRAILS (SYSTEM PROMPT) ---
    SYSTEM_PROMPT = """You are FinBot, a highly professional AI financial advisor exclusive to the FinAnalyze Pro app. 
    Your ONLY domain is finance, personal budgeting, investments, savings, financial health ratios, and explaining the FinAnalyze app.
    
    CRITICAL INSTRUCTION: You MUST NOT answer any questions that are unrelated to finance or the app. 
    If a user asks about an unrelated topic (e.g., cooking, fashion, general knowledge, coding, weather), you must politely decline. 
    Always try to cleverly pivot the conversation back to finance. 
    Example: If asked what color dress to wear, reply: "I'm a financial AI, so I can't help with fashion choices! However, I can help you build a savings plan so you can afford that designer dress. Would you like to discuss your budget?"
    """

    # Initialize chat history
    if "messages" not in st.session_state: 
        st.session_state.messages = []
    
    # Render chat history
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "assistant"
        bg = "#333" if role == "user" else "#1a1a40"
        st.markdown(f'<div style="background:{bg}; padding:10px; border-radius:10px; margin:5px;">{m["content"]}</div>', unsafe_allow_html=True)
        
    # Handle user input
    if prompt := st.chat_input("Ask FinBot..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()
        
    # Generate AI response
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("Analyzing financial data..."):
            try:
                client = Groq(api_key=GROQ_API_KEY)
                
                # Combine the strict system prompt with the chat history
                api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
                
                resp = client.chat.completions.create(
                    messages=api_messages, 
                    model="llama-3.3-70b-versatile"
                )
                
                reply = resp.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()
                
            except Exception as e: 
                st.error(f"Connection Error: {e}")