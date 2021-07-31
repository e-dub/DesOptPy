"""
xTODO legend of convergence outside of plot
xTODO server
TODO update from new data
xTODO faster?
xTODO click on graph to get data
xTODO change name in browser tabś
TODO data table
https://docs.bokeh.org/en/0.10.0/docs/user_guide/interaction.html#data-table
TODO differentiate between iteration and evaluation!!!
TODO add iteration and evaluation plots???
TODO use ColumnDataSource and streaming?
https://docs.bokeh.org/en/latest/docs/reference/models/sources.html?highlight=columndatasource#bokeh.models.sources.ColumnDataSource
"""

from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models.widgets import Panel, Tabs, Div
from bokeh.layouts import row, column, widgetbox, Spacer
from bokeh.models import Label, Legend, LinearAxis, Range1d, HoverTool
from bokeh.util.compiler import TypeScript

# from bokeh.models.ranges import Range1d, LinearAxis
import numpy as np
import pandas as pb
from bokeh.core.enums import LineDash, LineCap, MarkerType, NamedColor
from bokeh.io import curdoc
from bokeh.client import push_session
import os


# session = push_session(curdoc())
OptName = os.getcwd().split(os.sep)[-1][6:]
RunLoc = os.getcwd() + os.sep + OptName
# ManyDesVar = False
Server = 0
# OptName = "TestOptAlg20191111160524"
OptAlg = "NLPQLP"
wConvPlot = 1000
hConvPlot = 300
wBarPlot = 400
hBarPlot = 200
LineWidth = 1


def readHistory():
    import pyOpt

    OptHist = pyOpt.History(RunLoc, "r")
    xAll = OptHist.read([0, -1], ["x"])[0]["x"]
    fAll = OptHist.read([0, -1], ["obj"])[0]["obj"]
    gAll = OptHist.read([0, -1], ["con"])[0]["con"]
    xAll = np.array(xAll)
    fAll = np.array(fAll)[:, 0]
    gAll = -np.array(gAll)
    xNorm = (np.array(xAll) / 2).tolist()
    gMax = np.max(gAll, 1)
    return (xAll, xNorm, fAll, gAll, gMax)


x, xNorm, f, g, gMax = readHistory()


it = np.linspace(0, len(x) - 1, len(x))
colorList = list(NamedColor)
import fnmatch

RemoveColors = fnmatch.filter(colorList, "*white*")
RemoveGrey = fnmatch.filter(colorList, "*grey*")
RemoveColors = (
    RemoveColors
    + RemoveGrey
    + [
        "azure",
        "ivory",
        "aliceblue",
        "cornsilk",
        "honeydew",
        "lavenderblush",
        "lightyellow",
        "mintcream",
        "linen",
        "seashell",
        "snow",
        "forestgreen",
        "dodgerblue",
        "crimson",
        "black",
        "blanchedalmond",
        "darkorange",
        "beige",
        "gainsboro",
        "yellowgreen",
    ]
)

for i in RemoveColors:
    colorList.remove(i)
colorObjective = "forestgreen"
colorConstraint = "crimson"
colorList = ["dodgerblue", "darkorange", "yellowgreen"] + colorList
# colorList = ["forestgreen", "crimson", "dodgerblue"] + colorList


# Labels for x and g
xLabels = []
xNormLabels = []
for i in range(len(x[0])):
    if i < 9:
        xLabels.append("x{0}".format(chr(0x2080 + i + 1)))
        xNormLabels.append("x̂{0}".format(chr(0x2080 + i + 1)))
    elif i == 9:
        xLabels.append("x{0}".format(chr(0x2081)) + "{0}".format(chr(0x2080)))
        xNormLabels.append("x̂{0}".format(chr(0x2081)) + "{0}".format(chr(0x2080)))
    elif i < 99 and float(str(i)[1]) < 9:
        xLabels.append(
            "x{0}".format(chr(0x2080 + int(str(i)[0])))
            + "{0}".format(chr(0x2080 + int(str(i)[1]) + 1))
        )
        xNormLabels.append(
            "x̂{0}".format(chr(0x2080 + int(str(i)[0])))
            + "{0}".format(chr(0x2080 + int(str(i)[1]) + 1))
        )
    elif i < 99 and float(str(i)[1]) == 9:
        xLabels.append(
            "x{0}".format(chr(0x2080 + int(str(i)[0]) + 1)) + "{0}".format(chr(0x2080))
        )
        xNormLabels.append(
            "x̂{0}".format(chr(0x2080 + int(str(i)[0]) + 1)) + "{0}".format(chr(0x2080))
        )
    xLabelLatex = "x_" + str(i + 1)
    xNormLabelLatex = ("$\hat{x}_" + str(i) + "$",)
    # xLabels.append("x_"+str(i+1))
