import streamlit as st
import os
from dotenv import load_dotenv
from workflow.graph import run_workflow

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        font-weight: 700;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .status-indicator {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        font-weight: bold;
    }
    .status-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def check_api_key():
    """Check if the Groq API key is configured."""
    api_key = os.getenv("GROQ_API_KEY")
    # if api_key:
    #     print("API Key Loaded Successfully")
    # else:
    #     print("API Key Missing")
    return api_key and api_key != "your_key_here"

def main():
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/bot.png", width=80)
        st.title("🤖 Navigation & Settings")
        
        # API Status Indicator
        st.subheader("API Status")
        if check_api_key():
            st.markdown('<div class="status-indicator status-success">✅ Groq API Key Configured</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-error">❌ Groq API Key Missing</div>', unsafe_allow_html=True)
            st.warning("Please add your GROQ_API_KEY to the .env file.")
            
        st.markdown("---")
        
        # Example Topics
        st.subheader("💡 Example Topics")
        example_topics = [
            "Quantum Computing",
            "Artificial General Intelligence",
            "CRISPR Gene Editing",
            "Nuclear Fusion Energy",
            "Blockchain Technology"
        ]
        
        for topic in example_topics:
            if st.button(topic):
                st.session_state.topic_input = topic
                
        st.markdown("---")
        st.markdown("**Powered by:**")
        st.markdown("- LangGraph")
        st.markdown("- Streamlit")
        st.markdown("- Groq API (Llama 3.3 70B)")

    # Main content area
    st.markdown('<p class="main-header">Multi-Agent Research Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Generate comprehensive research, summaries, and quizzes on any topic using specialized AI agents.</p>', unsafe_allow_html=True)

    # Initialize session state for input
    if 'topic_input' not in st.session_state:
        st.session_state.topic_input = ""

    # Input section
    topic = st.text_input("Enter a topic for research:", value=st.session_state.topic_input, placeholder="e.g., The Impact of Artificial Intelligence on Healthcare")
    
    # Generate button
    generate_clicked = st.button("🚀 Generate Research", type="primary")

    if generate_clicked:
        if not topic.strip():
            st.error("⚠️ Please enter a topic to begin research.")
        elif not check_api_key():
            st.error("⚠️ Groq API key is missing. Please check your .env file.")
        else:
            with st.spinner(f"Agents are collaborating to research '{topic}'..."):
                # Run the LangGraph workflow
                result = run_workflow(topic)
                
                if result.get("error"):
                    st.error(f"❌ An error occurred during the workflow: {result['error']}")
                else:
                    st.success("✅ Research generation complete!")
                    
                    # Store results in session state to persist across tab switches
                    st.session_state.research_content = result.get("research_content", "No content generated.")
                    st.session_state.summary_content = result.get("summary_content", "No content generated.")
                    st.session_state.quiz_content = result.get("quiz_content", "No content generated.")

    # Display sections in tabs if results exist
    if 'research_content' in st.session_state:
        tab1, tab2, tab3 = st.tabs(["📚 Research Output", "📝 Summary Output", "❓ Quiz Output"])
        
        with tab1:
            st.markdown(st.session_state.research_content)
            st.download_button(
                label="📥 Download Research as TXT",
                data=st.session_state.research_content,
                file_name=f"research_{topic.replace(' ', '_')}.txt",
                mime="text/plain"
            )
            
        with tab2:
            st.markdown(st.session_state.summary_content)
            st.download_button(
                label="📥 Download Summary as TXT",
                data=st.session_state.summary_content,
                file_name=f"summary_{topic.replace(' ', '_')}.txt",
                mime="text/plain"
            )
            
        with tab3:
            st.markdown(st.session_state.quiz_content)
            st.download_button(
                label="📥 Download Quiz as TXT",
                data=st.session_state.quiz_content,
                file_name=f"quiz_{topic.replace(' ', '_')}.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
