class Instruction(object):
    def __init__(self, message):
        self.edited_timestamp = message.edited_timestamp
        self.timestamp = message.timestamp
        self.tts = message.tts
        self.author = message.author
        self.content = message.content
        self.embeds = message.embeds
        self.channel = message.channel
        self.server = message.server
        self.mention_everyone 
        self.mentions
        self.channel_mentions
        self.role_mentions
        self.attachments
        self.pinned

class Parser(object):

    def __init__(self, config):
        self.config = config

    def parse(self, message):
        instruction = Instruction(message)
        return instruction

    def has_command(self, instruction)
        if instruction.content.startswith(config["triggerstring"]):
            return True
        else:
            return False

    def return_command(self, instruction):
        user = instruction.author
        command, parameters = instruction.content.split(" ")[0], instruction.content.split(" ")[1]
        return user, command, parameters