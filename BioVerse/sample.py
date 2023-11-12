import autogen

config_list = autogen.config_list_from_json(
    "modelConfig.json",
    filter_dict={
        "model": [ "gpt-3.5-turbo"],
    },
)

# Accepted file formats for that can be stored in 
# a vector database instance
from autogen.retrieve_utils import TEXT_FORMATS

print("Accepted file formats for `docs_path`:")
print(TEXT_FORMATS)

from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb

# 1. create an RetrieveAssistantAgent instance named "assistant"
assistant = RetrieveAssistantAgent(
    name="assistant", 
    system_message="You are a helpful assistant.",
    llm_config={
        "timeout": 600,
        "cache_seed": 42,
        "config_list": config_list,
    },
)

# 2. create the RetrieveUserProxyAgent instance named "ragproxyagent"
# By default, the human_input_mode is "ALWAYS", which means the agent will ask for human input at every step. We set it to "NEVER" here.
# `docs_path` is the path to the docs directory. It can also be the path to a single file, or the url to a single file. By default, 
# it is set to None, which works only if the collection is already created.
# 
# Here we generated the documentations from FLAML's docstrings. Not needed if you just want to try this notebook but not to reproduce the
# outputs. Clone the FLAML (https://github.com/microsoft/FLAML) repo and navigate to its website folder. Pip install and run `pydoc-markdown`
# and it will generate folder `reference` under `website/docs`.
#
# `task` indicates the kind of task we're working on. In this example, it's a `code` task.
# `chunk_token_size` is the chunk token size for the retrieve chat. By default, it is set to `max_tokens * 0.6`, here we set it to 2000.
ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    retrieve_config={
        "task": "code",
        "docs_path": "sampleagentsdocs",  # change this to your own path, such as https://raw.githubusercontent.com/microsoft/autogen/main/README.md
        "chunk_token_size": 2000,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="chromadb"),
        "embedding_model": "all-mpnet-base-v2",
        "get_or_create": True,  # set to False if you don't want to reuse an existing collection, but you'll need to remove the collection manually
    },
)

# reset the assistant. Always reset the assistant before starting a new conversation.
assistant.reset()

# given a problem, we use the ragproxyagent to generate a prompt to be sent to the assistant as the initial message.
# the assistant receives the message and generates a response. The response will be sent back to the ragproxyagent for processing.
# The conversation continues until the termination condition is met, in RetrieveChat, the termination condition when no human-in-loop is no code block detected.
# With human-in-loop, the conversation will continue until the user says "exit".
code_problem = "What skills does this candidate have."
ragproxyagent.initiate_chat(assistant, problem=code_problem, search_string="")