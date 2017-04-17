class Instruction(object):
    def __init__(self, message, command, parameters):

        self.command = command
        self.parameters = parameters
        
        self.message_object = message
        
class Parser(object):

    def __init__(self, config):
        self.config = config

    def parse(self, message):
        cmd, param = message.content.split(" ")[0], message.content.split(" ")[1]
        instruction = Instruction(message, cmd, param)
        return instruction