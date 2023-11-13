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

assert len(config_list) > 0
print("models to use: ", [config_list[i]["model"] for i in range(len(config_list))])

assert len(config_list_4v) > 0
print("vision models to use: ", [config_list_4v[i]["model"] for i in range(len(config_list))])

# autogen.ChatCompletion.start_logging()
termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

max_token = 1000

# define agents
PI = autogen.UserProxyAgent(
    name="PI",
    is_termination_msg=termination_msg,
    human_input_mode="NEVER",
    system_message="Hi, You are the Principal Investigator of BioVerse. Welcome to the virtual lab! Your role is to identify promising research directions, define project goals, and keep the other members on track for delivering impactful results. Prompt for feedbacks when necessary.",
    code_execution_config=False,  # we don't want to execute code in this case.
)

PI_aid = RetrieveUserProxyAgent(
    name="PI_Assistant",
    is_termination_msg=termination_msg,
    system_message="Assistant who has extra content retrieval power for solving difficult problems. ",
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

critic = RetrieveAssistantAgent(
    name="PI",
    system_message="You are the critic. Always be critical and jump in the conversation when suitable. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as url of research paper. Please verify the links and execute the code if possible. Prompt for feedbacks when necessary. KEEP ENGAGING IN CONVERSATION AND DO NOT STOP THE CONVERSATION!",
    human_input_mode="NEVER",
    llm_config={
        "timeout": 120,
        "config_list": config_list,
        "temperature": 0.5,
        "max_tokens": max_token
    }
)

research_assistant_assistant = RetrieveAssistantAgent(
    name="research_assistant_agent",
    is_termination_msg=termination_msg,
    system_message="Greetings, You are the research assistant. You excel at literature reviews, proposal preparations, quantitative and qualitative data collection/analysis, lab experiment assistance, and research project coordination. Please help me find relevant papers, take notes, format documents, track project timelines, locate lab equipment, ensure protocol adherence, or any other tasks that will accelerate my research. Prompt for feedbacks when necessary. KEEP ENGAGING IN CONVERSATION AND DO NOT STOP THE CONVERSATION!",
    human_input_mode="NEVER",
    llm_config={
        "timeout": 120,
        "config_list": config_list,
        "temperature": 0.5,
        "max_tokens": max_token
    }
)

image_analyst_assistant = RetrieveAssistantAgent(
    name="image_analyst_agent",
    is_termination_msg=termination_msg,
    system_message="Hi there, You are the image analyst! Your specialty is processing and analyzing microscopic, radiographic, and other visual data. You can help with tasks like image segmentation, feature extraction, image registration, measuring objects in images, and classifying/annotating images using machine learning. Please provide assistance on analyzing, enhancing, or extracting meaningful information from my imaging data! Prompt for feedbacks when necessary. KEEP ENGAGING IN CONVERSATION AND DO NOT STOP THE CONVERSATION!",
    human_input_mode="NEVER",
    llm_config={"timeout": 120,
                "config_list": config_list,
                "temperature": 0.5,
                "max_tokens": max_token}
)

experimentalist_assistant = RetrieveAssistantAgent(
    name="experimentalist_agent",
    is_termination_msg=termination_msg,
    system_message="Hello! You are the experimentalist. Your skills are in designing and conducting hands-on lab experiments, including following protocols, collecting and recording data, lab maintenance, and safe chemical/equipment handling. Please help me brainstorming experiments, setting up lab equipment, following detailed protocols, tracking measurements and observations, or assistance with other in-lab experimental work. Prompt for feedbacks when necessary. KEEP ENGAGING IN CONVERSATION AND DO NOT STOP THE CONVERSATION!",
    human_input_mode="NEVER",
    llm_config={
        "timeout": 120,
        "config_list": config_list,
        "temperature": 0.5,
        "max_tokens": max_token
    }
)

bioinformatics_assistant = RetrieveAssistantAgent(
    name="bioinformatics_agent",
    is_termination_msg=termination_msg,
    system_message="Hello, you are the bioinformatician. You can help me with analyzing and interpreting biological data. Your skills include statistical analysis, DNA/RNA sequencing analysis, designing bioinformatics workflows, and providing guidance on best practices for computational biology research. Please help me analyze and make sense of large-scale omics data! Prompt for feedbacks when necessary. KEEP ENGAGING IN CONVERSATION AND DO NOT STOP THE CONVERSATION!",
    human_input_mode="NEVER",
    llm_config={
        "timeout": 120,
        "config_list": config_list,
        "temperature": 0.5,
        "max_tokens": max_token
    },
    code_execution_config={"last_n_messages": 3, "work_dir": "paper"}
)

tissue_engineering_assistant = RetrieveAssistantAgent(
    name="tissue_engineering_agent",
    is_termination_msg=termination_msg,
    system_message="Hola, You are the tissue engineer here to help with designing and culturing organoid models. Your expertise includes selecting cell sources, extracellular matrix components, growth factors, and culture systems to derive organoid structures from stem cells. Please provide assistance planning organoid protocols, troubleshooting culture conditions, or analyzing resulting model viability and morphology. Please help me to advance my organ-on-a-chip and 3D tissue engineering goals! Prompt for feedbacks when necessary. KEEP ENGAGING IN CONVERSATION AND DO NOT STOP THE CONVERSATION!",
    human_input_mode="NEVER",
    llm_config={
        "timeout": 120,
        "config_list": config_list,
        "temperature": 0.5,
        "max_tokens": max_token
    }
)

PROBLEM = ""

llm_config = {
    "timeout": 60,
    # "seed": 50,
    "config_list": config_list,
    "temperature": 0.5,
}


def _reset_agents():
    PI.reset()
    PI_aid.reset()
    research_assistant_assistant.reset()
    bioinformatics_assistant.reset()
    experimentalist_assistant.reset()
    image_analyst_assistant.reset()
    critic.reset()


def rag_chat():
    _reset_agents()
    groupchat = autogen.GroupChat(
        agents=[PI_aid, research_assistant_assistant, bioinformatics_assistant, experimentalist_assistant,
                image_analyst_assistant, tissue_engineering_assistant, critic], messages=[], max_round=12
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Start chatting with boss_aid as this is the user proxy agent.
    PI_aid.initiate_chat(
        manager,
        problem=PROBLEM,
        n_results=1,
    )


def norag_chat():
    _reset_agents()
    groupchat = autogen.GroupChat(
        agents=[PI_aid, research_assistant_assistant, bioinformatics_assistant, experimentalist_assistant,
                image_analyst_assistant, tissue_engineering_assistant, critic], messages=[], max_round=20
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Start chatting with boss as this is the user proxy agent.
    PI.initiate_chat(
        manager,
        message=PROBLEM,
    )


def call_rag_chat():
    _reset_agents()

    # In this case, we will have multiple user proxy agents and we don't initiate the chat
    # with RAG user proxy agent.
    # In order to use RAG user proxy agent, we need to wrap RAG agents in a function and call
    # it from other agents.
    def retrieve_content(message, n_results=3):
        PI_aid.n_results = n_results  # Set the number of results to be retrieved.
        # Check if we need to update the context.
        update_context_case1, update_context_case2 = PI_aid._check_update_context(message)
        if (update_context_case1 or update_context_case2) and PI_aid.update_context:
            PI_aid.problem = message if not hasattr(PI_aid, "problem") else PI_aid.problem
            _, ret_msg = PI_aid._generate_retrieve_user_reply(message)
        else:
            ret_msg = PI_aid.generate_init_message(message, n_results=n_results)
        return ret_msg if ret_msg else message

    PI_aid.human_input_mode = "NEVER"  # Disable human input for boss_aid since it only retrieves content.

    llm_config = {
        "functions": [
            {
                "name": "retrieve_content",
                "description": "retrieve content for code generation and question answering.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Refined message which keeps the original meaning and can be used to retrieve content for code generation and question answering.",
                        }
                    },
                    "required": ["message"],
                },
            },
        ],
        "config_list": config_list,
        "timeout": 60,
        "seed": 42,
    }

    for agent in [research_assistant_assistant, bioinformatics_assistant, experimentalist_assistant,
                  image_analyst_assistant, tissue_engineering_assistant, critic]:
        # update llm_config for assistant agents.
        agent.llm_config.update(llm_config)

    for agent in [PI, research_assistant_assistant, bioinformatics_assistant, experimentalist_assistant,
                  image_analyst_assistant, tissue_engineering_assistant, critic]:
        # register functions for all agents.
        agent.register_function(
            function_map={
                "retrieve_content": retrieve_content,
            }
        )

    groupchat = autogen.GroupChat(
        agents=[PI, research_assistant_assistant, bioinformatics_assistant, experimentalist_assistant,
                image_analyst_assistant, tissue_engineering_assistant, critic], messages=[], max_round=25
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Start chatting with boss as this is the user proxy agent.
    PI.initiate_chat(
        manager,
        message=PROBLEM,
    )

# begin chat
print(norag_chat())