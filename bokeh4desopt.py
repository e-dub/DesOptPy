"""
xTODO legend of convergence outside of plot
TODO server
TODO update from new data
TODO faster?
TODO click on graph to get data
TODO change name in browser tabś
"""

from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models.widgets import Panel, Tabs, Div
from bokeh.layouts import row, column, widgetbox, Spacer
from bokeh.models import Label, Legend, LinearAxis, Range1d
from bokeh.util.compiler import TypeScript
#from bokeh.models.ranges import Range1d, LinearAxis
import numpy as np
import pandas as pb
from bokeh.core.enums import LineDash, LineCap, MarkerType, NamedColor
from bokeh.io import curdoc

ManyDesVar = False
Server = True
OptName = "TestOptAlg20191111160524"

if ManyDesVar:
    x = np.array([[0, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2],
                  [0, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2],
                  [0, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2],
                  [0, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2],
                  [1, 2, 3, 4, 5, 6, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2],
                  [0, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2],
                  [0, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2],
                  [0, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2],
                  [0, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2],
                  [0, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2],
                  [0, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2],
                  [0, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2],
                  [2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2]])
else:
    x = np.array([[0, 1, 2, 0, 1],
                  [0, 1, 2, 0, 1],
                  [0, 1, 2, 0, 1],
                  [0, 1, 2, 0, 1],
                  [1, 2, 3, 4, 5],
                  [0, 1, 2, 0, 1],
                  [0, 1, 2, 0, 1],
                  [0, 1, 2, 0, 1],
                  [0, 1, 2, 0, 1],
                  [0, 1, 2, 0, 1],
                  [0, 1, 2, 0, 1],
                  [0, 1, 2, 0, 1],
                  [2, 1, 2, 0, 1]])


xNorm = (np.array(x)/2).tolist()
f = [5, 4, 3, 2, 5, 4, 3, 2, 5, 4, 3, 2, 5]
g = -1*np.array([[2, 1, 2],
                 [0, 1, 2],
                 [0, 1, 2],
                 [0, 1, 2],
                 [0, 1, 2],
                 [0, 1, 2],
                 [0, 1, 2],
                 [0, 1, 2],
                 [0, 1, 2],
                 [0, 1, 2],
                 [0, 1, 2],
                 [0, 1, 2],
                 [0, 1, 2]])


def readHistory():
    import pyOpt
    OptHist = pyOpt.History(Name, "r")
    xAll = OptHist.read([0, -1], ["x"])[0]["x"]
    fAll = OptHist.read([0, -1], ["obj"])[0]["obj"]
    gAll = OptHist.read([0, -1], ["con"])[0]["con"]
    return(xAll, fAll, gAll)
x, f, g = readHistory()
gMax = np.max(g, 1)
it = np.linspace(0, len(x)-1, len(x))
colorList = list(NamedColor)
import fnmatch
RemoveColors = fnmatch.filter(colorList, "*white*")
RemoveGrey = fnmatch.filter(colorList, "*grey*")
RemoveColors = RemoveColors + RemoveGrey + \
               ["azure", "ivory", "aliceblue", "cornsilk", "honeydew",
                "lavenderblush", "lightyellow", "mintcream", "linen",
                "seashell", "snow", "forestgreen", "dodgerblue", "crimson",
                "black", "blanchedalmond", "darkorange", "beige", "gainsboro",
                "yellowgreen"]

for i in RemoveColors:
    colorList.remove(i)
colorObjective = "forestgreen"
colorConstraint = "crimson"
colorList = ["dodgerblue", "darkorange", "yellowgreen"] + colorList
#colorList = ["forestgreen", "crimson", "dodgerblue"] + colorList

wConvPlot = 1500
hConvPlot = 500
wBarPlot = 750
hBarPlot = 500

# Labels for x and g
xLabels = []
xNormLabels = []
for i in range(len(x[0])):
    if i < 9:
        xLabels.append('x{0}'.format(chr(0x2080 + i+1)))
        xNormLabels.append('x̂{0}'.format(chr(0x2080 + i+1)))
    elif i == 9:
        xLabels.append('x{0}'.format(chr(0x2081)) + '{0}'.format(chr(0x2080)))
        xNormLabels.append('x̂{0}'.format(chr(0x2081)) + '{0}'.format(chr(0x2080)))
    elif i < 99 and float(str(i)[1])<9:
        xLabels.append('x{0}'.format(chr(0x2080 + int(str(i)[0]))) +
                      '{0}'.format(chr(0x2080 + int(str(i)[1])+1)))
        xNormLabels.append('x̂{0}'.format(chr(0x2080 + int(str(i)[0]))) +
                      '{0}'.format(chr(0x2080 + int(str(i)[1])+1)))
    elif i < 99 and float(str(i)[1])==9:
        xLabels.append('x{0}'.format(chr(0x2080 + int(str(i)[0])+1)) +
                       '{0}'.format(chr(0x2080)))
        xNormLabels.append('x̂{0}'.format(chr(0x2080 + int(str(i)[0])+1)) +
                       '{0}'.format(chr(0x2080)))
    xLabelLatex = "x_"+str(i+1)
    xNormLabelLatex = "$\hat{x}_"+str(i)+"$",
    #xLabels.append("x_"+str(i+1))
