import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
    	a+=1
        return "Hello World!%d" %a

cherrypy.config.update({'server.socket_port': 12358})
cherrypy.config.update({'server.socket_host': '58.199.131.111'})

cherrypy.quickstart(HelloWorld())