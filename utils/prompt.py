from langchain_core.prompts import ChatPromptTemplate

system_prompt = (
    "You are an intelligent chatbot. Use the following context to answer the question. If you don't know the answer, just say that you don't know."
    "\n\n"
    "{context}"
)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)