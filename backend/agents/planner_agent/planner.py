from dotenv import load_dotenv
from typing import TypedDict, Optional, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()

class PlannerState(TypedDict):
    event: dict
    memory_context: List[dict]
    action_required: bool
    goal: Optional[str]
    reasoning: str
    
class DecisionOutput(BaseModel):
    action_required: bool = Field(description="True if the AI should take action on the this event, otherwise False")
    reasoning: str = Field(description="Why action is or isn't required.")

class GoalOutput(BaseModel):
    goal: str = Field(description="A high-level executable goal for the AI.")

llm = ChatOpenAI(model="gpt-5-mini", temperature=0)

def evaluate_event(state: PlannerState):
    prompt = f"""
    You are an autonomous Chief of Staff. Analyze the following event and memory context.
    Determine if this event requires autonomous action (e.g., scheduling, researching, reminding).
    
    Event: {state['event']}
    Memory Context: {state['memory_context']}
    """
    
    structured_llm = llm.with_structured_output(DecisionOutput)
    result = structured_llm.invoke(prompt)

    return {"action_required": result.action_required, "reasoning": result.reasoning}

def generate_goal(state: PlannerState):
    prompt = f"""
    Event: {state['event']}
    Memory Context: {state['memory_context']}
    Reasoning: {state['reasoning']}
    
    Based on the context, define a single, clear, high-level goal to handle this event.
    """
    
    structured_llm = llm.with_structured_output(GoalOutput)
    result = structured_llm.invoke(prompt)

    return {"goal": result.goal}

def route_decision(state: PlannerState):
    if state["action_required"]:
        return "generate_goal"
    return END

workflow = StateGraph(PlannerState)
workflow.add_node("evaluate_event", evaluate_event)
workflow.add_node("generate_goal", generate_goal)

workflow.set_entry_point("evaluate_event")
workflow.add_conditional_edges("evaluate_event", route_decision)
workflow.add_edge("generate_goal", END)

planner_app = workflow.compile()