gLabels = []
for i in range(np.size(g, axis=1)):
    if i < 9:
        gLabels.append("g{0}".format(chr(0x2080 + i + 1)))
    elif i == 9:
        gLabels.append("g{0}".format(chr(0x2081)) + "{0}".format(chr(0x2080)))
    elif i < 99 and float(str(i)[1]) < 9:
        gLabels.append(
            "g{0}".format(chr(0x2080 + int(str(i)[0])))
            + "{0}".format(chr(0x2080 + int(str(i)[1]) + 1))
        )

    elif i < 99 and float(str(i)[1]) == 9:
        gLabels.append(
            "g{0}".format(chr(0x2080 + int(str(i)[0]) + 1)) + "{0}".format(chr(0x2080))
        )
    gLabelLatex = "g_" + str(i)
fgLabels = ["f"] + gLabels
gMaxLabel = "gₘₐₓ"
gMaxLabelLatex = "g_{max}"
itLabel = "nᵢₜ"
itLabelLatex = "$n_{it}$"
# Plots

# x convergence
xConv = figure(plot_width=wConvPlot, plot_height=hConvPlot)
xConvi = [None] * len(xLabels)
for i in range(len(x[0])):
    xConvi[i] = xConv.line(
        it, x[:, i], legend_label=xLabels[i], color=colorList[i], line_width=LineWidth
    )
    xConv.circle(it, x[:, i], legend_label=xLabels[i], color=colorList[i])
xConv.x_range.start = 0
xConv.x_range.end = max(it)
xConv.xaxis.axis_label = "Iteration " + itLabel
xConv.yaxis.axis_label = "Design variable value x"
# xConv.yaxis.axis_label = "Design variable value $x$"
xConv.xaxis.major_label_orientation = np.pi / 2
xConv.yaxis.axis_label_text_font_style = "normal"
xConv.xaxis.axis_label_text_font_style = "normal"
xConv.legend.location = (10, -5)
xConv.right.append(xConv.legend[0])
xConv.legend.border_line_color = None
xConv.add_tools(
    HoverTool(tooltips=[("Iteration", "@x"), ("Value", "@y")], mode="vline")
)


# x norm convergence
xNormConv = figure(plot_width=wConvPlot, plot_height=hConvPlot)
for i in range(len(x[0])):
    xNormConv.line(
        it,
        x[:, i],
        legend_label=xNormLabels[i],
        color=colorList[i],
        line_width=LineWidth,
    )
    xNormConv.circle(it, x[:, i], legend_label=xNormLabels[i], color=colorList[i])
xNormConv.x_range.start = 0
xNormConv.x_range.end = max(it)
xNormConv.xaxis.axis_label = "Iteration " + itLabel
xNormConv.yaxis.axis_label = "Normalized design variable value x̂"
# xNormConv.yaxis.axis_label = "Normalized design variable value $\hat{x}$"
xNormConv.xaxis.major_label_orientation = np.pi / 2
xNormConv.xaxis.axis_label_text_font_style = "normal"
xNormConv.yaxis.axis_label_text_font_style = "normal"
xNormConv.legend.location = (10, -5)
xNormConv.right.append(xNormConv.legend[0])
xNormConv.legend.border_line_color = None
xNormConv.add_tools(
    HoverTool(tooltips=[("Iteration", "@x"), ("Value", "@y")], mode="vline")
)

