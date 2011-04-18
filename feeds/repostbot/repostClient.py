import xmpp

class repostClient():
    def connect(self, user, password):
        jid = xmpp.protocol.JID(user)
        self.cl = xmpp.Client(jid.getDomain(),debug=[])
        #debug on
        #self.cl = xmpp.Client(jid.getDomain())
        if not self.cl.connect():
            #fail return
            return False
        self.cl.auth(jid.getNode(),password)
    
    def sendPicPost(self, title, link):
        #form up content then send using normal post method

    def sendPost(self, content):
        #form up post here and send

    def sendToAll(self,msg):
        roster = self.cl.getRoster()
        for r in roster.getItems():
            self.cl.send(xmpp.Message(r,msg))

    def process(self):
        self.cl.Process(1)


