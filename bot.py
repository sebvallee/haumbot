import logging

import irc.bot
#import praw

import re

import settings
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
        #self.connection.execute_every(
        #    settings.POLL_REDDIT_EVERY, self._check_submissions, (serv,))
        #self._check_submissions(serv)

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
        self.analyse_msg(serv, nick, message, "PrivMsg")

    def analyse_msg(self, serv, ev, type):
        nick = ev.source
        nick = nick.split("!")[0]
        message = ev.arguments[0].lower()
        get_logger().info("%s from %s : %s" % (type, nick, message))
        if (message.startsWith("!help")):
            get_logger().info("%s demande de l'aide !" % nick)
            self.send_help(serv, nick, "")
        if (message.startsWith("!agenda"))

    def send_help(self, serv, nick, command):
        if (command == ""):
            serv.privmsg(nick, "Ce bot voit tout, sait tout, et fait tout !")
            serv.privmsg(nick, "Il est l'esclave communiquant du HAUM, Hackerspace AU Mans.")
            serv.privmsg(nick, "Plusieurs modules sont disponibles :")
            serv.privmsg(nick, "!help todolist pour les commandes relatives à la to-do list.")
            serv.privmsg(nick, "!help agenda pour les commandes relatives à l'agenda.")
            serv.privmsg(nick, "!help spaceapi pour les commandes de gestion d'ouverture du local (via SpaceApi).")
            serv.privmsg(nick, "@cmd pour les commandes de réseaux sociaux (Twitter et Facebook)")
        if (command == "agenda"):
            serv.privmsg(nick, "!agenda {add_seance|add|remove|modify|all}")
