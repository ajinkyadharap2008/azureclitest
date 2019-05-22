import cherrypy
import cherrypy_cors
from DomainClassification import DomainClassification

@cherrypy.tools.json_out()
@cherrypy.tools.json_in()
class MyResource:

    @cherrypy.expose()
    def trainModel(self):
        obj = DomainClassification()
        response = obj.trainModel()
        return response
    
    @cherrypy.expose()
    def classifyDomain(self):
        input_json = cherrypy.request.json
        transaction_data=input_json['utterance']  
        obj = DomainClassification()
        response = obj.classifyDomain(transaction_data)
        return response
    

    @classmethod
    def run(cls):
        cherrypy_cors.install()
        config = {
            '/': {
                'cors.expose.on': True,
            },
        }
        
        cherrypy.server.socket_host = '127.0.0.1'
        cherrypy.server.socket_port = 5000
        cherrypy.quickstart(cls(), config=config)
        
        
__name__ == '__main__' and MyResource.run()

    