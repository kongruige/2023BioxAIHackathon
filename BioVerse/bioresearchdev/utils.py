import html
import logging
import re
import time

import markdown
import inspect


def now():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())

def log_and_print_online(role, content=None):
    if not content:
        logging.info(role + "\n")
        print(role + "\n")
    else:
        print(str(role) + ": " + str(content) + "\n")
        logging.info(str(role) + ": " + str(content) + "\n")
        role = str(role)
        content = str(content)

def convert_to_markdown_table(records_kv):
    # Create the Markdown table header
    header = "| Parameter | Value |\n| --- | --- |"

    # Create the Markdown table rows
    rows = [f"| **{key}** | {value} |" for (key, value) in records_kv]

    # Combine the header and rows to form the final Markdown table
    markdown_table = header + "\n" + '\n'.join(rows)

    return markdown_table


def log_arguments(func):
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        params = sig.parameters

        all_args = {}
        all_args.update({name: value for name, value in zip(params.keys(), args)})
        all_args.update(kwargs)

        records_kv = []
        for name, value in all_args.items():
            if name in ["self", "chat_env", "task_type"]:
                continue
            value = str(value)
            value = html.unescape(value)
            value = markdown.markdown(value)
            value = re.sub(r'<[^>]*>', '', value)
            value = value.replace("\n", " ")
            records_kv.append([name, value])
        records = f"**[{func.__name__}]**\n\n" + convert_to_markdown_table(records_kv)
        log_and_print_online("System", records)

        return func(*args, **kwargs)

    return wrapper


def storeConversationMessage(sender, receiver, phase, turn, message, initial_prompt="Testing"):
    """
    Store conversation in log file
    Args:
        sender (_type_): _description_
        receiver (_type_): _description_
        phase (_type_): _description_
        turn (_type_): _description_
        message (_type_): _description_
    """
    if "_" in receiver:
        receiver = " ".join(receiver.split("_"))
        
    if "_" in sender:
        sender = " ".join(sender.split("_"))
        
    if message == " " or message == "" or message == "\n" or len(message) < 3:
        return
        
    conversation_meta = "**" + receiver + "<->" + sender + " on : " + str(phase) + ", turn " + str(turn) + "**\n\n"
    # we log the second interaction here
    log_and_print_online(sender,
                            conversation_meta + "[" + initial_prompt + "]\n\n" + message)
       