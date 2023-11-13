import os
import re
from abc import ABC, abstractmethod

from bioresearchdev.research_lab import ResearchEnv
from bioresearchdev.statistics import get_info
from bioresearchdev.utils import log_and_print_online, log_arguments
from bioresearchdev.agents import PrincipalInvestigatorProxy, config_list
import autogen

config_list_gpt4 = autogen.config_list_from_json(
    "modelConfig.json",
    filter_dict={
        "model": ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
    },
)

llm_config = {"config_list": config_list_gpt4, "cache_seed": 42}

class Phase(ABC):

    def __init__(self,
                 agents,
                 phase_prompt,
                 phase_name,
                 research_path,
                 log_filepath):
        """

        Args:
            assistant_role_name: who receives chat in a phase
            user_role_name: who starts the chat in a phase
            phase_prompt: prompt of this phase
            role_prompts: prompts of all roles
            phase_name: name of this phase
        """
        self.agents = agents
        self.seminar_conclusion = None
        self.phase_prompt = phase_prompt
        self.phase_name = phase_name
        self.log_filepath = log_filepath
        self.research_path = research_path

    @abstractmethod
    def update_chat_env(self, research_env):
        """
        update chan_env based on the results of self.execute, which is self.seminar_conclusion
        must be implemented in customized phase
        the usual format is just like:
        ```
            chat_env.xxx = some_func_for_postprocess(self.seminar_conclusion)
        ```
        Args:
            chat_env:global chat chain environment

        Returns:
            chat_env: updated global chat chain environment

        """
        return research_env
    
    @log_arguments
    def execute(self, phase_instruction, research_env, chat_turn_limit):
        """
        execute this particular phase
        Args:
            chat_env: global chat chain environment
            chat_turn_limit: turn limit in each chat
            need_reflect: flag for reflection

        Returns:
            chat_env: updated global chat chain environment using the conclusion from this phase execution

        """
        
        print(self.norag_chat())
        # perform update on the research enviroment with relevant infomation after the process has been completed
        research_env = self.update_chat_env()
        return research_env
    
    def _reset_agents(self):
        for agent in self.agents:
            agent.reset()
            
    def rag_chat(self):
        self._reset_agents()
        groupchat = autogen.GroupChat(
            agents=self.agents, messages=[], max_round=12
        )
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

        # Start chatting with boss_aid as this is the user proxy agent.
        PrincipalInvestigatorProxy.initiate_chat(
            manager,
            problem=self.phase_prompt,
            n_results=3,
        )
    
    def norag_chat(self):
        self._reset_agents()
        groupchat = autogen.GroupChat(
            agents=self.agents, messages=[], max_round=12
        )
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

        # Start chatting with boss as this is the user proxy agent.
        PrincipalInvestigatorProxy.initiate_chat(
            manager,
            message=self.phase_prompt,
        )
        
    def call_rag_chat(self):
        self._reset_agents()

        # In this case, we will have multiple user proxy agents and we don't initiate the chat
        # with RAG user proxy agent.
        # In order to use RAG user proxy agent, we need to wrap RAG agents in a function and call
        # it from other agents.
        def retrieve_content(message, n_results=3):
            PrincipalInvestigatorProxy.n_results = n_results  # Set the number of results to be retrieved.
            # Check if we need to update the context.
            update_context_case1, update_context_case2 = PrincipalInvestigatorProxy._check_update_context(message)
            if (update_context_case1 or update_context_case2) and PrincipalInvestigatorProxy.update_context:
                PrincipalInvestigatorProxy.problem = message if not hasattr(PrincipalInvestigatorProxy, "problem") else PrincipalInvestigatorProxy.problem
                _, ret_msg = PrincipalInvestigatorProxy._generate_retrieve_user_reply(message)
            else:
                ret_msg = PrincipalInvestigatorProxy.generate_init_message(message, n_results=n_results)
            return ret_msg if ret_msg else message

        PrincipalInvestigatorProxy.human_input_mode = "NEVER"  # Disable human input for boss_aid since it only retrieves content.

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
        }

        for agent in self.agents:
            # update llm_config for assistant agents.
            agent.llm_config.update(llm_config)

        for agent in self.agents:
            # register functions for all agents.
            agent.register_function(
                function_map={
                    "retrieve_content": retrieve_content,
                }
            )

        groupchat = autogen.GroupChat(
            agents=self.agents, messages=[], max_round=12
        )
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

        # Start chatting with boss as this is the user proxy agent.
        PrincipalInvestigatorProxy.initiate_chat(
            manager,
            message=self.phase_prompt,
        )