from . import config
import discord
import asyncio
import urllib.parse

class Info(Command):

    def parse_damage(self, damage):
        dam = urllib.parse.parse_qs(damage)
        if dam == {}:
            damtup = ("Not living", "Not living", "Not living", "Not living", "Not living", "Not living")
        else:
            damtup = (dam["oxy"][0], dam["tox"][0], dam["fire"][0], dam["brute"][0], dam["clone"][0], dam["brain"][0])
        return damtup

    @asyncio.coroutine
    def do_command(self):
        try:
            commandtup = get_command(self.message)
            command = "?info=" + commandtup[1]
            command += ";key=" + config.commskey
            info = yield from self.get_server_info(command, self.loop)
            if info == "No matches":
                yield from self.client.send_message(self.message.channel, "No matches.")
            else:
                info = urllib.parse.parse_qs(info)
                area = info["area"][0]
                info["area"][0] = area.replace("%ff", "")
                infoMsg = "```"
                infoMsg += "Key:           " + info["key"][0] + "\r\n"
                infoMsg += "Name:          " + info["name"][0] + "\r\n"
                infoMsg += "Species:       " + info["species"][0] + "\r\n"
                infoMsg += "Gender:        " + info["gender"][0] + "\r\n"
                infoMsg += "Role:          " + info["role"][0] + "\r\n"
                infoMsg += "Location:      " + info["loc"][0] + "\r\n"
                infoMsg += "Turf:          " + info["turf"][0] + "\r\n"
                infoMsg += "Area:          " + info["area"][0] + "\r\n"
                infoMsg += "Antag:         " + info["antag"][0] + "\r\n"
                infoMsg += "Has been rev?: "  
                if int(info["hasbeenrev"][0]):
                    infoMsg += "Yes" + "\r\n"
                else:
                    infoMsg += "No" + "\r\n"
                infoMsg += "Mob type:      " + info["type"][0] + "\r\n"
                damages = self.parse_damage(info["damage"][0])
                infoMsg += "Damage:        " + "\r\n"
                infoMsg += "--Oxy:   " + damages[0] + "\r\n"
                infoMsg += "--Tox:   " + damages[1] + "\r\n"
                infoMsg += "--Fire:  " + damages[2] + "\r\n"
                infoMsg += "--Brute: " + damages[3] + "\r\n"
                infoMsg += "--Clone: " + damages[4] + "\r\n"
                infoMsg += "--Brain: " + damages[5]
                infoMsg += "```"
                yield from self.client.send_message(self.message.channel, infoMsg)
        except OSError:
            yield from self.client.send_message(self.message.channel, "Server is offline.")