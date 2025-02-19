from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, filter_messages
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
import re
from typing import List, Dict, Any,Callable, Tuple

from aibanker.config_files.config import OPTION_DICT
from aibanker.config_files.config_ai import system_prompt_chat, open_ai_model


class LLMChat:
    
    def __init__(self, 
                 currency: str, tools):
        
        self.llm = ChatOpenAI(model=open_ai_model)
        self.llm_with_tools = self.llm.bind_tools(tools, parallel_tool_calls=False)
        
        self.sys_msg = SystemMessage(content=system_prompt_chat.format(currency=currency, category_list = str(OPTION_DICT.keys())))
        
        self.memory = MemorySaver()
        self.builder = StateGraph(MessagesState)

        self.builder.add_node("assistant", self._process_assistant_message)
        self.builder.add_node("tools", ToolNode(tools))
        
        self.builder.add_edge(START, "assistant")
        self.builder.add_conditional_edges("assistant", tools_condition)
        self.builder.add_edge("tools", "assistant")
        
        self.react_graph_memory = self.builder.compile(checkpointer=self.memory)
        
        self.config = {"configurable": {"thread_id": "1"}}
    
    def _process_assistant_message(self, state: MessagesState) -> Dict[str, Any]:
        messages = [self.sys_msg] + state["messages"]
        response = self.llm_with_tools.invoke(messages)
        return {"messages": [response]}

    
    
    def add_message(self, content: str) -> str:
        new_message = HumanMessage(content=content)
        input_payload = {"messages": [new_message]}
        updated_state = self.react_graph_memory.invoke(input_payload, self.config)
        messages = updated_state.get("messages", [])
        # print(messages)
        
        # Filter to only include AIMessage objects using LangChain's utility
        ai_messages = list(filter_messages(messages, include_types=[AIMessage]))
        
        # Check if there are any AI messages; if so, take only the last one
        if ai_messages:
            answer = ai_messages[-1].content
            clean_text = lambda s: re.sub(r'[#*_~`>\-\[\]\(\)\\\n]', '', s)
            answer =clean_text(answer)
        else:

            answer = ""
        return answer



        
        