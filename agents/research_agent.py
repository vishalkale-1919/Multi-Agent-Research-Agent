from utils.llm import get_llm
from utils.prompts import RESEARCH_AGENT_PROMPT
from langchain_core.prompts import PromptTemplate

def run_research_agent(state: dict) -> dict:
    """
    Executes the research agent to generate comprehensive content on the topic.
    """
    topic = state.get("topic", "")
    
    try:
        llm = get_llm()
        prompt = PromptTemplate.from_template(RESEARCH_AGENT_PROMPT)
        chain = prompt | llm
        
        response = chain.invoke({"topic": topic})
        
        return {"research_content": response.content}
    except Exception as e:
        return {"error": f"Research Agent failed: {str(e)}"}