fgMaxConv = figure(plot_width=wConvPlot, plot_height=hConvPlot)
fgMaxConv.line(it, f, legend_label="f", color=colorObjective, line_width=LineWidth)
fgMaxConv.circle(it, f, legend_label="f", color=colorObjective)
fgMaxConv.x_range.start = 0
fgMaxConv.x_range.end = max(it)
fgMaxConv.yaxis.axis_label = "Objective value f"
# fgMaxConv.yaxis.axis_label = "Objective value $f$"
fgMaxConv.xaxis.axis_label = "Iteration " + itLabel
fgMaxConv.xaxis.major_label_orientation = np.pi / 2
fgMaxConv.yaxis.axis_label_text_font_style = "normal"
fgMaxConv.xaxis.axis_label_text_font_style = "normal"
fgMaxConv.y_range = Range1d(min(f), max(f))
fgMaxConv.yaxis.axis_label_text_color = color = colorObjective
gMaxMin = float(np.min(gMax))
gMaxMax = float(np.max(gMax))
fgMaxConv.extra_y_ranges = {
    "gMax": Range1d(
        start=min(np.min(gMax), -np.max(np.abs(g)) / 100),
        end=np.max(max(np.max(g), np.max(np.abs(g)) / 100)),
    )
}
# gMaxAxis = LinearAxis(axis_label="Maximum constraint value $g_{max}$",
gMaxAxis = LinearAxis(
    axis_label="Maximum constraint value " + gMaxLabel,
    y_range_name="gMax",
    axis_label_text_font_style="normal",
    axis_label_text_color=colorConstraint,
    major_label_orientation="vertical",
)
fgMaxConv.add_layout(gMaxAxis, "right")
fgMaxConv.line(
    it,
    gMax,
    legend_label=gMaxLabel,
    y_range_name="gMax",
    color=colorConstraint,
    line_width=LineWidth,
)
fgMaxConv.circle(
    it, gMax, legend_label=gMaxLabel, y_range_name="gMax", color=colorConstraint
)
fgMaxConv.legend.location = (10, -5)
fgMaxConv.right.append(fgMaxConv.legend[0])
fgMaxConv.legend.border_line_color = None
fgMaxConv.add_tools(
    HoverTool(tooltips=[("Iteration", "@x"), ("Value", "@y")], mode="vline")
)


# Constraint convergence plot
gConv = figure(plot_width=wConvPlot, plot_height=hConvPlot)
for i in range(len(g[0])):
    gConv.line(
        it, g[:, i], legend_label=gLabels[i], color=colorList[i], line_width=LineWidth
    )
    gConv.circle(it, g[:, i], legend_label=gLabels[i], color=colorList[i])
gConv.x_range.start = 0
gConv.x_range.end = max(it)
gConv.y_range.start = min(np.min(g), -0.1)
gConv.y_range.end = max(np.max(g), 0)
gConv.yaxis.axis_label = "Constraint value g"
# gConv.yaxis.axis_label = "Constraint value $g$"
gConv.xaxis.axis_label = "Iteration " + itLabel
gConv.xaxis.major_label_orientation = np.pi / 2
gConv.yaxis.axis_label_text_font_style = "normal"
gConv.xaxis.axis_label_text_font_style = "normal"
gConv.legend.location = (10, -5)
gConv.right.append(gConv.legend[0])
gConv.legend.border_line_color = None
gConv.add_tools(
    HoverTool(tooltips=[("Iteration", "@x"), ("Value", "@y")], mode="vline")
)
# Bar diagrams

# Bar diagram of current design
xBar = figure(x_range=xLabels, plot_width=wBarPlot, plot_height=hBarPlot)
xBar.y_range.start = 0
xBar.vbar(top=x[0], x=xLabels, width=0.9, color="darkgrey")
xBar.vbar(top=x[-1], x=xLabels, width=0.75, color="dodgerblue")
xBar.yaxis.axis_label = "Design variable value x"
# xBar.yaxis.axis_label = "Design variable value $x$"
xBar.xaxis.major_label_orientation = np.pi / 2
xBar.yaxis.axis_label_text_font_style = "normal"

