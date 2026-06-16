
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from tmdb import client as tmdb_client

@tool
def search_movie(query:str, limt:int=5, config:RunnableConfig ={}):
    """
    从电影数据库中搜索最近的LIMIT部电影，最多10部。

    argument:
    query:  str or 在文档标题或内容中进行查找搜索
    limt: int or 结果数量
    """
    configurable = config.get("configurable") or config.get("metadata")
    user_id = configurable.get("user_id")
    print(f"为id为的{user_id}用户,查找。")
    response = tmdb_client.search_movie(query, raw=True)
    if response.status_code not in range(200, 299):
        return []
    data = response.json()
    total_results = data.get("total_results", -1)
    if total_results == 0:
        return []
    if limt > 10:
        limt = 10
    results = data.get("results")[:limt]
    print(results)
    return results



@tool
def movie_detail(movie_id:int, config:RunnableConfig ={}):
    """
    通过search_movie中的id查找相关电影

    argument:
    movie_id: int or 出自电影的search_movie
    """
    configurable = config.get("configurable") or config.get("metadata")
    user_id = configurable.get("user_id")
    print(f"为id为的{user_id}用户,查找。")
    response = tmdb_client.movie_detail(movie_id, raw=True)
    if response.status_code not in range(200, 299):
        return {"error": "not found"}
    data = response.json()
    return data




movie_discovery_tools = [
    search_movie,
    movie_detail
]