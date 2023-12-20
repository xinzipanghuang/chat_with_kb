import gradio as gr
import time
from kb import LLMKnowledgeBaseManager
from chat import Conversation
from utils import LLM_MODEL


def echo(message, chat_history, kb):
    print(message, chat_history,kb)
    # bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])


    if kb is None:
        a=exist_dict.get("now")
        if a is None:
            a=Conversation(LLM_MODEL,)
            exist_dict["now"]=a
    else:
        a=exist_dict.get("now"+kb)
        if a is None:
            a=Conversation(LLM_MODEL,kb)

            exist_dict["now"+kb]=a

    response=a.start(message,chat_history)
    content=""
    for res in response:
        content+=res
        time.sleep(0.02)
        yield content



if __name__ == "__main__":
    exist_dict={}
    kb_manager=LLMKnowledgeBaseManager()
    demo = gr.ChatInterface(echo, 
                            chatbot=gr.Chatbot(height=600),
                            additional_inputs=[
                                # gr.Textbox("知识库", label="System Prompt"), 
                                gr.Radio(
                                        [i[1] for i in kb_manager.table_info], label="知识库KnowledgeBase", info="Chat with Documents!"
                                    ) ]
                        )

    demo.queue().launch()