gLabels = []
for i in range(np.size(g, axis=1)):
    if i < 9:
        gLabels.append('g{0}'.format(chr(0x2080 + i+1)))
    elif i == 9:
        gLabels.append('g{0}'.format(chr(0x2081)) + '{0}'.format(chr(0x2080)))
    elif i < 99 and float(str(i)[1])<9:
        gLabels.append('g{0}'.format(chr(0x2080 + int(str(i)[0]))) +
                       '{0}'.format(chr(0x2080 + int(str(i)[1])+1)))

    elif i < 99 and float(str(i)[1])==9:
        gLabels.append('g{0}'.format(chr(0x2080 + int(str(i)[0])+1)) +
                       '{0}'.format(chr(0x2080)))
    gLabelLatex = "g_"+str(i)
fgLabels = ["f"] + gLabels
gMaxLabel = "gₘₐₓ"
gMaxLabelLatex = "g_{max}"
itLabel = "nᵢₜ"
itLabelLatex = "$n_{it}$"
# Plots

# x convergence
xConv = figure(plot_width=wConvPlot, plot_height=hConvPlot)
xConvi = [None]*len(xLabels)
for i in range(len(x[0])):
    xConvi[i] = xConv.line(it, x[:, i], legend_label=xLabels[i], color=colorList[i],
               line_width=2)
    xConv.circle(it, x[:, i], legend_label=xLabels[i], color=colorList[i])
    #xConvi[i] = xConv.line(it, x[:, i], color=colorList[i],
    #           line_width=2)
    #xConv.circle(it, x[:, i], color=colorList[i])
xConv.x_range.start = 0
xConv.x_range.end = max(it)
xConv.xaxis.axis_label = "Iteration " + itLabel
xConv.yaxis.axis_label = "Design variable value x"
#xConv.yaxis.axis_label = "Design variable value $x$"
xConv.xaxis.major_label_orientation = np.pi/2
xConv.yaxis.axis_label_text_font_style = "normal"
xConv.xaxis.axis_label_text_font_style = "normal"
xConv.legend.location = (10, -5)
xConv.right.append(xConv.legend[0])
xConv.legend.border_line_color = None


# x norm convergence
xNormConv = figure(plot_width=wConvPlot, plot_height=hConvPlot)
for i in range(len(x[0])):
    #xNormConv.line(it, x[:, i], legend_label=LatexLabel(text="$\hat{x}_"+str(i)+"$"),
    #               color=colorList[i])
    xNormConv.line(it, x[:, i], legend_label=xNormLabels[i],
                   color=colorList[i], line_width=2)
    xNormConv.circle(it, x[:, i], legend_label=xNormLabels[i],
                     color=colorList[i])
    #xNormConvi[i] = xNormConv.line(it, x[:, i], color=colorList[i],
    #                               line_width=2)
    #xNormConv.circle(it, x[:, i], color=colorList[i])
xNormConv.x_range.start = 0
xNormConv.x_range.end = max(it)
xNormConv.xaxis.axis_label = "Iteration " + itLabel
xNormConv.yaxis.axis_label = "Normalized design variable value x̂"
#xNormConv.yaxis.axis_label = "Normalized design variable value $\hat{x}$"
xNormConv.xaxis.major_label_orientation = np.pi/2
xNormConv.yaxis.axis_label_text_font_style = "normal"
xNormConv.xaxis.axis_label_text_font_style = "normal"
xNormConv.legend.location = (10, -5)
xNormConv.right.append(xNormConv.legend[0])
xNormConv.legend.border_line_color = None


fgMaxConv = figure(plot_width=wConvPlot, plot_height=hConvPlot)
fgMaxConv.line(it, f, legend_label="f", color=colorObjective, line_width=2)
fgMaxConv.circle(it, f, legend_label="f", color=colorObjective)
fgMaxConv.x_range.start = 0
fgMaxConv.x_range.end = max(it)
fgMaxConv.yaxis.axis_label = "Objective value f"
#fgMaxConv.yaxis.axis_label = "Objective value $f$"
fgMaxConv.xaxis.axis_label = "Iteration " + itLabel
fgMaxConv.xaxis.major_label_orientation = np.pi/2
fgMaxConv.yaxis.axis_label_text_font_style = "normal"
fgMaxConv.xaxis.axis_label_text_font_style = "normal"
fgMaxConv.y_range = Range1d(min(f), max(f))
fgMaxConv.yaxis.axis_label_text_color = color=colorObjective
gMaxMin = float(np.min(gMax))
gMaxMax = float(np.max(gMax))
fgMaxConv.extra_y_ranges = {"gMax": Range1d(start=np.min(gMax),
                                            end=np.max(max(np.max(g), 0)))}
