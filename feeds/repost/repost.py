import xmpp
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

        print doc.toxml()
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
    
    def sendPicPost(self, title, link):
        #form up content then send using normal post method
        t = title
        post = Post()
        post.setContent("sadasd")
        print post.xml()

    def sendPost(self, content):
        #form up post here and send
        c = content

    def sendToAll(self,msg):
        roster = self.cl.getRoster()
        for r in roster.getItems():
            self.cl.send(xmpp.Message(r,msg))

    def process(self):
        self.cl.Process(1)


