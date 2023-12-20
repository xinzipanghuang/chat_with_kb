import os
from db import DatabaseHandler


class ConversationManager:
    def __init__(self,db_name="./database/FAQ.sqlite",table_name="ConversationHistory"):
        
        self.db_name=db_name
        if not os.path.exists(os.path.dirname(db_name)):
            os.makedirs(os.path.dirname(db_name),exist_ok=True)
        self.table_name=table_name
        self.dbhandler=DatabaseHandler(self.db_name,self.table_name)
        self.columns=['id',"uuid",'start_time','knowledgebase','history']
        self.dbhandler.create_table(columns=dict(zip(self.columns,["int","str","str",'str','str'])))
        self.table_info=self.dbhandler.query_data()

    def add_item(self,item):

        self.dbhandler.insert_data(data=dict(zip(self.columns,item)))

    def update_item(self,item,uuid):
        self.dbhandler.update_data(data=dict(zip(self.columns,item)),condition=f"uuid= '{uuid}'")

    def fetch_uuid(self,uuid):
        
        return self.dbhandler.query_data(condition=f"uuid= '{uuid}'")
    
if __name__ == "__main__":
    a=ConversationManager("./database/FAQ.sqlite","LLMKnowledgeBase")
    a.create_kb(r"D:\AIBio\20231204_chat_kb\CNVseq.csv","CNV-seq")