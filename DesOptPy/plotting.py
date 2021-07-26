import matplotlib.pyplot as plt
import numpy as np
import dufte
import seaborn as sns

#plt.style.use(dufte.style)
#plt.rcParams['font.family'] = 'serif'
#plt.rcParams['font.serif'] = "Palatino"
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Palatino"],
})

maxDots = 20
lineThick = 0.75


def plotConvergence(self, show=True, savePDF=False,savePNG=False,
                    saveSVG=False, saveTikZ=False):

    def ConvergencePlot(r, legend, ylabel=[], plotType=1):
        if plotType==1:
            fig, ax = plt.subplots()
            if legend == "g" and (np.max(r)-np.min(r))>1e3:
                log = True
            if np.size(r) > self.nIt:
                for i in range(np.size(r)//self.nIt):
                    ax.plot(np.array(r)[:, i], clip_on=False, linestyle="-",
                            linewidth=lineThick, zorder=1,
                            label="$" + legend + "_{"+str(i+1)+"}$")
                    if self.nIt < maxDots:
                        ax.scatter(list(range(0, self.nIt, 1)), np.array(r)[:, i],
                                   color='white', s=50, zorder=2)
                        ax.scatter(list(range(0, self.nIt, 1)),
                                   np.array(r)[:, i], clip_on=False, s=5, zorder=3)
            else:
                ax.plot(r, clip_on=False, linestyle="-", linewidth=lineThick,
                        zorder=1, label="$" + legend + "$")
                if self.nIt < maxDots:
                    ax.scatter(list(range(0, self.nIt, 1)), r,
                               color='white', s=50, zorder=2)
                    ax.scatter(list(range(0, self.nIt, 1)), r, s=5, zorder=3,
                               clip_on=False)
            plt.xlabel("iteration $i_{it}$")
            dufte.ylabel(ylabel)
            dufte.legend()
            sns.despine()

            # axes shift
            buffer = 0.1
            xDelta = self.nIt-1
            yDelta = np.max(r)-np.min(r)

            ax.spines['bottom'].set_bounds(0, self.nIt-1)
            ax.spines['left'].set_bounds(np.min(r),
                                         np.max(r))
            if self.nIt < 21:
                x_ticks = list(range(0, self.nIt, 1))
                ax.xaxis.set_ticks(x_ticks)
            elif self.nIt < 41:
                x_ticks = list(range(0, self.nIt, 2))
                ax.xaxis.set_ticks(x_ticks)
            #yStep = yDelta//3
            #y_ticks = list(np.arange(np.min(r), np.max(r), int(yStep)))
            #ax.yaxis.set_ticks(y_ticks)
            #for label in ax.get_yticklabels()[::2]:
            #    label.set_visible(False)
            #else:
            #    x_ticks = list(range(0, self.nIt))
            #ax.yaxis.set_major_locator(ticker.MultipleLocator(base=25))
            #ax.tick_params(direction='in')
            ax.set_xlim([-buffer*xDelta, self.nIt-1])
            #ax.set_ylim([ax.get_ylim()[0], ax.get_ylim()[1]])
            ax.set_ylim([np.min(r)-buffer*yDelta,
                         np.max(r)])

            # ticks inward
            ax.tick_params(direction='in')

            # make space
            fig.tight_layout()

            plotName = (str.split(self.RunDir, "/")[-1][6:] +
                        str.split(ylabel, " ")[0].title()).replace("\n", "")

        else:
            def adjust_spines(ax, spines, color):
                for loc, spine in ax.spines.items():
                    if loc in spines:
                        spine.set_position(('outward', 24))  # outward by 10 points
                        if loc == "bottom":
                            spine.set_color("black")
                        else:
                            spine.set_color(color)

                    else:
                        spine.set_color('none')  # don't draw spine
            fig = plt.figure()
            x = np.linspace(0, 6)
            y = 2 * np.sin(x)
            ax = fig.add_subplot()
            ax2 = ax.twinx()

            ax.plot(r[0], clip_on=False, linestyle="-", linewidth=lineThick,
                     color="tab:blue", zorder=1)
            ax2.plot(r[1], clip_on=False, linestyle="-", linewidth=lineThick,
                     color="tab:red", zorder=1)
            if self.nIt < maxDots:
                ax.scatter(list(range(0, self.nIt, 1)), r[0],
                           color='white', s=50, zorder=2)
                ax.scatter(list(range(0, self.nIt, 1)), r[0], s=5, zorder=3,
                           clip_on=False, color="tab:blue")
                ax2.scatter(list(range(0, self.nIt, 1)), r[1],
                           color='white', s=50, zorder=2)
                ax2.scatter(list(range(0, self.nIt, 1)), r[1], s=5, zorder=3,
                           clip_on=False, color="tab:red")
            adjust_spines(ax, ['bottom', 'left'], "tab:blue")
            adjust_spines(ax2, ['right'], "tab:red")
            ax.set_xlim([0, self.nIt-1])
            ax2.set_xlim([0, self.nIt-1])

            ax.set_ylim([min(r[0])[0], max(r[0])[0]])
            ax2.set_ylim([min(r[1]), max(r[1])])
            #ax2.set_ylim([np.min(np.array(r)[:,1]), np.max(np.array(r)[:,1])])
            ax.set_ylabel("objective value $f$", rotation='horizontal', position=(0, 1.05))
            ax2.set_ylabel("max constraint value $g_{\max}$", rotation='horizontal', position=(0, 1.1))
            ax.set_xlabel("iteration $i_{it}$")
            ax.tick_params(axis='y', colors="tab:blue")
            ax2.tick_params(axis='y', colors="tab:red")
            ax.yaxis.label.set_color("tab:blue")
            ax2.yaxis.label.set_color("tab:red")


            # ticks inward
            ax.tick_params(direction='in')
            ax2.tick_params(direction='in')

            plotName = (str.split(self.RunDir, "/")[-1][6:] +
                        "ObjectiveMaxConstraint")

        if savePNG:
            plt.savefig(plotName + '.png', dpi=400)
        if saveTikZ:
            import tikzplotlib
            tikzplotlib.save(plotName + ".pgf", show_info=False, strict=False,
                             extra_axis_parameters={
                                 "ylabel style={rotate=90.0}",
                                 "xmin=0",
                                 "ymin="+str(np.min(r)),
                                 "ymax="+str(np.max(r))
                                 })

            plt.savefig(plotName + '2.pgf')
        if saveSVG:
            plt.savefig(plotName + ".svg")
        if savePDF:
            plt.savefig(plotName + '.pdf', backend='pgf')
        if show:
            plt.show()

    ConvergencePlot(self.xIt, "x", "design variable value")
    ConvergencePlot(self.xNormIt, "\hat{x}", "normalized\ndesign variable value")
    ConvergencePlot(self.fIt, "f", "objective function value")
    if self.g is not None:
        ConvergencePlot(self.gIt, "g", "constraint function value")
        ConvergencePlot([self.fIt, self.gMaxIt], ["f", "g"], plotType=2)

    # # objective and max constraint convergence
    # fig, ax1 = plt.subplots()
    # ax2 = ax1.twinx()
    # ax1.plot(self.fIt, label="$f$", color="green")
    # dufte.legend()
    # ax2.plot(np.max(np.array(self.gIt), 1), label="$g_{\max}$", color="red")
    # plt.xlabel("iteration $i_{it}$")
    # dufte.legend()
    # #sns.despine()
    # plt.show()


def plotBeforeAfter(self):
    """
    I will add bar plots here for initial and optimal values
    x
    xNorm
    f
    g

    """
    pass


def PrintTikZInfo():
    tikzMessage = r"""
To use PGF files (TikZ) in LyX and LaTeX:

At top of document initialize values:

    \newlength\figureheight
    \newlength\figurewidth

Where you want figure, use the following code
(set height and width to desire size):

    \setlength\figureheight{5.0cm}
    \setlength\figurewidth{7cm}
    \input{FigureName.pgf}


For Tufte style add following to LaTeX/LyX preamble:

\usepackage{pgfplots}
\pgfplotsset{compat=newest}
\pgfplotsset{every axis y label/.style={at={(-0.1, 1.05)},
									   anchor=south east,
                                        rotate=0.0},
             axis x line*=bottom,
             axis y line*=left,
             axis x line shift=17pt,
             axis y line shift=17pt,
             separate axis lines,
             clip=false}

also changed
/usr/local/lib/python3.9/dist-packages/tikzplotlib/_text.py line 51
    scaling = 1.0 * size / data["font size"]
"""
    print(tikzMessage)
