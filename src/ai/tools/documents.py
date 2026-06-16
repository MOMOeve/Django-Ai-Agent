from django.db.models import Q
from documents.models import Document
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig


def _get_user_id(config: RunnableConfig):
    configurable = config.get("configurable") or config.get("metadata") or {}
    user_id = configurable.get("user_id")
    if user_id is None:
        return None
    return int(user_id)


@tool
def list_documents(config: RunnableConfig):
    """
    获取当前用户最近的文档（最多5条）
    :return:
    """
    user_id = _get_user_id(config)
    if user_id is None:
        return {"error": "无效请求：未识别当前用户"}
    queryset = Document.objects.filter(owner_id=user_id, active=True).order_by("-created_at")
    response_data = []
    for obj in queryset[:5]:
        response_data.append({
            "id": obj.id,
            "title": obj.title,
        })
    return response_data


@tool
def get_document(document_id: int, config: RunnableConfig):
    """
    获取特定文档详细信息
    :param document_id:
    :return:
    """
    user_id = _get_user_id(config)
    if user_id is None:
        return {"error": "无效请求：未识别当前用户"}
    try:
        queryset = Document.objects.get(owner_id=user_id, id=document_id, active=True)
    except Document.DoesNotExist:
        return {"error": "没有找到这个文档，该文档不存在或不属于您，请先列出文档确认 ID"}
    response_data = {
        "id": queryset.id,
        "title": queryset.title,
        "content": queryset.content,
        "created_at": queryset.created_at,
    }
    return response_data



@tool
def create_document(title: str, content: str, config: RunnableConfig):
    """
    帮我写一篇文章。

    Arguments are:
    title: 标题长度在50字以内与内容相关
    content: 内容长度300字以上500字以内
    """
    user_id = _get_user_id(config)
    if user_id is None:
        return {"error": "无效请求：未识别当前用户"}
    queryset = Document.objects.create(owner_id=user_id, content=content, title=title, active=True)
    response_data = {
        "id": queryset.id,
        "title": queryset.title,
        "content": queryset.content,
        "created_at": queryset.created_at,
    }
    return response_data


@tool
def delete_document(document_id: int, config: RunnableConfig):
    """
    删除文章
    :param document_id:
    :return:
    """
    user_id = _get_user_id(config)
    if user_id is None:
        return {"error": "无效请求：未识别当前用户"}
    try:
        queryset = Document.objects.get(owner_id=user_id, id=document_id, active=True)
    except Document.DoesNotExist:
        return {"error": "没有找到这个文档，该文档不存在或不属于您"}
    queryset.delete()
    response_data = {
        "messages": "删除成功"
    }
    return response_data


@tool
def update_document(document_id: int, title: str = None, content: str = None, config: RunnableConfig = None):
    """
    通过document_id, title, content等相关参数来更新文章

    Arguments are:
    document_id: 要更新的文章id (required)
    title: 新标题 (optional)
    content: 新内容 (optional) )
    """
    user_id = _get_user_id(config)
    if user_id is None:
        return {"error": "无效请求：未识别当前用户"}
    try:
        queryset = Document.objects.get(owner_id=user_id, id=document_id, active=True)
    except Document.DoesNotExist:
        return {"error": "没有找到这个文档，该文档不存在或不属于您"}
    if title is not None:
        queryset.title = title
    if content is not None:
        queryset.content = content
    if title or content:
        queryset.save()
    response_data = {
        "id": queryset.id,
        "title": queryset.title,
        "content": queryset.content,
        "updated_at": queryset.updated_at,
        "messages": "更新成功"
    }
    return response_data


@tool
def search_documents(query: str, config: RunnableConfig):
    """
    查找与query相关的内容或标题的文章

    arguments:
    query: string 或 查找标题或内容
    """
    user_id = _get_user_id(config)
    if user_id is None:
        return {"error": "无效请求：未识别当前用户"}

    default_lookups = {
        "owner_id": user_id,
        "active": True,
    }

    queryset = Document.objects.filter(**default_lookups).filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )
    response_data = []
    for obj in queryset[:5]:
        response_data.append({
            "id": obj.id,
            "title": obj.title,
            "content": obj.content,
            "updated_at": obj.updated_at,
            "messages": "查找成功"
        })
    return response_data




document_tools = [
    update_document,
    delete_document,
    list_documents,
    get_document,
    create_document,
]