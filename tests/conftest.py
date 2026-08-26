import sys
import types

from langchain_google_vertexai import ChatVertexAI, VertexAI

vertexai_module = types.ModuleType(
    "langchain_community.chat_models.vertexai"
)

vertexai_module.ChatVertexAI = ChatVertexAI
vertexai_module.VertexAI = VertexAI

sys.modules["langchain_community.chat_models.vertexai"] = vertexai_module 