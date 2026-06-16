from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from ai import agents
from ai import llms


def create_supervisor_agent(checkpointer=None):
    doc_agent = agents.get_document_agent()
    movie_agent = agents.get_movie_discovery_agent()

    @tool
    def doc_agent_tool(request: str, config: RunnableConfig) -> str:
        """处理文档相关任务：创建、查询、更新、删除文档。"""
        result = doc_agent.invoke({"messages": [("human", request)]}, config)
        return result["messages"][-1].content

    @tool
    def movie_agent_tool(request: str, config: RunnableConfig) -> str:
        """处理电影发现和查询相关任务。"""
        result = movie_agent.invoke({"messages": [("human", request)]}, config)
        return result["messages"][-1].content

    supervisor = create_react_agent(
        model=llms.get_openai_model(),
        tools=[
            doc_agent_tool,
            movie_agent_tool,
        ],
        prompt="你是一个 supervisor，根据用户问题分派给对应的子 agent",
        checkpointer=checkpointer,
    )
    return supervisor



