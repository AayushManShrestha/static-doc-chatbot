# app/prompts.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", "Given a chat history and the latest user question which might reference the chat history, formulate a standalone question which can be understood without the chat history."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that answers questions based on the provided context and chat history.\n\n{context}"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
