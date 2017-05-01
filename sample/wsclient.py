from socketIO_client import SocketIO, BaseNamespace

#import logging
#logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
#logging.basicConfig()

class CommandNamespace(BaseNamespace):

    def on_drive(self, *args):
        print('on_aaa_response', args)

    def on_connect(self):
        print('[connect]')

    def on_disconnect(self):
        print('[disconnect]')

    def on_reconnect(self):
        print('[reconnect]')


socketIO = SocketIO('localhost', 5000)
cmd_namespace = socketIO.define(CommandNamespace, '/commands')
socketIO.wait()
