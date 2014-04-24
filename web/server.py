import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import subprocess, json

PORT = 8080

class WSHandler(tornado.websocket.WebSocketHandler):
#    def __init__(self):
#        self.proc = None

    def spawn(self, program):
        return subprocess.Popen(program,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)
    
    def open(self):
        print 'new connection'
        #self.write_message("Hello World")
      
    def on_message(self, message):
        print 'message received %s' % message
        msg = json.loads(message)
        if msg['cmd'] == "launch":
            self.proc = self.spawn("./learntris")
            self.send("launched")
        elif msg['cmd'] == "sendCommand":
            if self.proc is None: self.fail()
            print "writing command:", msg['command']
            self.proc.stdin.write(msg['command'] + '\n')
            self.proc.stdin.flush()
        elif msg['cmd'] == "readLines":
            if self.proc is None: self.fail()
            print "reading %d lines" % msg['lines']
            output = ""
            for i in range(msg['lines']):
                print "reading line", i
                output += self.proc.stdout.readline() + '\n'
            print "output:", output
            self.send("output", output=output)

    def fail(self):
        raise Exception()

    def send(self, cmd, **kwargs):
        self.write_message(json.dumps(dict(cmd=cmd, **kwargs)))
 
    def on_close(self):
        print 'connection closed'

class HTTPHandler(tornado.web.RequestHandler):
    def get(self):
        #self.write("Hi")
        self.write("""
            <body></body>
            <script>
                var ws = new WebSocket("ws://%s/ws");

                function send(obj) {
                    ws.send(JSON.stringify(obj));
                }

                function sendCommand(cmd) {
                    send({cmd:'sendCommand', command:cmd});
                }

                var outqueue = [];
                function readLines(lines, callback) {
                    send({cmd:'readLines', lines:lines});
                    outqueue.push(callback);
                }

                ws.onopen = function() {
                    //ws.send("Hello, world!");
                    send({'cmd':'launch'});
                };

                ws.onmessage = function (evt) {
                    //alert(evt.data);
                    console.log("msg: " + evt.data);
                    var msg = JSON.parse(evt.data);
                    switch(msg.cmd) {
                        case 'launched':
                            console.log('launched');
                            sendCommand('p');
                            readLines(22, function(output) {
                                console.log("output: " + output);
                                sendCommand('q');
                            });
                        break;

                        case 'output':
                            if(outqueue.length === 0) throw new Exception("queue underrun");
                            console.log('output: ' + msg.output);
                            outqueue.unshift()(msg.output);
                        break;

                        default:
                            throw new Exception("Unhandled command: " + msg.cmd);
                    }
                    };
            </script>""" % "lpmc.p.sabren.com:8080")

application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/', HTTPHandler)
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    print "Listening on port", PORT
    http_server.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
