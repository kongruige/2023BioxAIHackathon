import autogen
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb

config_list = autogen.config_list_from_json(
    env_or_file="modelConfig.json",
    file_location=".",
    filter_dict={
        "model": {
            "gpt-3.5-turbo-1106"
        }
    },
)

config_list_4v = autogen.config_list_from_json(
    env_or_file="modelConfig.json",
    file_location=".",
    filter_dict={
        "model": ["gpt-4-vision-preview"],
    },
)

llm_config = {
    "timeout": 60,
    "config_list": config_list,
    "temperature": 0.5,
}
# autogen.ChatCompletion.start_logging()
termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

max_token = 1000

# define agents
PrincipalInvestigator = autogen.UserProxyAgent(
    name="Principal_Investigator",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    system_message="Hi, You are the Principal Investigator of BioVerse. Welcome to the virtual lab! Your role is to identify promising research directions, define project goals, and keep the other members on track for delivering impactful results.",
    code_execution_config=False,  # we don't want to execute code in this case.
)

PrincipalInvestigatorProxy = RetrieveUserProxyAgent(
    name="Principal_Investigator",
    is_termination_msg=termination_msg,
    system_message="Assistant who has extra content retrieval power for solving difficult problems.",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    retrieve_config={
        "task": "code",
        "docs_path": "group_chat_pdf",
        "chunk_token_size": 1000,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="group_chat_db"),
        "collection_name": "groupchat",
        "get_or_create": True,
    },
    code_execution_config=False,  # we don't want to execute code in this case.
)

PrincipalInvestigatorCritic = RetrieveAssistantAgent(
    name="Principal_Investigator",
    system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as url of research paper. Please verify the links and execute the code if possible.",
    human_input_mode="NEVER",
    llm_config={
        "timeout": 120,
        "config_list": config_list,
        "temperature": 0.5,
        "max_tokens": max_token
    }
)

ResearchAssistant = RetrieveAssistantAgent(
    name="Research_Assistant",
    is_termination_msg=termination_msg,
    system_message="Greetings, You are the research assistant. You excel at literature reviews, proposal preparations, quantitative and qualitative data collection/analysis, lab experiment assistance, and research project coordination. Please help me find relevant papers, take notes, format documents, track project timelines, locate lab equipment, ensure protocol adherence, or any other tasks that will accelerate my research!",
    human_input_mode="NEVER",
    llm_config={
        "timeout": 120,
        "config_list": config_list,
        "temperature": 0.5,
        "max_tokens": max_token
    }
)

ImageAnalyst = RetrieveAssistantAgent(
    name="Image_Analyst",
    is_termination_msg=termination_msg,
    system_message="Hi there, You are the image analyst! Your specialty is processing and analyzing microscopic, radiographic, and other visual data. You can help with tasks like image segmentation, feature extraction, image registration, measuring objects in images, and classifying/annotating images using machine learning. Please provide assistance on analyzing, enhancing, or extracting meaningful information from my imaging data!",
    human_input_mode="NEVER",
    llm_config={"timeout": 120,
                "config_list": config_list,
                "temperature": 0.5,
                "max_tokens": max_token}
)

Experimentalist = RetrieveAssistantAgent(
    name="Experimentalist",
    is_termination_msg=termination_msg,
    system_message="Hello! You are the experimentalist. Your skills are in designing and conducting hands-on lab experiments, including following protocols, collecting and recording data, lab maintenance, and safe chemical/equipment handling. Please help me brainstorming experiments, setting up lab equipment, following detailed protocols, tracking measurements and observations, or assistance with other in-lab experimental work.",
    human_input_mode="NEVER",
    llm_config={
        "timeout": 120,
        "config_list": config_list,
        "temperature": 0.5,
        "max_tokens": max_token
    }
)

Bioinformatician = RetrieveAssistantAgent(
    name="Bioinformatician",
    is_termination_msg=termination_msg,
    system_message="Hello, you are the bioinformatician. You can help me with analyzing and interpreting biological data. Your skills include statistical analysis, DNA/RNA sequencing analysis, designing bioinformatics workflows, and providing guidance on best practices for computational biology research. Please help me analyze and make sense of large-scale omics data!",
    human_input_mode="NEVER",
    llm_config={
        "timeout": 120,
        "config_list": config_list,
        "temperature": 0.5,
        "max_tokens": max_token
    },
    code_execution_config={"last_n_messages": 3, "work_dir": "paper"}
)

TissueEngineer = RetrieveAssistantAgent(
    name="Tissue_Engineer",
    is_termination_msg=termination_msg,
    system_message="Hola, You are the tissue engineer here to help with designing and culturing organoid models. Your expertise includes selecting cell sources, extracellular matrix components, growth factors, and culture systems to derive organoid structures from stem cells. Please provide assistance planning organoid protocols, troubleshooting culture conditions, or analyzing resulting model viability and morphology. Please help me to advance my organ-on-a-chip and 3D tissue engineering goals!",
    human_input_mode="NEVER",
    llm_config={
        "timeout": 120,
        "config_list": config_list,
        "temperature": 0.5,
        "max_tokens": max_token
    }
)

