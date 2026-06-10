from utils.llm import get_llm
from utils.prompts import QUIZ_AGENT_PROMPT
from langchain_core.prompts import PromptTemplate

def run_quiz_agent(state: dict) -> dict:
    """
    Executes the quiz agent to generate questions based on the summary content.
    """
    summary_content = state.get("summary_content", "")
    
    # Check if there's an error from previous steps
    if state.get("error"):
        return {"error": state.get("error")}
        
    if not summary_content:
        return {"error": "Quiz Agent failed: No summary content provided."}
    
    try:
        llm = get_llm()
        prompt = PromptTemplate.from_template(QUIZ_AGENT_PROMPT)
        chain = prompt | llm
        
        response = chain.invoke({"summary_content": summary_content})
        
        return {"quiz_content": response.content}
    except Exception as e:
        return {"error": f"Quiz Agent failed: {str(e)}"}
