from langchain.chat_models import tongyi,ChatOpenAI

api_key=""
LLM_MODEL = tongyi.ChatTongyi(dashscope_api_key=api_key,streaming=True)

# openai_key=""
# Tongyi_chat =ChatOpenAI(api_key=openai_key,streaming=True)
