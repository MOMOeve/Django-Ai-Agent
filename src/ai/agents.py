from langgraph.prebuilt import create_react_agent
from ai.llms import get_openai_model
from ai.tools import (
    document_tools,
    movie_discovery_tools
)


def get_document_agent(checkpointer=None):
    model = get_openai_model()
    agent = create_react_agent(
        model=model,
        tools=document_tools,
        prompt = "你是一位文档管理助手。你可以查询已有文档、查看文档详情、以及创建新文档。当用户要创建文档时，你需要从对话中提取标题和内容来调用创建工具。",
        checkpointer=checkpointer,
    )
    return agent


def get_movie_discovery_agent(checkpointer=None):
    model = get_openai_model()
    agent = create_react_agent(
        model=model,
        tools=movie_discovery_tools,
        prompt = "你是一位乐于助人的电影代理人，协助寻找发现电影的相关信息，你需要从对话中提取标题和内容来调用创建工具。",
        checkpointer=checkpointer,
    )
    return agent