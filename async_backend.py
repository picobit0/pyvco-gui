from subprocess import Popen, PIPE
from queue import Queue
from threading import Thread

class AsyncBackend ():
    def __init__ (self, cmd):
        self.cmd = cmd
        self.stopped = False
        self._process = None
        self._outQueue = Queue()

    def start (self):
        self._process = Popen(self.cmd, stdin=PIPE, stdout=PIPE, shell=True)
        self._readThread = Thread(target=self.reader)
        self._readThread.start()

    def stop (self):
        stopped = True
        self._process.kill()
        
    def __enter__ (self):
        self.start()

    def __exit__ (self, *_):
        self.stop()

    def __bool__ (self):
        return not self.stopped

    def reader (self):
        while True:
            line = self._process.stdout.read(1)
            if not line: break
            self._outQueue.put(line)
        self.stopped = True

    def try_get (self):
        if self._outQueue.empty(): return None
        line = b""
        while not self._outQueue.empty():            
            line += self._outQueue.get()
        try:
            line = line.decode()
        except UnicodeDecodeError:
            line = line.decode("866")
        return line

    def send (self, line):
        self._process.stdin.write(line.encode())
        self._process.stdin.flush()
