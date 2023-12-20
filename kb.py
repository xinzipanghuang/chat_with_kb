import os
from db import DatabaseHandler
from langchain.document_loaders import TextLoader,CSVLoader,JSONLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import argparse

# os.environ['HTTP_PROXY'] = "http://127.0.0.1:10809"
# os.environ['HTTPS_PROXY'] = "http://127.0.0.1:10809"


def Embedding():
    
    # model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    model_name="thenlper/gte-large-zh"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    hf = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return  hf

class LLMKnowledgeBaseManager:
    def __init__(self,db_name="./database/FAQ.sqlite",table_name="LLMKnowledgeBase",db_save_dir="./knowledgebase"):
        
        self.db_name=db_name
        if not os.path.exists(os.path.dirname(db_name)):
            os.makedirs(os.path.dirname(db_name),exist_ok=True)
        self.table_name=table_name
        self.db_save_dir=db_save_dir
        if not os.path.exists(db_save_dir):
            os.makedirs(db_save_dir,exist_ok=True)
        self.dbhandler=DatabaseHandler(self.db_name,self.table_name)
        self.columns=['id','db_name','location']
        self.dbhandler.create_table(columns=dict(zip(self.columns,["int","str","str"])))
        self.table_info=self.dbhandler.query_data()
        # print(self.table_info)

    def create_kb(self,text_file,kb_name,chunk_size=1000,chunk_overlap=200):
        ext=os.path.splitext(text_file)[-1][1:]
        if ext.lower()=="csv":
            loader = CSVLoader(text_file,encoding='utf-8')
        elif ext.lower()=="txt":
            loader = TextLoader(text_file,encoding='utf-8')
        else:
            raise ValueError("未知的文本类型，无法识别，仅支持 txt,csv")
        
        is_exist,id,db_name,location=self.fetch_kb_info(kb_name)
        if not is_exist:
            documents = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            texts = text_splitter.split_documents(documents)
            embedding_model=Embedding()
            db = FAISS.from_documents(texts, embedding_model)
            db.save_local(os.path.join(self.db_save_dir,kb_name))
            self.dbhandler.insert_data(data=dict(zip(self.columns,[len(self.table_info)+1,kb_name,self.db_save_dir])))
        else:
            # raise FileExistsError(f"{kb_name} 该知识库名称已存在，请换个知识库名称")
            documents = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            texts = text_splitter.split_documents(documents)
            embedding_model=Embedding()
            db = FAISS.from_documents(texts, embedding_model)
            db.save_local(os.path.join(self.db_save_dir,kb_name))
            self.dbhandler.update_data(data=dict(zip(self.columns,[id,kb_name,self.db_save_dir])),condition=f"id= {id}")


        return True
    
    def fetch_kb_info(self,kb_name):
        for row in self.table_info:
            if row[1]==kb_name:
                return True,*row
        return False,None,None,None
    
    def fetch_kb(self,kb_name,):
        is_exist,id,db_name,location=self.fetch_kb_info(kb_name)
        if not is_exist:
            raise FileExistsError(f"{kb_name} vector database 不存在")
        db = FAISS.load_local(os.path.join(location,db_name),Embedding())
        return db
    
    def save_kb(self):
        pass

'''
python kb.py -i ./CNVseq.csv -o ./knowledgebase -s ./database/FAQ.sqlite -t LLMKnowledgeBase -n CNV-seq
python kb.py -i state_of_the_union.txt -o ./knowledgebase -s ./database/FAQ.sqlite -t LLMKnowledgeBase -n state_of_the_union

'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Create Knowledge base with csv,txt',
    )

    parser.add_argument('-i', '--input', type=str,
                        help='Input text file path', required=True)

    parser.add_argument('-o', '--output', type=str,default="./knowledgebase",
                        help='vector database save location, directory')

    parser.add_argument('-s', '--sqlite', type=str, default="./database/FAQ.sqlite",
                        help='sqlite database file location')

    parser.add_argument('-t', '--table', type=str,default="LLMKnowledgeBase",
                        help='database table save name',)

    parser.add_argument('-n', '--kb-name', type=str,
                        help=' Knowledge base name',required=True)
    args = parser.parse_args()

    a=LLMKnowledgeBaseManager(args.sqlite,args.table,args.output)
    a.create_kb(args.input,args.kb_name)

    print("Done!")