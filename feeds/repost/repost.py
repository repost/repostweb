import xmpp
import json
from xml.dom.minidom import Document
import uuid
import time

class Post():
    def __init__(self):
        self.uuid = str(uuid.uuid4()).upper()

    def fromXml(self, xml):
        pasr = "asdsa"

    def setContent(self, content):
        self.content = content

    def xml(self):
        doc = Document()
        post = doc.createElement("post")
        doc.appendChild(post)

        id = doc.createElement("uuid")
        idcode = doc.createTextNode(self.uuid)
        id.appendChild(idcode)
        post.appendChild(id)
        
        content = doc.createElement("content")
        contentstr = doc.createTextNode(self.content)
        content.appendChild(contentstr)
        post.appendChild(content)

        certs = doc.createElement("certs")
        post.appendChild(certs)

        return doc.toxml()

class Client():
    def __init__(self, user, password):
        self.user = user;
        self.password = password
        self.conTryTime = 0;
        self.isConnected = False

    def connect(self):
        jid = xmpp.protocol.JID(self.user)
        self.cl = xmpp.Client(jid.getDomain(),debug=[])
        #debug on
        #self.cl = xmpp.Client(jid.getDomain())
        if not self.cl.connect():
            #fail return
            return False
        print "CONNECTED"
        self.isConnected = True
        self.cl.auth(jid.getNode(), self.password)
        self.cl.RegisterHandler('presence', self.presenceCB)
        self.cl.RegisterHandler('presence', self.presenceCB)
        self.cl.RegisterDisconnectHandler(self.disconnect)
        self.cl.sendInitPresence()
        return True
    
    def checkConnection(self):
        if not self.isConnected:
            now = time.time()
            if (now - self.conTryTime) > 60:
                print "Attempting reconnect"
                self.conTryTime = time.time()
                return self.connect()
            else:
                return False
        else:
            return True

    def disconnect(self):
        # we have been disconnected. try and come back
        print "Disconnected :'("
        self.isConnected = False
        self.connect()
    
    def presenceCB(self, conn, msg):
        prs_type = msg.getType()
        who = msg.getFrom()
        if prs_type == "subscribe":
            conn.send(xmpp.Presence(to=who, typ = 'subscribed'))
            conn.send(xmpp.Presence(to=who, typ = 'subscribe'))

    def sendPicPost(self, caption, image, context):
        if self.checkConnection(): 
            #form up content then send using normal post method
            post = Post()
            content = ImagePost(caption, image, context)
            post.setContent(content.toStringifiedJSON())
            self.sendToAll(post)
   
    def sendToAll(self,post):
        if self.checkConnection(): 
            roster = self.cl.getRoster()
            print post.xml()
            try:
                for r in roster.getItems():
                    self.cl.send(xmpp.Message(r,post.xml()))
            except IOError, e :
                # Usually have disconnected
                print "Error: not connected usually "
                print e
                self.isConnected = False
    
    def process(self):
        if self.checkConnection(): 
            self.cl.Process(1)

class ImagePost():
    def __init__(self, cap, img, con):
        self.caption = cap
        self.image = img
        self.context = con
    def toStringifiedJSON(self):
        jobj = {"cname":"postImage", "caption":self.caption, "image":self.image, "context":self.context}
        return json.dumps(jobj)

