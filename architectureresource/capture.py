"""
Since there is valuable information in the caffe log output that can't be captured in the 
python objects, this function decorator is designed to capture stdout.
This can then be parsed like a log file and analyzed accordingly.
"""

from cStringIO import StringIO
import sys
import os
import threading
import time


class Capturing(threading.Thread):
    def __enter__(self):
        self.goflag=True
        self.output=""
        self.err=""
        self.stdout_fileno = sys.stdout.fileno()
        self.stdout_save = os.dup(self.stdout_fileno)
        self.stdout_pipe = os.pipe()
        os.dup2(self.stdout_pipe[1], self.stdout_fileno)
        os.close(self.stdout_pipe[1])

        self.stderr_fileno = sys.stderr.fileno()
        self.stderr_save = os.dup(self.stderr_fileno)
        self.stderr_pipe = os.pipe()
        os.dup2(self.stderr_pipe[1], self.stderr_fileno)
        os.close(self.stderr_pipe[1])

        self.start()
        return self
        
    def run(self):
        while self.goflag:
            data = os.read(self.stdout_pipe[0], 1024)
            if not data:
                break
            self.output+=data
            data = os.read(self.stderr_pipe[0], 1024)
            if not data:
                break
            self.err+=data

    def __exit__(self, *args):
        self.goflag=False
        os.close(self.stdout_fileno)
        os.close(self.stderr_fileno)


        os.close(self.stdout_pipe[0])
        os.dup2(self.stdout_save, self.stdout_fileno)
        os.close(self.stdout_save)
        os.close(self.stderr_pipe[0])
        os.dup2(self.stderr_save, self.stderr_fileno)
        os.close(self.stderr_save)
        self.join()
        print "Finished Capture"


class OutputGrabber(object):
    """
    Class used to grab standard output or another stream.
    """
    escape_char = "\b"

    def __init__(self, stream=None, threaded=False):
        self.origstream = stream
        self.threaded = threaded
        if self.origstream is None:
            self.origstream = sys.stdout
        self.origstreamfd = self.origstream.fileno()
        self.capturedtext = ""
        # Create a pipe so the stream can be captured:
        self.pipe_out, self.pipe_in = os.pipe()
        self.goflag=True
        pass

    def start(self):
        """
        Start capturing the stream data.
        """
        self.capturedtext = ""
        # Save a copy of the stream:
        self.streamfd = os.dup(self.origstreamfd)
        # Replace the Original stream with our write pipe
        os.dup2(self.pipe_in, self.origstreamfd)
        if self.threaded:
            # Start thread that will read the stream:
            self.workerThread = threading.Thread(target=self.readOutput)
            self.workerThread.start()
            # Make sure that the thread is running and os.read is executed:
            time.sleep(0.01)
        pass

    def stop(self):
        """
        Stop capturing the stream data and save the text in `capturedtext`.
        """
        #
        # Flush the stream to make sure all our data goes in before
        # the escape character.
        self.goflag=False
        self.origstream.flush()
        # Print the escape character to make the readOutput method stop:
        self.origstream.write(self.escape_char)
        self.goflag=False
        if self.threaded:
            # wait until the thread finishes so we are sure that
            # we have until the last character:
            self.workerThread.join()
        else:
            self.readOutput()
        # Close the pipe:
        os.close(self.pipe_out)
        # Restore the original stream:
        os.dup2(self.streamfd, self.origstreamfd)
        pass

    def readOutput(self):
        """
        Read the stream data (one byte at a time)
        and save the text in `capturedtext`.
        """
        while self.goflag:
            data = os.read(self.pipe_out, 1)  # Read One Byte Only
            if self.escape_char in data:
                break
            if not data:
                break
            self.capturedtext += data
        pass
