'''Exploring the capabilities of autogen framework by Microsoft Reasearch
'''


import autogen # type: ignore


def two_way_chat(task: str, config_list):
    '''
    '''
    assistant = autogen.AssistantAgent(
        name= "Assistant",
        llm_config={
            "config_list": config_list
        }
    )
    user_proxy = autogen.UserProxyAgent(
        name="user",
        human_input_mode="NEVER", # "TERMINATE" or "ALWAYS"
        code_excecution_config={
            "work_dir": "agent_code",
            "use_docker": False
        },
        is_termination_message=lambda msg:  "TERMINATE" in msg['content']
    )
    user_proxy.initiate_chat(assistant, message=task)


def group_chat(
    task: str, config_list, llm_config: dict, max_round: int=10
) -> None:
    '''
    '''
    coder = autogen.AssistantAgent(
        name= "Coder",
        system_message='''
        Your task is to write code to implement a web scraping bot which collects
        data from X formerly known as Twitter about the US politics and Donald Trump in particular.
        ''',
        llm_config={"config_list": config_list, "temperature": 0}
    )
    uat_tester = autogen.AssistantAgent(
        name= "Assistant",
        system_message='''
        Your task is to perform code quality checks for the code written and suggest how the
        code can be improved. check error and run the code to actually see if the bot executes
        successfully
        ''',
        llm_config={"config_list": config_list, "temperature": 0}
    )
    cto = autogen.AssistantAgent(
        name= "Chief Technology Officer",
        system_message='''
        Your task is to check if the code conforms with the industry standards and check if the
        SOLID principles are implemented accordingly. Lastly, check if the project at hand is
        attained by the code implementation.
        ''',
        llm_config={"config_list": config_list, "temperature": 0}
    )
    user_proxy = autogen.UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        code_excecution_config={
            "work_dir": "agent_code",
            "use_docker": False
        }
    )
    group = autogen.GroupChat(
        agents=[coder, uat_tester, cto], message=task, max_round=max_round
    )
    manager = autogen.GroupChatManager(group_chat=group, llm_config=llm_config)
    user_proxy.initiate_chat(manager, message=task)


def sequential_chat():
    '''
    '''


def nested_chat():
    '''
    '''


def main():
    task = "You're to write code to flatten a list given that all the elements are lists"
    config_list = autogen.config_list_from_json(
        env_or_file= "OAI_CONFIG_LIST.json"
    )
    two_way_chat(config_list=config_list, task=task)


if __name__ == "__main__":
    main()
