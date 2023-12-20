from langchain.chat_models import tongyi,ChatOpenAI

api_key="sk-77f54bfeb4eb4dda83e115e2687d8564"
LLM_MODEL = tongyi.ChatTongyi(dashscope_api_key=api_key,streaming=True)

# openai_key=""
# Tongyi_chat =ChatOpenAI(api_key=openai_key,streaming=True)
