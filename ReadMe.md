## FAQ知识库智能问答

### 环境准备
需要python环境
```
pip install -r requirements.txt 
```
### 添加APIKEY

utils.py apikey="" 添加KEY

### 知识库建立

现已有CNV-seq 和state of union 两个测试数据库。

目前支持txt和csv的知识库材料输入，注意不要出现人名等敏感信息。知识库名称不要重复，重复则会替换。

```
python kb.py -i ./CNVseq.csv -o ./knowledgebase -s ./database/FAQ.sqlite -t LLMKnowledgeBase -n CNV-seq
```

### demo 界面运行

```
python demo.py
```

界面会自动在数据库中搜索所构建的知识库。
不选任何参数，默认为与LLM进行对话。
### 其他

可以在`utils.py`中更改`api_key`或者更换LLM。

