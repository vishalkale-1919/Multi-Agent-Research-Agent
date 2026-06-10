from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from agents.research_agent import run_research_agent
from agents.summary_agent import run_summary_agent
from agents.quiz_agent import run_quiz_agent

class AgentState(TypedDict):
    """
    Represents the state of our multi-agent workflow.
    """
    topic: str
    research_content: Optional[str]
    summary_content: Optional[str]
    quiz_content: Optional[str]
    error: Optional[str]

def create_coordinator_graph() -> StateGraph:
    """
    Creates and compiles the LangGraph workflow.
    """
    # Initialize the graph with the state schema
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("research", run_research_agent)
    workflow.add_node("summary", run_summary_agent)
    workflow.add_node("quiz", run_quiz_agent)
    
    # Set the entry point
    workflow.set_entry_point("research")
    
    # Add edges
    # Standard linear flow: research -> summary -> quiz -> END
    # If any agent fails, we could potentially route to END early, 
    # but the current node implementations handle errors gracefully by passing them forward.
    workflow.add_edge("research", "summary")
    workflow.add_edge("summary", "quiz")
    workflow.add_edge("quiz", END)
    
    # Compile the graph
    app = workflow.compile()
    return app

def run_workflow(topic: str) -> dict:
    """
    Executes the full LangGraph workflow for a given topic.
    """
    app = create_coordinator_graph()
    initial_state = {
        "topic": topic,
        "research_content": None,
        "summary_content": None,
        "quiz_content": None,
        "error": None
    }
    
    # Run the graph and get the final state
    final_state = app.invoke(initial_state)
    return final_state
