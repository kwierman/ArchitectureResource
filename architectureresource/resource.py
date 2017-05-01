from networks import network_list
from capture import Capturing, OutputGrabber
import os, sys
import time
import commands
import subprocess
import numpy as np
import scipy
from scipy import stats
from datetime import datetime, timedelta
import xlsxwriter
#import caffe
#caffe.set_device(1)
#caffe.set_mode_gpu()

def getdatetime(line):
  token = line.split()[1]
  return datetime.strptime(token, '%H:%M:%S.%f')

def getdatetimeforitem(lines, item):
  return [getdatetime(line) for line in lines if item in line]
  

def analyze_batch_size(network, attribs, batch_size):
  input_network = open(os.path.join(attribs['folder'], attribs['test']), 'r').readlines()
  output_network = open('tmp.prototxt','w')

  for line in input_network:
    if "batch_size" in line and not '#' in line:
      line = "    batch_size: "+str(batch_size)+"\n"
    if "filler_config:" in line and not '#' in line:
      line = '    filler_config: "/data/shared/ArchitectureStudyInference/testA.cfg"\n'
    output_network.write(line)
  output_network.close()

  try:
    """
    My God, this is the DUMBEST THING I HAVE EVER DONE. Seriously
    """
    old = time.time()
    output = subprocess.check_output(['/home/kwierman/proj/src/caffe/build/tools/caffe', 'test', 
                                    '--weights={}'.format(os.path.join(attribs['folder'], attribs['snapshot'])),
                                    '--model=tmp.prototxt',
                                    '--iterations=1',
                                    #'--gpu=3',
                                    ],stderr=subprocess.STDOUT)
    new = time.time()
    return output, new-old
  except Exception as e:
    return "",0
  return output,0

"""
  #output = OutputGrabber(threaded=True)
  #output.start()
  #err = OutputGrabber(stream=sys.stderr, threaded=True)
  #err.start()
  with Capturing() as output:
    print "Hello World"
    net = caffe.Net('tmp.prototxt',
                  os.path.join(attribs['folder'], attribs['snapshot']),
                  caffe.TEST)
    #net.forward()
    time.sleep(1)
  #output.stop()
  #err.stop()
  return output.output+output.err
  #return output.capturedtext+err.capturedtext
"""

_table_file = open("data/stage0.csv","w")
_table_file.write("network,batch_size,memory,exec_time,blob_resize_time,blob_fill_time,load_time,finished_time\n")

def analyze_network(network, attribs):
  global _table_file
  print "Analyzing: ", network
  images=[]
  memory=[]
  times=[]
  blob_resize = []
  blob_fill = []
  load_time = []
  finished_time= []
  for batch_size in range(1,7):
    print "Checking Batch Size: ", batch_size
    log, t_exec = analyze_batch_size(network, attribs, batch_size)
    output = open('logs/'+network+".log",'w')
    output.write(str(log))
    memory_required = 0

    for line in log.split("\n"):
      if "Memory required for data:" in line:
        memory_required = int(line.split()[-1])
    if memory_required>0:
      print memory_required
      images.append(batch_size)
      memory.append(memory_required)
      times.append(t_exec)
      lines = log.split('\n')
      begin = getdatetimeforitem(lines, "Start LoadROOTFileData")[0]
      blob_resize.append((getdatetimeforitem(lines, "Resizing blob")[0]-begin).total_seconds())
      blob_fill.append((getdatetimeforitem(lines, "Filling empty blob")[0]-begin).total_seconds())
      load_time.append((getdatetimeforitem(lines, "Calling root_load_data")[0]-begin).total_seconds())
      finished_time.append((getdatetimeforitem(lines, "Finished LoadROOTFileData")[0]-begin).total_seconds())
    else:
      print log
  print memory



  _table_file.write("{},{},{},{},{},{},{},{},{}\n".format(network, 
                                              stats.linregress(images, memory)[0],
                                              stats.linregress(images, memory)[1],
                                              stats.linregress(images, times)[0],
                                              stats.linregress(images, times)[1],
                                              stats.linregress(images, blob_resize)[1],
                                                          stats.linregress(images, blob_fill)[1],
                                                          stats.linregress(images,load_time)[1],
                                                          stats.linregress(images, finished_time)[1],
                                      ))
  print network


if __name__ == "__main__":
  print "starting"
  for network in network_list:
    analyze_network(network, network_list[network])
