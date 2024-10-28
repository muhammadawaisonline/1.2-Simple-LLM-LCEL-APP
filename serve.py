import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from fastapi import FastAPI
 

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

model = ChatGroq(model="llama3.2", GROQ_API_KEY= GROQ_API_KEY)

#1 Create Prompt template 
system_template = "Translate into {language}"
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("sytem", system_template),
        ("user", "{text}")
    ]
)

parser = StrOutputParser()

#2 Create chain
chain = prompt_template | model | parser

chain.invoke({"language": "French", "text": "Hello"})

#3 App Definition
app = FastAPI(title="Langchain Server", version= "1.0", description="A Simple LLM Translator App")

#4 Adding Chain routes

add_routes(
    app, 
    chain,
    path="/chain"
)

if __name__ == "__main__":
    import unicorn
    # unicorn.run(app, host= "localhost", port= 8000)
    unicorn.run(app, host= "127.0.0.1", port= 8000)