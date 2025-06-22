from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
import certifi
from langserve import add_routes
from langserve.validation import chainBatchRequest

from dotenv import load_dotenv
load_dotenv()

os.environ['SSL_CERT_FILE'] = certifi.where()
groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

# Create prompt template
system_template = "Translate the following into {language}"
prompt_template = ChatPromptTemplate.from_messages([
    ('system',system_template),
    ('user','{text}')
])

perser = StrOutputParser()

# create chain
chain = prompt_template|model|StrOutputParser
# Fix: explicitly rebuild the model to satisfy Pydantic v2
chainBatchRequest.model_rebuild()
# App definition
app=FastAPI(title="Langchain Server",
            version="1.0",
            description="A simple API server using langchain runnable interfaces")



# adding chain routes
add_routes(
    app,
    chain,
    path='/chain'
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8080)