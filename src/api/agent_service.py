import uuid

from langgraph.checkpoint.memory import InMemorySaver

from ai import agents, supervisors

_checkpointer = InMemorySaver()
_agent_cache = {}


def _get_cached_agent(agent_type: str):
    if agent_type not in _agent_cache:
        if agent_type == "document":
            _agent_cache[agent_type] = agents.get_document_agent(checkpointer=_checkpointer)
        elif agent_type == "movie":
            _agent_cache[agent_type] = agents.get_movie_discovery_agent(checkpointer=_checkpointer)
        elif agent_type == "supervisor":
            _agent_cache[agent_type] = supervisors.create_supervisor_agent(checkpointer=_checkpointer)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
    return _agent_cache[agent_type]


def invoke_agent(agent_type: str, message: str, user_id: int, thread_id: str | None = None) -> dict:
    agent = _get_cached_agent(agent_type)
    thread_id = thread_id or str(uuid.uuid4())
    config = {"configurable": {"user_id": str(user_id), "thread_id": thread_id}}
    response = agent.invoke(
        {"messages": [{"role": "user", "content": message}]},
        config,
    )
    reply = response["messages"][-1].content
    if not isinstance(reply, str):
        reply = str(reply)
    return {"reply": reply, "thread_id": thread_id}