#gMaxAxis = LinearAxis(axis_label="Maximum constraint value $g_{max}$",
gMaxAxis = LinearAxis(axis_label="Maximum constraint value "+gMaxLabel,
                      y_range_name="gMax",
                      axis_label_text_font_style="normal",
                      axis_label_text_color=colorConstraint,
                      major_label_orientation="vertical")
fgMaxConv.add_layout(gMaxAxis, 'right')

fgMaxConv.line(it, gMax, legend_label=gMaxLabel, y_range_name="gMax",
               color=colorConstraint, line_width=2)
fgMaxConv.circle(it, gMax, legend_label=gMaxLabel, y_range_name="gMax",
                 color=colorConstraint)
fgMaxConv.legend.location = (10, -5)
fgMaxConv.right.append(fgMaxConv.legend[0])
fgMaxConv.legend.border_line_color = None

# Constraint convergence plot
gConv = figure(plot_width=wConvPlot, plot_height=hConvPlot)
for i in range(len(g[0])):
    gConv.line(it, g[:, i], legend_label=gLabels[i], color=colorList[i],
               line_width=2)
    gConv.circle(it, g[:, i], legend_label=gLabels[i], color=colorList[i])
gConv.x_range.start = 0
gConv.x_range.end = max(it)
gConv.y_range.end = max(np.max(g), 0)
gConv.yaxis.axis_label = "Constraint value g"
#gConv.yaxis.axis_label = "Constraint value $g$"
gConv.xaxis.axis_label = "Iteration " + itLabel
gConv.xaxis.major_label_orientation = np.pi/2
gConv.yaxis.axis_label_text_font_style = "normal"
gConv.xaxis.axis_label_text_font_style = "normal"
gConv.legend.location = (10, -5)
gConv.right.append(gConv.legend[0])
gConv.legend.border_line_color = None

# Bar diagrams

# Bar diagram of current design
xBar = figure(x_range=xLabels, plot_width=wBarPlot, plot_height=hBarPlot)
xBar.y_range.start = 0
xBar.vbar(top=x[-1], x=xLabels, width=0.75, color="dodgerblue")
xBar.yaxis.axis_label = "Design variable value x"
#xBar.yaxis.axis_label = "Design variable value $x$"
xBar.xaxis.major_label_orientation = np.pi/2
xBar.yaxis.axis_label_text_font_style = "normal"

# Bar diagram of objective functions
fg = np.zeros((np.size(g, axis=1)+1,))
fg[0] = f[-1]
fg[1:] = g[-1, :]
fgBar = figure(x_range=fgLabels, plot_width=wBarPlot, plot_height=hBarPlot)
fgBar.vbar(top=f[-1], x=["f"], width=0.75, color=colorObjective)
fgBar.vbar(top=g[-1], x=gLabels, width=0.75, color=colorConstraint)
fgBar.yaxis.axis_label = "Objective and constrint value f, "+gMaxLabel
#fgBar.yaxis.axis_label = "Objective and constrint value $f$, $g$"
fgBar.yaxis.axis_label_text_font_style = "normal"
fgBar.xaxis.major_label_orientation = np.pi/2
#gBarAxis = LinearAxis(axis_label="Constraint value $g$",
#                      y_range_name="gBar",
#                      axis_label_text_font_style="normal",
#                      axis_label_text_color=colorList[1],
#                      major_label_orientation="vertical")

#fgBar.extra_y_ranges = {"gBar": Range1d(start=np.min(g[-1]),
#                                        end=np.max(g[-1]))}
#gBarAxis = LinearAxis(axis_label="Constraint value $g$",
#                      y_range_name="gBar",
#                      axis_label_text_font_style="normal",
#                      axis_label_text_color="red",
#                      major_label_orientation="vertical")
#fgBar.add_layout(gBarAxis, 'right')
#fgBar.vbar(top=g[-1, :], x=gLabels,  width=0.75, y_range_name="gBar",
#           color=colorList[1])


# Layout of sheet
title = Div(text='<h1 style="text-align: center">Design optimization monitoring</h1>')
headerConvPlot = Div(text='<h2 style="text-align: center">Convergence plots</h2>')
headerBarPlot = Div(text='<h2 style="text-align: center">Current design</h2>')
tab1 = Panel(child=xConv, title="Design variable values")
tab2 = Panel(child=xNormConv, title="Normalized design variable values")
tab3 = Panel(child=fgMaxConv, title="Objective and maximum constraint values")
tab4 = Panel(child=gConv, title="Constraint values")
layout = column(title,
                row(column(headerConvPlot,
                           Tabs(tabs=[tab1, tab2, tab3, tab4]),
                           Spacer(height=0),
                           headerBarPlot,
                           row(xBar, Spacer(width=50), fgBar)),
                   Spacer(width=25),
                   column(Spacer(height=25),
                          Div(text="Design optimization model"),
                          Div(text="Design optimization"))))
ExportHTML = False
if ExportHTML:
    output_file("opt.html")
if Server:
    #update()
    curdoc().add_root(layout)
    curdoc().title = OptName
show(layout)