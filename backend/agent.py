"""
LangChain Agent for natural language queries over cap table data
"""
from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from typing import Any, Dict, Optional
import json
from tools import CapTableTools
from config import settings

class EquityAgent:
    """LangChain-based agent for equity insights"""
    
    def __init__(self, cap_table_data: Dict[str, Any]):
        """Initialize agent with cap table data"""
        self.cap_table_tools = CapTableTools(cap_table_data)
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=settings.google_api_key,
            model=settings.google_model,
            temperature=0
        )
        self.agent_executor = self._setup_agent()
    
    def _setup_agent(self) -> AgentExecutor:
        """Setup LangChain agent with tools"""
        tools = [
            Tool(
                name="get_cap_table",
                func=lambda _: json.dumps(self.cap_table_tools.get_cap_table()),
                description="Get the full cap table with all shareholders and their ownership percentages"
            ),
            Tool(
                name="get_largest_shareholder",
                func=lambda _: json.dumps(self.cap_table_tools.get_largest_shareholder(), default=str),
                description="Find the shareholder with the largest stake in the company"
            ),
            Tool(
                name="calculate_ownership",
                func=lambda _: json.dumps([
                    obj.model_dump() if hasattr(obj, 'model_dump') else str(obj)
                    for obj in self.cap_table_tools.calculate_ownership()
                ]),
                description="Calculate and return ownership breakdown ranked by percentage"
            ),
            Tool(
                name="calculate_dilution",
                func=self._dilution_wrapper,
                description="Calculate dilution effect on shareholders. Input: number of new shares to issue"
            ),
            Tool(
                name="get_esop_summary",
                func=lambda _: json.dumps(self.cap_table_tools.get_esop_summary().model_dump()),
                description="Get Employee Stock Option Plan (ESOP) summary and allocation details"
            ),
            Tool(
                name="shareholder_summary",
                func=self._shareholder_wrapper,
                description="Get detailed information about a specific shareholder"
            ),
        ]
        
        # Create a local prompt template instead of pulling from hub
        prompt_template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
        
        prompt = PromptTemplate(
            input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
            template=prompt_template
        )
        
        agent = create_react_agent(self.llm, tools, prompt)
        executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            verbose=False,
            handle_parsing_errors=True
        )
        return executor
    
    def _dilution_wrapper(self, new_shares_str: str) -> str:
        """Wrapper for dilution calculation"""
        try:
            new_shares = int(float(new_shares_str))
            results = self.cap_table_tools.calculate_dilution(new_shares)
            return json.dumps([r.model_dump() for r in results])
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def _shareholder_wrapper(self, shareholder_name: str) -> str:
        """Wrapper for shareholder summary"""
        result = self.cap_table_tools.shareholder_summary(shareholder_name)
        return json.dumps(result)
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Process a natural language question using the agent
        """
        try:
            result = self.agent_executor.invoke({
                "input": question
            })
            return {
                "success": True,
                "answer": result.get("output", ""),
                "data": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "answer": f"I encountered an error processing your question: {str(e)}"
            }
    
    def get_available_tools(self) -> list:
        """Get list of available tools"""
        return [
            {
                "name": "get_cap_table",
                "description": "Get the full cap table with all shareholders and their ownership percentages"
            },
            {
                "name": "get_largest_shareholder",
                "description": "Find the shareholder with the largest stake"
            },
            {
                "name": "calculate_ownership",
                "description": "Get ownership breakdown ranked by percentage"
            },
            {
                "name": "calculate_dilution",
                "description": "Calculate dilution effect after new investment"
            },
            {
                "name": "get_esop_summary",
                "description": "Get ESOP allocation summary"
            },
            {
                "name": "shareholder_summary",
                "description": "Get details about a specific shareholder"
            },
        ]