# Bar diagram of objective functions
fg = np.zeros((np.size(g, axis=1) + 1,))
fg[0] = f[-1]
fg[1:] = g[-1, :]
fgBar = figure(x_range=fgLabels, plot_width=wBarPlot, plot_height=hBarPlot)
fgBar.vbar(top=f[0], x=["f"], width=0.9, color="darkgrey")
fgBar.vbar(top=f[-1], x=["f"], width=0.75, color=colorObjective)
fgBar.yaxis.axis_label = "Objective value f"
# fgBar.yaxis.axis_label = "Objective and constrint value $f$, $g$"
fgBar.yaxis.axis_label_text_font_style = "normal"
fgBar.xaxis.major_label_orientation = np.pi / 2
fgBar.yaxis.axis_label_text_color = color = colorObjective
fgBar.y_range.start = -max(f[-1] * 1.1, f[0] * 1.1)
fgBar.y_range.end = max(f[-1] * 1.1, f[0] * 1.1)
# fgBar.y_range.start = -f[-1]*1.1
# fgBar.y_range.end = f[-1]*1.1
fgBar.extra_y_ranges = {
    "gBar": Range1d(start=-np.max(np.abs(g)) * 1.1, end=np.max(np.max(np.abs(g)) * 1.1))
}
# fgBar.extra_y_ranges = {"gBar": Range1d(start=-np.max(np.abs(g)),
#                                        end=np.max(np.max(np.abs(g))))}
gBarAxis = LinearAxis(
    axis_label="Constraint value g",
    y_range_name="gBar",
    axis_label_text_font_style="normal",
    axis_label_text_color=colorConstraint,
    major_label_orientation="vertical",
)
fgBar.add_layout(gBarAxis, "right")
fgBar.vbar(top=g[0], x=gLabels, width=0.9, y_range_name="gBar", color="darkgrey")
fgBar.vbar(top=g[-1], x=gLabels, width=0.75, y_range_name="gBar", color=colorConstraint)
# fgBar.vbar(top=g[-1, :], x=gLabels,  width=0.75, ,
#           color=colorList[1])


# Logo
Logo = figure()
Logo.image_url(url=["DesOptPy.png"], x=0, y=1, w=1, h=1)

# Layout of sheet
title = Div(text='<h2 style="text-align: center">Design optimization monitoring</h1>')
headerConvPlot = Div(text='<h3 style="text-align: center">Convergence plots</h2>')
headerBarPlot = Div(text='<h3 style="text-align: center">Current design</h2>')
headerDetails = Div(text='<h3 style="text-align: center">Optimization details</h2>')
tab1 = Panel(child=xConv, title="Design variables")
tab2 = Panel(child=xNormConv, title="Normalized design variables")
tab3 = Panel(child=fgMaxConv, title="Objective and maximum constraint")
tab4 = Panel(child=gConv, title="Constraints")
layout = column(
    title,
    row(
        column(
            headerConvPlot,
            Tabs(tabs=[tab1, tab2, tab3, tab4]),
            Spacer(height=0),
            headerBarPlot,
            row(xBar, Spacer(width=50), fgBar),
        ),
        Spacer(width=25),
        column(
            headerDetails,
            Div(text="Run: 		" + OptName),
            Div(text="Model: 			" + OptName[:-17]),
            Div(text="Algorithm: 	" + OptAlg),
            Div(text="Start time: 	" + OptName[-14:]),
        ),
    ),
)


def update():
    x, xNorm, f, g, gMax = readHistory()


from bokeh.client import push_session

if Server:
    # update()
    # session = push_session(curdoc())
    curdoc().add_root(layout)
    curdoc().add_periodic_callback(update, 500)
    curdoc().title = OptName
    # session.show() # open the document in a browser
    # session.loop_until_closed()
else:
    # curdoc().add_root(layout)
    # curdoc().title = OptName
    output_file("opt.html")

    show(layout)
