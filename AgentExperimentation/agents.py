import os
import getpass

# import langchain packages
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_types import AgentType
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

# define directories
base_dir = os.getcwd()

bioinformatics_pdf_dir = os.path.join(base_dir, 'BioinformaticsPDF')
experimentalist_pdf_dir = os.path.join(base_dir, 'ExperimentalistPDF')
image_analysis_pdf_dir = os.path.join(base_dir, 'ImageAnalystPDF')
research_assistant_pdf_dir = os.path.join(base_dir, 'ResearchAssistantPDF')

bioinformatics_database_dir = os.path.join(base_dir, 'BioinformaticsDatabase')
experimentalist_database_dir = os.path.join(base_dir, 'ExperimentalistDatabase')
image_analysis_database_dir = os.path.join(base_dir, 'ImageAnalystDatabase')
research_assistant_database_dir = os.path.join(base_dir, 'ResearchAssistantDatabase')

os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key:')


class BioinformaticsAgent:
    def __init__(self,
                 llm=ChatOpenAI(model_name='gpt-4',temperature=0.1),
                 persist_dir=bioinformatics_database_dir,
                 embedding=OpenAIEmbeddings()):
        self.memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True)
        self.db = Chroma(persist_directory=persist_dir,
                  embedding_function=embedding)

        self.retriever = self.db.as_retriever()

        self.template = """You the bioinformatician. You can help me with analyzing and interpreting biological data. 
        Your skills include statistical analysis, DNA/RNA sequencing analysis, designing bioinformatics workflows, 
        and providing guidance on best practices for computational biology research. Please help me analyze and make 
        sense of large-scale omics data.
        Chat History:
        {chat_history}
        Follow Up Input: {question}
        Standalone question:"""
        self.prompt = PromptTemplate.from_template(self.template)
        # Create the chain to answer questions
        self.qa = ConversationalRetrievalChain.from_llm(
                                                          llm=llm,
                                                          retriever=self.retriever,
                                                          memory=self.memory,
                                                          condense_question_prompt=self.prompt
                                      )

    def invoke(self,query):
        result = self.qa({"question":query})
        return result['answer']



