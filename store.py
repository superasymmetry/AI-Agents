import os
import json
from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings
from groq import Groq
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from agents.auto import AutomationAgent
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

agent = AutomationAgent()
agent.get_major_controls(agent.root_control)
ui_features = agent.getTree()
print(ui_features)


os.environ["GROQ_API_KEY"] = "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"
documents = []
for control_type, elements in ui_features.items():
    for element in elements:
        content = (
            f"Control Type: {control_type}\n"
            f"Feature: {element['feature']}\n"
            f"Coordinates: {element['coordinates']}"
        )
        metadata = {
            "control_type": control_type,
            "feature": element["feature"],
            "coordinates": element["coordinates"]
        }
        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(documents)

len(all_splits)

vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

retrieved_docs = retriever.invoke("What are the coordinates of google chrome?")

len(retrieved_docs)
print(retrieved_docs[0].page_content)