
## this is write by qingluan 
# just a inti handler 
# and a tempalte offer to coder
import json
import tornado
import tornado.web
from tornado.websocket import WebSocketHandler
from tornado.curl_httpclient import AsyncHTTPClient
from base64 import b64encode, b64decode
from chardet import detect

class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.db = self.settings['db']
        self.L = self.settings['L']
        self.de = self.settings['de_and_en']
        self.pack = self.settings['pack']
        self.unpack = self.settings['unpack']

    def get_current_user(self):
        return (self.get_cookie('user'),self.get_cookie('passwd'))
    def get_current_secure_user(self):
        return (self.get_cookie('user'),self.get_secure_cookie('passwd'))
    def set_current_seccure_user_cookie(self,user,passwd):
        self.set_cookie('user',user)
        self.set_secure_cookie("passwd",passwd)


class SocketHandler(WebSocketHandler):
    """ Web socket """
    clients = set()
    con = dict()
         
    @staticmethod
    def send_to_all(msg):
        for con in SocketHandler.clients:
            con.write_message(json.dumps(msg))
         
    @staticmethod
    def send_to_one(msg, id):
        SocketHandler.con[id(self)].write_message(msg)

    def json_reply(self, msg):
        self.write_message(json.dumps(msg))

    def open(self):
        SocketHandler.clients.add(self)
        SocketHandler.con[id(self)] = self
         
    def on_close(self):
        SocketHandler.clients.remove(self)
         
    def on_message(self, msg):
        SocketHandler.send_to_all(msg)





class IndexHandler(BaseHandler):
    
    def prepare(self):
        super(IndexHandler, self).prepare()
        self.template = "template/index.html"

    def get(self):
        # L is log function , which include ok , info , err , fail, wrn
        self.L.ok('got')
        return self.render(self.template, post_page="/")

    @tornado.web.asynchronous
    def post(self):
        # you should get some argument from follow 
        post_args = self.get_argument("some_argument")
        # .....
        # for parse json post
        # post_args = json.loads(self.request.body.decode("utf8", "ignore"))['msg']
        
        # redirect or reply some content
        # self.redirect()  
        self.write("hello world")
        self.finish()
    


class RelayHandler(BaseHandler):
    
    def prepare(self):
        super(RelayHandler, self).prepare()
        self.template = "template/relay.html"

    def get(self):
        # L is log function , which include ok , info , err , fail, wrn
        self.L.ok('got')
        return self.render(self.template, post_page="/relay")

    def async_get(self, url):
        client = AsyncHTTPClient()
        print('to connect ...',url)
        client.fetch(url, self.handle_async_reponse)

    @tornado.web.asynchronous
    def reply(self, con, **kargs):
        
        m = self.pack(con)
        # print(m)
        kargs['body'] = m.decode("utf8")
        data = json.dumps(kargs)
        self.write(data)
        self.finish()

    @tornado.web.asynchronous
    def handle_async_reponse(self, resp):
        if resp.error:
            print("Error: %s" % resp.error)
            self.reply(b'error')
        else:
            if len(resp.body) > 2000:
                charset = detect(resp.body[:2000])
            else:
                charset = detect(resp.body)

            self.reply(resp.body, charset=charset)


    @tornado.web.asynchronous
    def post(self):
        # you should get some argument from follow 
        url = bytes(self.de(self.get_argument("url").encode('utf8'))).decode("utf8")
        
        print(url)
        self.async_get(url)
        # .....
        # for parse json post
        # post_args = json.loads(self.request.body.decode("utf8", "ignore"))['msg']
        
        # redirect or reply some content
        # self.redirect()
        # self.write("got task")
        # self.finish()
    
