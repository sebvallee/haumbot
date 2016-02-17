import logging
import irc.bot
import re
import settings

import requests
import json

#import praw
#from security import VeganWatchdog
#from reddit import mark_posted, get_submissions


def get_logger():
    return logging.getLogger(__name__)


class MyBot(irc.bot.SingleServerIRCBot):

    def __init__(self, channel, nickname, server, port):
        super().__init__([(server, port)], nickname, nickname)
        self.channel = channel
        #self.rwatchdog = VeganWatchdog(settings.REVERSE_WATCHDOG_TIMEOUT)

    def on_welcome(self, serv, ev):
        get_logger().info("Signed on")
        get_logger().info("Joining {}".format(self.channel))
        serv.join(self.channel)

    def on_join(self, serv, ev):
        get_logger().info("Joined {}".format(self.channel))
        serv.privmsg(self.channel, "DGSI, bonjour !")

    def on_kick(self, serv, ev):
        get_logger().warning("Kicked")
        #self.die('got kicked')
        serv.join(self.channel)
        serv.privmsg(self.channel, "Non, je veux pas ! Je reste !")

    def on_nicknameinuse(self, serv, ev):
        newnick = serv.get_nickname() + '_'
        get_logger().warning("Nick already in use, using {}".format(newnick))
        serv.nick(newnick)

    def on_pubmsg(self, serv, ev):
        self.analyse_msg(serv, ev, "PubMsg")

    def on_privmsg(self, serv, ev):
        self.analyse_msg(serv, ev, "PrivMsg")

    def analyse_msg(self, serv, ev, type):
        nick = ev.source
        nick = nick.split("!")[0]
        if (type == "PrivMsg"):
            dest = nick
        else:
            dest = settings.CHAN
        message = ev.arguments[0].lower()
        args = message.lstrip(message.split()[0])
        get_logger().info("%s from %s : %s" % (type, nick, message))
        if (message.startswith('!')):
            if (message.startswith("!help")):
                get_logger().info("%s demande de l'aide !" % nick)
                
                self.send_help(serv, nick, "")
            if (message.startswith("!agenda")):
                get_logger().info("%s utilise l'agenda !" % nick)
            if (message.startswith("!updatesite")):
                get_logger().info("%s met à jour le site oueb !" % nick)
            if (message.startswith("!spaceapi")):
                get_logger().info("%s change l'état d'ouverture du local !" % nick)
            if (message.startswith("!shrink")):
                get_logger().info("%s utilise le raccourcisseur d'URL !" % nick)
                url = args.split()[0]
                get_logger().info("L'URL a raccourcir est %s" % url)
                self.shrink(serv, url, dest)

    def shrink(self, serv, url, dest):
        r = requests.post("https://huit.re/a", data={'lsturl': url, 'format': 'json'})
        if (r.status_code == "200"):
            get_logger().debug(r.text)
            short = json.loads(r.text)["short"]
            get_logger().debug(short)
            serv.privmsg(dest, short)
        else:
            serv.privmsg(dest, "Probleme de shrink : %s (%s)" % (r.status_code, r.reason))

    def send_help(self, serv, nick, args):
        if (args == ""):
            serv.privmsg(nick, "Ce bot voit tout, sait tout, et fait tout !")
            serv.privmsg(nick, "Il est l'esclave communiquant du HAUM, Hackerspace AU Mans.")
            serv.privmsg(nick, "Plusieurs modules sont disponibles :")
            serv.privmsg(nick, "!help todolist pour les commandes relatives à la to-do list.")
            serv.privmsg(nick, "!help agenda pour les commandes relatives à l'agenda.")
            serv.privmsg(nick, "!help spaceapi pour les commandes de gestion d'ouverture du local (via SpaceApi).")
            serv.privmsg(nick, "!help shrink pour les commandes de raccourcissement d'URL.")
            serv.privmsg(nick, "!help twitter pour les commandes de Twitter")
            serv.privmsg(nick, "!help fb pour les commandes de Facebook")

        if (args == "agenda"):
            serv.privmsg(nick, "!agenda {add_seance|add|remove|modify|all}")
