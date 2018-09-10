#!/usr/bin/env python

import sys
import logging
import getpass
from optparse import OptionParser
import re
from bs4 import BeautifulSoup
import requests
import sleekxmpp

def get_page_title(url):
    sourceCode = requests.get(url).text
    soup = BeautifulSoup(sourceCode, 'html.parser')
    return soup.title.string


class LinkPreviewBot(sleekxmpp.ClientXMPP):

    """
    A simple bot that joins a room and responds to messages including
    a link with the page title of the site.
    """

    def __init__(self, jid, password, room, nick):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.room = room
        self.nick = nick

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        """
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        # If a room password is needed, use:
                                        # password=the_room_password,
                                        wait=True)

    def muc_message(self, msg):
        """
        Process incoming message stanzas from any chat room.

        Whenever someone posts a message containing a URL, the bot
        fetches the page title and posts it.
        """
        if msg['mucnick'] == self.nick:
            return
        url_in_message = re.search("(?P<url>https?://[^\s]+)", msg['body'])
        if url_in_message is not None:
            self.send_message(mto=msg['from'].bare,
                              mbody=get_page_title(url_in_message.group('url')),
                              mtype='groupchat')


if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-r", "--room", dest="room",
                    help="MUC room to join")
    optp.add_option("-n", "--nick", dest="nick",
                    help="MUC nickname")

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None:
        opts.jid = raw_input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")
    if opts.room is None:
        opts.room = raw_input("MUC room: ")
    if opts.nick is None:
        opts.nick = raw_input("MUC nickname: ")

    # Setup the LinkPreviewBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = LinkPreviewBot(opts.jid, opts.password, opts.room, opts.nick)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0045') # Multi-User Chat
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")
