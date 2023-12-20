from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import StreamingResponse

import time
from kb import LLMKnowledgeBaseManager
from chat import Conversation
from utils import Tongyi_chat

app = FastAPI()

class LLMRequest(BaseModel):
    knowledgebase: str
    message: str

class LLMResponse(BaseModel):
    response: str

@app.post("/llm", response_model=LLMResponse)
async def llm_endpoint(request: LLMRequest):
    # 解析请求
    kb = request.knowledgebase
    message = request.message

    # 确保必要的参数都存在
    if kb is None or message is None:
        raise HTTPException(status_code=400, detail="Missing 'knowledgebase' or 'message' parameter")

    # 创建对话系统实例并获取回应
    conversation = Conversation(Tongyi_chat,kb) # 这里假设 Conversation 类在初始化时接收 knowledgebase 参数
    response = conversation.start(message, conversation.chat_history_list)
    # content=""
    # for res in response:
    #     # print(res,end=" ",flush=True)
    #     content+=res

         
    # 返回响应
    return StreamingResponse(response, media_type='text/plain')

templates = Jinja2Templates(directory=".")

@app.get("/")
def read_item(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})


# 运行服务器
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
