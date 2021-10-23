from bokeh import palettes
from bokeh.plotting import figure, show, output_file, save
from bokeh.layouts import column, layout
from bokeh.models import LinearAxis, Range1d, Legend, ColumnDataSource
from bokeh.models.tools import BoxZoomTool, PanTool, ResetTool, HoverTool
import numpy as np
import panel as pn
import os


# TODO write out details at beginning including xL, xU, nx etc. Or just entire model self

"""
https://github.com/holoviz/panel/issues/1496

"""

# ds = ColumnDataSource({"x": [0], "fAll": [0], "gMax": [0]})

showPlot = True
savePlot = False
OptName = os.getcwd().split(os.sep)[-1][6:]
Dir = os.getcwd() + os.sep + os.getcwd().split(os.sep)[-1][6:]

font = 'palantino'
fontSize = '12pt'


def colorPalette(nColors):
    # Palettes: https://docs.bokeh.org/en/latest/docs/reference/palettes.html
    if nx < 11:
        colorsx = palettes.d3['Category10'][10]
    elif nx < 21:
        colorsx = (
            palettes.d3['Category20'][20][::2]
            + palettes.d3['Category20'][20][1::2]
        )
    else:
        colorsx = (
            palettes.d3['Category20'][20][::2]
            + palettes.d3['Category20'][20][1::2]
            + palettes.d3['Category20c'][20][::4]
            + palettes.d3['Category20b'][20][::4]
            + palettes.d3['Category20c'][20][1::4]
            + palettes.d3['Category20b'][20][1::4]
            + palettes.d3['Category20c'][20][2::4]
            + palettes.d3['Category20b'][20][2::4]
            + palettes.d3['Category20c'][20][3::4]
            + palettes.d3['Category20b'][20][3::4]
        )
    if nx > 60:
        colorsx *= nx // 60 + 1
    return colorsx[:nColors]


def readHistory():
    import pyOpt

    OptHist = pyOpt.History(Dir, 'r')
    xAll = OptHist.read([0, -1], ['x'])[0]['x']
    fAll = OptHist.read([0, -1], ['obj'])[0]['obj']
    gAll = OptHist.read([0, -1], ['con'])[0]['con']
    gMax = np.max(gAll, 1)
    return (xAll, fAll, gAll, gMax)


def plotStyle(p, axes, colors):
    # colors
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.background_fill_alpha = 0.0
    p.border_fill_alpha = 0.0
    p.outline_line_alpha = 0.0

    # title
    p.title.align = 'left'
    p.title.text_font = font
    p.title.text_font_size = '14pt'
    p.title.text_color = 'black'
    p.title.text_font_style = 'normal'

    # x axis
    p.xaxis.axis_label_text_font = font
    p.xaxis.axis_label_text_font_style = 'normal'
    p.xaxis.axis_label_text_font_size = fontSize
    p.xaxis.axis_label_text_color = 'black'
    p.xaxis.major_label_text_font = font
    p.xaxis.major_label_text_font_style = 'normal'
    p.xaxis.major_label_text_font_size = fontSize
    p.xaxis.major_label_text_color = 'black'
    p.xaxis.major_tick_in = 5
    p.xaxis.major_tick_out = 0
    p.xaxis.minor_tick_in = 0  # 2
    p.xaxis.minor_tick_out = 0

    # y axis
    # p.yaxis.axis_label_text_align = "horizontal"
    p.yaxis.axis_label_text_font = font
    p.yaxis.axis_label_text_font_style = 'normal'
    p.yaxis.axis_label_text_font_size = fontSize
    p.yaxis.major_label_text_font = font
    p.yaxis.major_label_text_font_style = 'normal'
    p.yaxis.major_label_text_font_size = fontSize
    if axes == 2:
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
        ds_fg.stream(
            {'x': [it[-1]], 'fAll': [fAll[-1][0]], 'gMax': [gMax[-1]]}
        )
        # ds_x.stream({"x": [it[-1]], "xAll": [xAll[-1].tolist()]})

    for i in range(nx):
        ds_x[i].stream(
            {
                'x': [it[-1]],
                # "xAll": np.array(xAlcolorPalette(4)l).reshape(nx, len(it)).tolist(),
                'xAll': [xAll[-1][i]],
            }
        )

    for i in range(ng):
        ds_g[i].stream(
            {
                'x': [it[-1]],
                'gAll': [gAll[-1][i]],
            }
        )


# Read in model information
import pickle

with open(OptName + '.pkl', 'rb') as f:
    ModelInfo = pickle.load(f)


# initial
xAll, fAll, gAll, gMax = readHistory()
i = len(fAll)
it = np.array(range(len(fAll)))

# data as data stream
# ds = ColumnDataSource({"x": it, "y": fAll, "gMax":gMax})
ds_fg = ColumnDataSource(
    {
        'x': it.tolist(),
        'fAll': np.array(fAll).reshape(len(it)).tolist(),
        'gMax': gMax.tolist(),
    }
)
nx = len(xAll[0])


# initialize objective and constraint convergence
p_fg = figure(
    sizing_mode='stretch_both', toolbar_location='above', toolbar_sticky=False
)
p_fg.xaxis.axis_label = 'evaluation'

# second y axis
gDelta = (max(gMax) - min(gMax)) * 0.025
p_fg.extra_y_ranges = {
    'constraint': Range1d(
        start=min(gMax) - gDelta,  # np.sign(max(gMax)) * gDelta,
        end=max(gMax) + gDelta,  # np.sign(min(gMax)) * gDelta,
    )
}
p_fg.add_layout(LinearAxis(y_range_name='constraint'), 'right')
fDelta = (max(fAll)[0] - min(fAll)[0]) * 0.025
p_fg.y_range = Range1d(
    start=min(fAll)[0] - fDelta,  # np.sign(max(fAll)[0]) * fDelta,
    end=max(fAll)[0] + fDelta,  # np.sign(min(fAll)[0]) * fDelta,
)
# p_fg.y_range.range_padding = fDelta[0]*0.01
# p_fg.y_range.range_padding = fDelta[0]*0.01

