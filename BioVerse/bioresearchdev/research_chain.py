import json
import os
import logging
from bioresearchdev.utils import now, log_and_print_online
from bioresearchdev.research_lab import ResearchEnvConfig, ResearchEnv
import importlib
import shutil
from datetime import datetime
from bioresearchdev.statistics import get_info
import time


from pprint import pprint

def check_bool(s):
    return s.lower() == "true"


class ResearchChain:
    def __init__(self,
                 config_path: str = None,
                 config_phase_path: str = None,
                 config_role_path: str = None,
                 task_prompt: str = None,
                 research_name: str = None,
                 lab_name: str = None,
                 model_type: str='gpt-3.5-turbo',
                 code_path: str = None) -> None:
        
        self.config_path = config_path
        self.config_phase_path = config_phase_path
        self.config_role_path = config_role_path
        self.research_name = research_name
        self.lab_name = lab_name
        self.model_type = model_type
        self.code_path = code_path
                
        with open(self.config_path, 'r', encoding="utf8") as file:
            self.config = json.load(file)
        with open(self.config_phase_path, 'r', encoding="utf8") as file:
            self.config_phase = json.load(file)
        with open(self.config_role_path, 'r', encoding="utf8") as file:
            self.config_role = json.load(file)

        # init chatchain config and recruitments
        self.chain = self.config["chain"]
        self.recruitments = self.config["recruitments"]
        

        # init default max chat turn
        self.chat_turn_limit_default = 10

        # init ChatEnv
        self.research_env_config = ResearchEnvConfig(clear_structure=check_bool(self.config["clear_structure"]),
                                             gui_design=check_bool(self.config["gui_design"]),
                                             git_management=check_bool(self.config["git_management"]),
                                             incremental_develop=check_bool(self.config["incremental_develop"]))
        self.research_env = ResearchEnv(self.research_env_config)
        
        # the user input prompt will be self-improved (if set "self_improve": "True" in ResearchChainConfig.json)
        # the self-improvement is done in self.preprocess
        self.task_prompt_raw = task_prompt
        self.task_prompt = ""


        # TODO: This should be checked properly befor experimenting
        # init role prompts
        self.role_prompts = dict()
        for role in self.config_role:
            self.role_prompts[role] = "\n".join(self.config_role[role])
        # TODO: This should initialize agents instead
        self.get_logfilepath()
        
        # TODO: This should be worked on properly
        # init SimplePhase instances
        # import all used phases in PhaseConfig.json from chatdev.phase
        # note that in PhaseConfig.json there only exist SimplePhases
        # ComposedPhases are defined in ChatChainConfig.json and will be imported in self.execute_step
        # self.compose_phase_module = importlib.import_module("bioresearchdev.composed_phase")
        self.phase_module = importlib.import_module("bioresearchdev.phase")
     
        self.phases = dict()
        for phase in self.config_phase:
            # agents = self.config_phase[phase]['agents']
            # phase_name = self.config_phase[phase]['phase_name']
            # phase_prompt = "\n\n".join(self.config_phase[phase]['phase_prompt'])
            # phase_class = getattr(self.phase_module, phase)
            # TODO: check
            # phase_instance = phase_class(
            #                              agent=user_role_name,
            #                              phase_prompt=phase_prompt,
            #                              phase_name=phase,
            #                              model_type=self.model_type,
            #                              log_filepath=self.log_filepath)
            self.phases[phase] = None
                
        
    
    def get_logfilepath(self):
        """
        get the log path (under the software path)
        Returns:
            start_time: time for starting making the software
            log_filepath: path to the log

        """
        # initiate start time of the research process
        start_time = now()
        # get the directory name of the run file path of this file
        filepath = os.path.dirname(__file__)
        
        # get the root directory
        root = os.path.dirname(filepath)

        # set a library directory, check it exists, if it does not exist create it
        directory = os.path.join(root, "Library")
        if not os.path.exists(directory):
            os.makedirs(directory)
    
        self.log_filepath = os.path.join(directory,
                                    "{}.log".format("_".join(["".join(self.research_name.split()), "".join(self.lab_name.split()), start_time,])))
        self.start_time = start_time
    
    def make_recruitment(self):
        """
        recruit all employees
        Returns: None

        """
        for employee in self.recruitments:
            self.research_env.recruit(agent_name=employee)
    
    
    def pre_processing(self):
        """
        remove useless files and log some global config settings
        Returns: None

        """
        if self.research_env.config.clear_structure:
            filepath = os.path.dirname(__file__)
            root = os.path.dirname(filepath)
            directory = os.path.join(root, "Library")
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                # logs with error trials are left in WareHouse/
                if os.path.isfile(file_path) and not filename.endswith(".py") and not filename.endswith(".log"):
                    os.remove(file_path)
                    print("{} Removed.".format(file_path))

        self.software_path = os.path.join(directory,"_".join(["".join(self.research_name.split()), "".join(self.lab_name.split()), self.start_time,]))
        self.research_env.env_dict["directory"] = self.software_path
        if not os.path.exists(self.software_path):
            os.mkdir(self.software_path)

        # write task prompt to software
        with open(os.path.join(self.software_path, self.research_name + ".prompt"), "w") as f:
            f.write(self.task_prompt_raw)

        preprocess_msg = "**[Preprocessing]**\n\n"

        preprocess_msg += "**Research Process Starts** ({})\n\n".format(self.start_time)
        preprocess_msg += "**Timestamp**: {}\n\n".format(self.start_time)
        preprocess_msg += "**config_path**: {}\n\n".format(self.config_path)
        preprocess_msg += "**config_phase_path**: {}\n\n".format(self.config_phase_path)
        preprocess_msg += "**config_role_path**: {}\n\n".format(self.config_role_path)
        preprocess_msg += "**task_prompt**: {}\n\n".format(self.task_prompt_raw)
        preprocess_msg += "**project_name**: {}\n\n".format(self.research_name)
        preprocess_msg += "**Log File**: {}\n\n".format(self.log_filepath)
        preprocess_msg += "**ResearchEnvConfig**:\n{}\n\n".format(self.research_env.config.__str__())
        preprocess_msg += "**ChatGPTConfig**:\n{}\n\n".format("ChatGPTConfig(temperature=0.2, top_p=1.0, n=1, stream=False, stop=None, max_tokens=None, presence_penalty=0.0, frequency_penalty=0.0, logit_bias={}, user='')")
        log_and_print_online(preprocess_msg)

        # init task prompt
        if check_bool(self.config['self_improve']):
            self.research_env.env_dict['task_prompt'] = self.self_task_improve(self.task_prompt_raw)
        else:
            self.research_env.env_dict['task_prompt'] = self.task_prompt_raw

    
    # # # TODO: do recruitments for all the scientists in the lab
    def execute_chain(self):
        """
        execute the whole chain based on ChatChainConfig.json
        Returns: None

        """
        for phase_item in self.chain:
            self.execute_step(phase_item)
            
            
    def execute_step(self, phase_item: dict):
        """
        execute single phase in the chain
        Args:
            phase_item: single phase configuration in the ChatChainConfig.json

        Returns:

        """
        phase = phase_item['phase']
        max_turn_step = phase_item.get('max_turn_step', -1)
        need_reflect = check_bool(phase_item.get('need_reflect', 'True'))
        self.research_env = self.phases[phase].execute(self.research_env,
                                                        self.chat_turn_limit_default if max_turn_step <= 0 else max_turn_step,
                                                        need_reflect)
        
    
    def post_processing(self):
        """
        summarize the production and move log files to the software directory
        Returns: None

        """

        self.research_env.write_meta()
        filepath = os.path.dirname(__file__)
        root = os.path.dirname(filepath)

        post_info = "**[Post Info]**\n\n"
        now_time = now()
        time_format = "%Y%m%d%H%M%S"
        datetime1 = datetime.strptime(self.start_time, time_format)
        datetime2 = datetime.strptime(now_time, time_format)
        duration = (datetime2 - datetime1).total_seconds()

        # TODO: resolve issue with info generation
        # post_info += "Software Info: {}".format(
        #     get_info(self.research_env.env_dict['directory'], self.log_filepath) + "\n\n🕑**duration**={:.2f}s\n\n".format(
        #         duration))

        post_info += "Research Process Starts ({})".format(self.start_time) + "\n\n"
        post_info += "Research Process Ends ({})".format(now_time) + "\n\n"

        log_and_print_online(post_info)

        logging.shutdown()
        time.sleep(1)