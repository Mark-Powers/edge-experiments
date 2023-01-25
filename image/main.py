import power_meter

# Time between keep alive messages, device will stop streaming if no KEEP_ALIVE
# message is received within 2000ms
KEEP_ALIVE_INTERVAL_S = 0.5

import datetime
import logging
import threading
import time

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class MeasuringThread(threading.Thread):
    def __init__(self, log):
        threading.Thread.__init__(self)
        self.daemon = True
        self.signal = True
        self.log = log
        self.name = "measurement"
        
        '''
        device = "/dev/ttyUSB0"
        self.log4usb=power_meter.Log4Device()
        if device:
            print("found device, starting streaming stuff")
            device.flushInput()
            log4usb.setStreaming(device, True)
            last_keep_alive_time = datetime.datetime.now()
        '''
        
    def run(self):
        while self.signal:
            '''
            now = datetime.datetime.now()
            if (now - last_keep_alive_time).seconds > KEEP_ALIVE_INTERVAL_S:
                last_keep_alive_time = now
                log4usb.keepAlive(device)
            log4usb.measure(device)
            if log4usb.device == "Log4 USB":
                pretty_timestamp = datetime.datetime.fromtimestamp(log4usb.timestamp).strftime("%Y-%m-%d %H:%M:%S.%f")
                print(log4usb)
            '''
            # Just logging fake data while testing
            time.sleep(10)
            self.log.info("%s,%s,%s,%f,%f,%f", self.name, time.time(), "power_measurement", 0, 0, 0)
            
            
class RPCServerThread(threading.Thread):
    def __init__(self, log):
        threading.Thread.__init__(self)
        self.daemon = True
        self.signal = True
        self.log = log
        self.name = "event"
        
    def run(self):
        class MyXMLRPCServer(SimpleXMLRPCServer):                
            def serve_forever(self):
                self.quit = False
                while not self.quit:
                    self.handle_request()
            
            def quit(self):
                self.quit = True

        with MyXMLRPCServer(
            ('localhost', 8000),
            requestHandler=SimpleXMLRPCRequestHandler,
            allow_none=True,
        ) as server:
            server.register_introspection_functions()

            def log(name, *args):
                self.log.info("%s,%s,%s,%s,%s", self.name, time.time(), "event", name, ",".join(args))
            server.register_function(log, "log")
            server.serve_forever()
            
            # This doesn't really work
            while self.signal:
                pass
            server.quit()
    
if __name__ == '__main__':
    logging.basicConfig(filename='out.log', encoding='utf-8', level=logging.DEBUG)
    log = logging.getLogger()

    # Create and start measuring thread, and rpc thread to mark events
    mt = MeasuringThread(log)
    rt = RPCServerThread(log)
    mt.start()
    rt.start()
    
    # TODO run experiment here
    time.sleep(100)
    
    
    # Signal to threads to shut down
    mt.signal = False
    rt.signal = False