colors_fg = colorPalette(10)
# plot style
p_fg = plotStyle(p_fg, 2, colors_fg)
p_fg.yaxis[0].axis_label = 'objective value'
p_fg.yaxis[1].axis_label = 'maximum constraint value'


# plot
p_fg.line(x='x', y='fAll', line_color=colors_fg[0], source=ds_fg)
p_fg.circle(
    x='x',
    y='fAll',
    fill_color='white',
    line_color='white',
    source=ds_fg,
    size=10,
)
p_fg.circle(
    x='x',
    y='fAll',
    fill_color=colors_fg[0],
    line_color=colors_fg[0],
    source=ds_fg,
    size=5,
)
p_fg.line(
    x='x',
    y='gMax',
    line_color=colors_fg[3],
    y_range_name='constraint',
    source=ds_fg,
)
p_fg.circle(
    x='x',
    y='gMax',
    fill_color='white',
    line_color='white',
    y_range_name='constraint',
    source=ds_fg,
    size=10,
)
p_fg.circle(
    x='x',
    y='gMax',
    fill_color=colors_fg[3],
    line_color=colors_fg[3],
    y_range_name='constraint',
    source=ds_fg,
)


# Design variable convergence
"""
https://medium.com/@andrewm4894/bokeh-battles-part-1-multi-line-plots-311109992fdc
https://towardsdatascience.com/draw-beautiful-and-interactive-line-charts-using-bokeh-in-python-9f3e11e0a16e
"""


# initialize design variable convergence
p_x = figure(
    sizing_mode='stretch_both', toolbar_location='above', toolbar_sticky=False
)
p_x.xaxis.axis_label = 'evaluation'
p_x.yaxis.axis_label = 'normalized design variable value'
colorsx = colorPalette(nx)
# plot style
p_x = plotStyle(p_x, 1, colorsx)

# plot
# p_x.multi_line(
#     xs="x",
#     ys="xAll",
#     source=ds_x,
#     color=["red", "blue"],
# )
ds_x = [[]] * nx
for i in range(nx):
    ds_x[i] = ColumnDataSource(
        {
            'x': it.tolist(),
            # "xAll": np.array(xAll).reshape(nx, len(it)).tolist(),
            'xAll': np.array(xAll)[:, i].tolist(),
        }
    )

    p_x.line(
        x='x',
        y='xAll',
        source=ds_x[i],
        color=colorsx[i],
        legend_label='design variable ' + str(i + 1),
    )  # legend_label=r"$\\hat{x}_"+str(i+1)+"$")
    p_x.circle(
        x='x',
        y='xAll',
        source=ds_x[i],
        legend_label='design variable ' + str(i + 1),
        fill_color='white',
        line_color='white',
        size=10,
    )
    p_x.circle(
        x='x',
        y='xAll',
        source=ds_x[i],
        color=colorsx[i],
        size=5,
        legend_label='design variable ' + str(i + 1),
    )

p_x.add_layout(p_x.legend[0], 'right')
p_x.legend.click_policy = 'hide'
p_x.legend.background_fill_alpha = 0.0
p_x.legend.border_line_alpha = 0.0
p_x.legend.label_text_font = font
p_x.legend.label_text_font_size = '12pt'


# initialize design variable convergence
ng = len(gAll[0])
p_g = figure(
    sizing_mode='stretch_both', toolbar_location='above', toolbar_sticky=False
)
p_g.xaxis.axis_label = 'evaluation'
p_g.yaxis.axis_label = 'constraint value'
colors_g = colorPalette(ng)
# plot style
p_g = plotStyle(p_g, 1, colors_g)

# plot
# p_x.multi_line(
#     xs="x",
#     ys="xAll",
#     source=ds_x,
#     color=["red", "blue"],
# )
ds_g = [[]] * ng
for i in range(ng):
    ds_g[i] = ColumnDataSource(
        {
            'x': it.tolist(),
            # "xAll": np.array(xAll).reshape(nx, len(it)).tolist(),
            'gAll': np.array(gAll)[:, i].tolist(),
        }
    )

    p_g.line(
        x='x',
        y='gAll',
        source=ds_g[i],
        color=colors_g[i],
        legend_label='constraint ' + str(i + 1),
    )  # legend_label=r"$\\hat{x}_"+str(i+1)+"$")
    p_g.circle(
        x='x',
        y='gAll',
        source=ds_g[i],
        legend_label='constraint ' + str(i + 1),
        fill_color='white',
        line_color='white',
        size=10,
    )
    p_g.circle(
        x='x',
        y='gAll',
        legend_label='constraint ' + str(i + 1),
        source=ds_g[i],
        color=colors_g[i],
        size=5,
    )

p_g.add_layout(p_g.legend[0], 'right')
p_g.legend.click_policy = 'hide'
p_g.legend.background_fill_alpha = 0.0
p_g.legend.border_line_alpha = 0.0
p_g.legend.label_text_font = font
p_g.legend.label_text_font_size = '12pt'


# layout
"""
https://docs.bokeh.org/en/latest/docs/user_guide/layout.html
"""
plotLayout = layout(
    [
        [p_fg],
        [p_x],
        [p_g],
    ],
    sizing_mode='stretch_both',
)

pane = pn.panel(plotLayout).servable()
pn.state.add_periodic_callback(update, 100)

if showPlot:
    show(plotLayout)

if savePlot:
    output_file(filename='Try.html', title='DesOptPy')
    save(plotLayout)
