from utils.llm import get_llm
from utils.prompts import SUMMARY_AGENT_PROMPT
from langchain_core.prompts import PromptTemplate

def run_summary_agent(state: dict) -> dict:
    """
    Executes the summary agent to generate a concise summary of the research content.
    """
    research_content = state.get("research_content", "")
    
    # Check if there's an error from the previous step
    if state.get("error"):
        return {"error": state.get("error")}
        
    if not research_content:
        return {"error": "Summary Agent failed: No research content provided."}
    
    try:
        llm = get_llm()
        prompt = PromptTemplate.from_template(SUMMARY_AGENT_PROMPT)
        chain = prompt | llm
        
        response = chain.invoke({"research_content": research_content})
        
        return {"summary_content": response.content}
    except Exception as e:
        return {"error": f"Summary Agent failed: {str(e)}"}
