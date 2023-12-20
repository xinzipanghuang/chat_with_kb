from utils import LLM_MODEL
from prompt import QUERY_PROMPT,template,template_question,condense_template

from kb import LLMKnowledgeBaseManager
from history import ConversationManager
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.prompts import PromptTemplate,ChatPromptTemplate

from uuid import uuid4

from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


import logging

logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)



class LineList(BaseModel):
    # "lines" is the key (attribute name) of the parsed output
    lines: List[str] = Field(description="Lines of text")


class LineListOutputParser(PydanticOutputParser):
    def __init__(self) -> None:
        super().__init__(pydantic_object=LineList)

    def parse(self, text: str) -> LineList:
        lines = text.strip().split("\n")
        return LineList(lines=lines)



class Conversation:
    def __init__(self,llm,kb=None,chat_history=[]):

        self.chat_history=chat_history
        self.llm=llm
        self.kb=kb
        self.uuid=str(uuid4())#.replace("-","_")
        self.chat_history_list=[]
        self.chat_history=""

    def fetch_docs_from_kb(self,inputs):
        if inputs=="":
            return ""
        kb_manager=LLMKnowledgeBaseManager()
        db=kb_manager.fetch_kb(self.kb)
        output_parser = LineListOutputParser()

        llm_chain = LLMChain(llm=self.llm, prompt=QUERY_PROMPT,output_parser=output_parser)
        output_parser = LineListOutputParser()
        retriever = MultiQueryRetriever(
            retriever=db.as_retriever(search_kwargs={'k': 3, 'fetch_k': 50}), llm_chain=llm_chain,verbose=True,parser_key="lines"
        )
        docs=retriever.get_relevant_documents(query=inputs)
        return docs
    
    def answer_with_docs(self,question,docs):

        prompt = ChatPromptTemplate.from_template(template)
        prompt_msg=prompt.format(question=question,context=docs)

        reply=self.llm.stream(prompt_msg)
        return reply

    def answer_with_llm(self,question):
        prompt = ChatPromptTemplate.from_template(template_question)
        prompt_msg=prompt.format(question=question)

        reply=self.llm.stream(prompt_msg)


        return reply
    
    def condense_question(self,question):
        return question
        history=self.chat_history
        print(history)
        if history=="":
            return question
        else:
            prompt = PromptTemplate.from_template(condense_template)
            question_generator_chain = LLMChain(llm=self.llm,prompt=prompt,verbose=True)
            
            response=question_generator_chain.run({"question":question,"chat_history":history})
            
            if response=="":
                return question
            return response






    def format_docs(self,docs):
        a="\n\n".join([d.page_content for d in docs])
        return a

    def start(self,question,chat_history):
        self.chat_history_list=chat_history
        self.chat_history= "\n".join(["Human: "+i[0].replace("\n",'\t')+"\nAI: "+i[1].replace("\n",'\t')+"\n" for i in chat_history[-2:] ])
        condense_question=self.condense_question(question)
        # print(condense_question)
        if self.kb:
            docs=self.fetch_docs_from_kb(condense_question)
            # for t,doc in enumerate(docs):
            #     print(t,doc.page_content)

            if docs==[]:
                response= self.answer_with_llm(condense_question)
            else:
                response= self.answer_with_docs(condense_question,docs)
        else:
            response= self.answer_with_llm(condense_question)

        tmp=response
        
        content=""
        for chunk in response:

            content+=chunk.content
            yield chunk.content
        print(content)
        dbmanger=ConversationManager()
        item=dbmanger.fetch_uuid(self.uuid)
        if len(item)==0:
            message=f"Human: {question}\t AI: {content}\n"
            info=[len(dbmanger.table_info)+1,self.uuid,datetime.now().strftime("%Y-%m-%d %H:%M:%S"),self.kb,message]
            dbmanger.add_item(info)
        else:
            message=f"Human: {question}\t AI: {content}\n"
            info=list(item[0])[:-1]+[list(item[0])[-1]+message]
            dbmanger.update_item(info,self.uuid)

    

if __name__ == "__main__":
    api_key="sk-77f54bfeb4eb4dda83e115e2687d8564"
    a=Conversation(LLM_MODEL,kb='CNV-seq')

    for res in a.start("CNV-seq数据校正如何实现",[]):
        print(res,end=" ",flush=True)
        pass
