import discord

class Command(object):
    
    def __init__(self, client):
        self.client = client
        
class Ping(Command):
    
    def __init__(self, client):
        self.client = client
    
class Players(Command):
    
    def __init__(self, client):
        self.client = client

class Status(Command):
    
    def __init__(self, client):
        self.client = client

class Manifest(Command):
    
    def __init__(self, client):
        self.client = client

class Revision(Command):
    
    def __init__(self, client):
        self.client = client

class Laws(Command):
    
    def __init__(self, client):
        self.client = client

class Info(Command):
    
    def __init__(self, client):
        self.client = client

class AdminMsg(Command):
    
    def __init__(self, client):
        self.client = client

class Notes(Command):
    
    def __init__(self, client):
        self.client = client

class Age(Command):
    
    def __init__(self, client):
        self.client = client