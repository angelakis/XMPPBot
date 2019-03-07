XMPP Link Preview Bot
=====================
A link preview bot for jabber multi-user chatrooms

The bot extracts the URL from any message posted and posts the page title.

USAGE
-----
Use pip to install requirements.txt.

```bash
Usage: muc.py [options]

Options:
  -h, --help            show this help message and exit
  -q, --quiet           set logging to ERROR
  -d, --debug           set logging to DEBUG
  -v, --verbose         set logging to COMM
  -j JID, --jid=JID     JID to use
  -p PASSWORD, --password=PASSWORD
                        password to use
  -r ROOM, --room=ROOM  MUC room to join
  -n NICK, --nick=NICK  MUC nickname
```

USING DOCKER
------------
To run with docker issue the following commands:
```bash
# docker build -t xmpp-bot .
# docker run -it xmpp-bot
```

LICENSE
-------

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Affero General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.
