import xmpp
import json
from xml.dom.minidom import Document
import uuid

class Post():
    def fromXml(self, xml):
        pasr = "asdsa"

    def setContent(self, content):
        self.content = content

    def xml(self):
        doc = Document()
        post = doc.createElement("post")
        doc.appendChild(post)

        id = doc.createElement("uuid")
        idcode = doc.createTextNode( uuid.uuid4().hex)
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
    def connect(self, user, password):
        jid = xmpp.protocol.JID(user)
        self.cl = xmpp.Client(jid.getDomain(),debug=[])
        #debug on
        #self.cl = xmpp.Client(jid.getDomain())
        if not self.cl.connect():
            #fail return
            return False
        self.cl.auth(jid.getNode(),password)
        self.cl.RegisterHandler('presence', self.presenceCB)
        self.cl.sendInitPresence()
    
    def presenceCB(self, conn, msg):
        prs_type = msg.getType()
        who = msg.getFrom()
        if prs_type == "subscribe":
            conn.send(xmpp.Presence(to=who, typ = 'subscribed'))
            conn.send(xmpp.Presence(to=who, typ = 'subscribe'))

    def sendPicPost(self, caption, image, context):
        #form up content then send using normal post method
        post = Post()
        content = ImagePost(caption, image, context)
        post.setContent(content.toStringifiedJSON())
        self.sendToAll(post)

    def sendToAll(self,post):
        roster = self.cl.getRoster()
        print post.xml()
        for r in roster.getItems():
            self.cl.send(xmpp.Message(r,post.xml()))

    def process(self):
        self.cl.Process(1)

class ImagePost():
    def __init__(self, cap, img, con):
        self.caption = cap
        self.image = img
        self.context = con
    def toStringifiedJSON(self):
        jobj = {"cname":"postImage", "caption":self.caption, "image":self.image, "context":self.context}
        return json.dumps(jobj)

