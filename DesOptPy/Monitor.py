from bokeh.plotting import figure
from bokeh.models import LinearAxis, Range1d, Legend, ColumnDataSource
from bokeh.models.tools import BoxZoomTool, PanTool, ResetTool, HoverTool
import numpy as np
import panel as pn
import os

"""
https://github.com/holoviz/panel/issues/1496

"""

# ds = ColumnDataSource({"x": [0], "fAll": [0], "gMax": [0]})


Name = os.getcwd() + os.sep + os.getcwd().split(os.sep)[-1][6:]
colors = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]
font = "palantino"
fontSize = "15pt"


def readHistory():
    import pyOpt

    OptHist = pyOpt.History(Name, "r")
    xAll = OptHist.read([0, -1], ["x"])[0]["x"]
    fAll = OptHist.read([0, -1], ["obj"])[0]["obj"]
    gAll = OptHist.read([0, -1], ["con"])[0]["con"]
    gMax = np.max(gAll, 1)
    return (xAll, fAll, gAll, gMax)


def plotStyleTwoAxis(p):
    # colors
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.background_fill_alpha = 0.0
    p.border_fill_alpha = 0.0
    p.outline_line_alpha = 0.0

    # title
    p.title.align = "left"
    p.title.text_font = font
    p.title.text_font_size = "14pt"
    p.title.text_color = "black"
    p.title.text_font_style = "normal"

    # x axis
    p.xaxis.axis_label_text_font = font
    p.xaxis.axis_label_text_font_style = "normal"
    p.xaxis.axis_label_text_font_size = fontSize
    p.xaxis.axis_label_text_color = "black"
    p.xaxis.major_label_text_font = font
    p.xaxis.major_label_text_font_style = "normal"
    p.xaxis.major_label_text_font_size = fontSize
    p.xaxis.major_label_text_color = "black"
    p.xaxis.major_tick_in = 5
    p.xaxis.major_tick_out = 0
    p.xaxis.minor_tick_in = 0  # 2
    p.xaxis.minor_tick_out = 0

    # y axis
    # p.yaxis.axis_label_text_align = "horizontal"
    p.yaxis.axis_label_text_font = font
    p.yaxis.axis_label_text_font_style = "normal"
    p.yaxis.axis_label_text_font_size = fontSize
    p.yaxis.major_label_text_font = font
    p.yaxis.major_label_text_font_style = "normal"
    p.yaxis.major_label_text_font_size = fontSize
    p.yaxis[0].axis_label_text_color = colors[0]
    p.yaxis[1].axis_label_text_color = colors[3]
    p.yaxis[0].major_label_text_color = colors[0]
    p.yaxis[1].major_label_text_color = colors[3]
    p.yaxis[0].major_tick_line_color = colors[0]
    p.yaxis[1].major_tick_line_color = colors[3]
    p.yaxis[0].axis_line_color = colors[0]
    p.yaxis[1].axis_line_color = colors[3]
    p.yaxis.major_tick_in = 5
    p.yaxis.major_tick_out = 0
    p.yaxis.minor_tick_in = 0  # 2
    p.yaxis.minor_tick_out = 0

    # toolbar
    p.toolbar.logo = None
    # p.add_tools(PanTool(dimensions="width"))
    # p.add_tools(HoverTool(
    #     tooltips=[
    #         ('evaluation',   '@x{0}'            ),
    #         ('objective',  "@y2{0.009}"),
    #         ('max constraint', '@y3{0.000}'),
    #     ],
    #     line_policy='nearest',
    #     mode='vline'))

    return p


def update(event=None):
    global i
    xAll, fAll, gAll, gMax = readHistory()
    it = np.array(range(len(fAll)))
    if i < len(it):
        i += 1
        ds.stream({"x": [it[-1]], "fAll": [fAll[-1][0]], "gMax": [gMax[-1]]})


# initial
xAll, fAll, gAll, gMax = readHistory()
i = len(fAll)
it = np.array(range(len(fAll)))
# ds = ColumnDataSource({"x": it, "y": fAll, "gMax":gMax})
ds = ColumnDataSource(
    {
        "x": it.tolist(),
        "fAll": np.array(fAll).reshape(len(it)).tolist(),
        "gMax": gMax.tolist(),
    }
)

# initialize figure
p = figure(sizing_mode="stretch_both", toolbar_location="above", toolbar_sticky=False)
p.xaxis.axis_label = "evaluation"

# second y axis
p.extra_y_ranges = {"constraint": Range1d(start=min(gMax), end=max(gMax))}
p.add_layout(LinearAxis(y_range_name="constraint"), "right")

# plot style
p = plotStyleTwoAxis(p)

# plot
p.line(x="x", y="fAll", line_color=colors[0], source=ds)
p.circle(x="x", y="fAll", fill_color="white", line_color="white", source=ds, size=10)
p.circle(x="x", y="fAll", fill_color=colors[0], line_color=colors[0], source=ds, size=5)
p.line(x="x", y="gMax", line_color=colors[3], y_range_name="constraint", source=ds)
p.circle(
    x="x",
    y="gMax",
    fill_color="white",
    line_color="white",
    y_range_name="constraint",
    source=ds,
    size=10,
)
p.circle(
    x="x",
    y="gMax",
    fill_color=colors[3],
    line_color=colors[3],
    y_range_name="constraint",
    source=ds,
)

# update
pane = pn.panel(p).servable()
pn.state.add_periodic_callback(update, 100)
