from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class Task(BaseModel):
    agent: str = Field(description="Must be exactly one of: 'research', 'scheduler', 'reminder'")
    instruction: str = Field(description="Clear, specific instruction for the agent.")
    payload: dict = Field(description="JSON dictionary of any specific data the agent needs (e.g., company name, time)")

class TaskPlan(BaseModel):
    tasks: List[Task] = Field(description="Ordered list of tasks to accomplish the goal")

llm = ChatOpenAI(model="gpt-5-mini", temperature=0)
structured_llm = llm.with_structured_output(TaskPlan)

def decompose_goal(goal: str, event_context: dict) -> List[dict]:
    prompt = f"""
    You are an autonomous Task Decomposer. Break the following goal down into actionable tasks.
    
    Goal: {goal}
    Event Context: {event_context}
    
    Available Agents:
    1. 'research' - Looks up information, company details, or interview prep on the web.
    2. 'scheduler' - Creates calendar events and blocks time.
    3. 'reminder' - Sends a notification or summary to the user.
    
    Return a logical sequence of tasks using only the available agents.
    """
    
    plan = structured_llm.invoke(prompt)
    return [task.dict() for task in plan.tasks]