from functools import partial
from random import random
from threading import Thread
import time
from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure
from tornado import gen
import os
import numpy as np
# this must only be modified from a Bokeh session callback
source = ColumnDataSource(data=dict(x=[0], y=[0]))

# This is important! Save curdoc() to make sure all threads
# see the same document.
doc = curdoc()

Name = os.getcwd()+os.sep+os.getcwd().split(os.sep)[-1][6:]

def readHistory():
    import pyOpt
    OptHist = pyOpt.History(Name, "r")
    xAll = OptHist.read([0, -1], ["x"])[0]["x"]
    fAll = OptHist.read([0, -1], ["obj"])[0]["obj"]
    gAll = OptHist.read([0, -1], ["con"])[0]["con"]
    return(xAll, fAll, gAll)


@gen.coroutine
def update(x, y):
    source.stream(dict(x=[x], y=[y]))

def blocking_task():
    while True:
        # do some blocking computation
        time.sleep(0.1)

        #read in from opt files!!!
        xAll, fAll, gAll = readHistory()

        # but update the document from callback
        doc.add_next_tick_callback(partial(update, x=fAll, y=np.linspace(0,len(fAll), len(fAll)+1)))
        print(fAll)
        print(len(fAll)+1)

p = figure(x_range=[0, 10], y_range=[0,10000])
l = p.circle(x='x', y='y', source=source)
doc.add_root(p)
thread = Thread(target=blocking_task)
thread.start()


