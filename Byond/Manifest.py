import ..config
import discord
import asyncio
import ast


class Manifest(Command):

    def fill_departments(self, manifest, departments, departmentName, manifestMsg):
        manifestMsg += departmentName
        for name in departments:
            position = departments[name]
            manifestMsg += name + " - " + position + "\r\n"
        return manifestMsg

    @asyncio.coroutine
    def do_command(self):
        try:
            command = "manifest"
            manifest = yield from self.get_server_info(command, self.loop)
            manifest = ast.literal_eval(manifest)
            manifestMsg = "```"
            if manifest == []:
                manifestMsg += "No crew found."
            else:    
                try:
                    manifestMsg = self.fill_departments(manifest, manifest["heads"], "Command:\r\n", manifestMsg)
                    manifestMsg += "\r\n"
                except KeyError:
                    pass
                try:
                    manifestMsg = self.fill_departments(manifest, manifest["sec"], "Security:\r\n", manifestMsg)
                    manifestMsg += "\r\n"
                except KeyError:
                    pass
                try:
                    manifestMsg = self.fill_departments(manifest, manifest["eng"], "Engineering:\r\n", manifestMsg)
                    manifestMsg += "\r\n"
                except KeyError:
                    pass
                try:
                    manifestMsg = self.fill_departments(manifest, manifest["med"], "Medical:\r\n", manifestMsg)
                    manifestMsg += "\r\n"
                except KeyError:
                    pass
                try:
                    manifestMsg = self.fill_departments(manifest, manifest["sci"], "Science:\r\n", manifestMsg)
                    manifestMsg += "\r\n"
                except KeyError:
                    pass
                try:
                    manifestMsg = self.fill_departments(manifest, manifest["car"], "Cargo:\r\n", manifestMsg)
                    manifestMsg += "\r\n"
                except KeyError:
                    pass
                try:
                    manifestMsg = self.fill_departments(manifest, manifest["civ"], "Civilian:\r\n", manifestMsg)
                    manifestMsg += "\r\n"
                except KeyError:
                    pass
                try:
                    manifestMsg = self.fill_departments(manifest, manifest["bots"], "Silicon:\r\n", manifestMsg)
                    manifestMsg += "```"
                except KeyError:
                    pass
                if manifestMsg == "``````":
                    manifestMsg = "No crew found."
            manifestMsg += "```"
            yield from self.client.send_message(self.message.author, manifestMsg)
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")