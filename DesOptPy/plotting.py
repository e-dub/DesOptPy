import matplotlib.pyplot as plt
import numpy as np
import dufte
import seaborn as sns


plt.rcParams.update(
    {
        'text.usetex': True,
        'font.family': 'serif',
        'font.serif': ['Palatino'],
    }
)

maxDots = 20
maxLineLables = 25
lineThick = 0.75


def plotConvergence(
    self,
    show=True,
    savePDF=False,
    savePNG=False,
    saveSVG=False,
    saveTikZ=False,
):

    # TDO: if nEval then only dots!
    # TODO change x label!
    def ConvergencePlot(r, legend, ylabel=[], plotType=1, xAxis='it'):
        if self.xIt is None:
            xAxisVal = self.nEval
            xLabel = 'evaluation $i_{\\mathrm{eval}}$'
        else:
            xAxisVal = self.nIt
            xLabel = 'iteration $i_{it}$'
        if plotType == 1:
            fig, ax = plt.subplots()
            # if legend == 'g' and (np.max(r) - np.min(r)) > 1e3:
            #     log = True
            if np.size(r) > xAxisVal:
                for i in range(np.size(r) // xAxisVal):
                    ax.plot(
                        np.array(r)[:, i],
                        linestyle='-',
                        clip_on=False,
                        linewidth=lineThick,
                        zorder=1,
                        label='$' + legend + '_{' + str(i + 1) + '}$',
                    )
                    if xAxisVal < maxDots:
                        ax.scatter(
                            list(range(0, xAxisVal, 1)),
                            np.array(r)[:, i],
                            color='white',
                            s=50,
                            zorder=2,
                        )
                        ax.scatter(
                            list(range(0, xAxisVal, 1)),
                            np.array(r)[:, i],
                            clip_on=False,
                            s=5,
                            zorder=3,
                        )
            else:
                ax.plot(
                    r,
                    # ".",
                    linestyle='-',
                    clip_on=False,
                    linewidth=lineThick,
                    zorder=1,
                    label='$' + legend + '$',
                )
                if xAxisVal < maxDots:
                    ax.scatter(
                        list(range(0, xAxisVal, 1)),
                        r,
                        color='white',
                        s=50,
                        zorder=2,
                    )
                    ax.scatter(
                        list(range(0, xAxisVal, 1)),
                        r,
                        s=5,
                        zorder=3,
                        clip_on=False,
                    )
            plt.xlabel(xLabel)
            dufte.ylabel(ylabel)
            if np.size(r) / xAxisVal < maxLineLables + 1:
                dufte.legend()
            sns.despine()

            # axes shift
            buffer = 0.1
            xDelta = xAxisVal - 1
            yDelta = np.max(r) - np.min(r)

            ax.spines['bottom'].set_bounds(0, xAxisVal - 1)
            ax.spines['left'].set_bounds(np.min(r), np.max(r))
            if xAxisVal < 21:
                x_ticks = list(range(0, xAxisVal, 1))
                ax.xaxis.set_ticks(x_ticks)
            elif xAxisVal < 41:
                x_ticks = list(range(0, xAxisVal, 2))
                ax.xaxis.set_ticks(x_ticks)
            # yStep = yDelta//3
            # y_ticks = list(np.arange(np.min(r), np.max(r), int(yStep)))
            # ax.yaxis.set_ticks(y_ticks)
            # for label in ax.get_yticklabels()[::2]:
            #    label.set_visible(False)
            # else:
            #    x_ticks = list(range(0, self.nIt))
            # ax.yaxis.set_major_locator(ticker.MultipleLocator(base=25))
            # ax.tick_params(direction='in')
            ax.set_xlim([-buffer * xDelta, xAxisVal - 1])
            # ax.set_ylim([ax.get_ylim()[0], ax.get_ylim()[1]])
            ax.set_ylim([np.min(r) - buffer * yDelta, np.max(r)])

            # ticks inward
            ax.tick_params(direction='in')

            # make space
            fig.tight_layout()

            plotName = (
                str.split(self.RunDir, '/')[-1][6:]
                + str.split(ylabel, ' ')[0].title()
                + 'Convergence'
            ).replace('\n', '')

        else:

            def adjust_spines(ax, spines, color):
                for loc, spine in ax.spines.items():
                    if loc in spines:
                        spine.set_position(
                            ('outward', 24)
                        )  # outward by 10 points
                        if loc == 'bottom':
                            spine.set_color('black')
                        else:
                            spine.set_color(color)

                    else:
                        spine.set_color('none')  # don't draw spine

            fig = plt.figure(figsize=[6.2 * 1.666, 4.8])
            x = np.linspace(0, 6)
            y = 2 * np.sin(x)
            ax = fig.add_subplot()
            ax2 = ax.twinx()

            ax.plot(
                r[0],
                clip_on=False,
                linestyle='-',
                linewidth=lineThick,
                color='tab:blue',
                zorder=1,
            )
            ax2.plot(
                r[1],
                clip_on=False,
                linestyle='-',
                linewidth=lineThick,
                color='tab:red',
                zorder=1,
            )
            if xAxisVal < maxDots:
                ax.scatter(
                    list(range(0, xAxisVal, 1)),
                    r[0],
                    color='white',
                    s=50,
                    zorder=2,
                )
                ax.scatter(
                    list(range(0, xAxisVal, 1)),
                    r[0],
                    s=5,
                    zorder=3,
                    clip_on=False,
                    color='tab:blue',
                )
                ax2.scatter(
                    list(range(0, xAxisVal, 1)),
                    r[1],
                    color='white',
                    s=50,
                    zorder=2,
                )
                ax2.scatter(
                    list(range(0, xAxisVal, 1)),
                    r[1],
                    s=5,
                    zorder=3,
                    clip_on=False,
                    color='tab:red',
                )
            adjust_spines(ax, ['bottom', 'left'], 'tab:blue')
            adjust_spines(ax2, ['right'], 'tab:red')
            ax.set_xlim([0, xAxisVal - 1])
            ax2.set_xlim([0, xAxisVal - 1])
            if xAxisVal < 21:
                x_ticks = list(range(0, xAxisVal, 1))
                ax.xaxis.set_ticks(x_ticks)
                ax2.xaxis.set_ticks(x_ticks)
            elif xAxisVal < 41:
                x_ticks = list(range(0, xAxisVal, 2))
                ax.xaxis.set_ticks(x_ticks)
                ax2.xaxis.set_ticks(x_ticks)
            ax.set_ylim([min(r[0]), max(r[0])])
            ax2.set_ylim([min(np.min(r[1]), 0), max(np.max(r[1]), 0)])
            # ax2.set_ylim([np.min(np.array(r)[:,1]), np.max(np.array(r)[:,1])])
            # ax.set_ylabel("objective value $f$", rotation='horizontal', position=(0, 1.05))
            # ax2.set_ylabel("max constraint value $g_{\max}$", rotation='horizontal', position=(0, 1.09))

            ax.set_ylabel(
                'objective function value $f$',
                rotation='horizontal',
                verticalalignment='baseline',
            )
            ax.yaxis.set_label_coords(-0.3, 1.05)
            ax2.set_ylabel(
                'max constraint value $g_{\\max}$',
                rotation='horizontal',
                verticalalignment='baseline',
            )
            ax2.yaxis.set_label_coords(1.3, 1.05)

            # ax.set_ylabel("objective function value $f$", rotation='horizontal', verticalalignment='baseline', loc="top")
            # ax2.set_ylabel("max constraint value $g_{\max}$", rotation='horizontal', verticalalignment='baseline', loc="top")

            ax.set_xlabel(xLabel)
            ax.tick_params(axis='y', colors='tab:blue')
            ax2.tick_params(axis='y', colors='tab:red')
            ax.yaxis.label.set_color('tab:blue')
            ax2.yaxis.label.set_color('tab:red')

            # ticks inward
            ax.tick_params(direction='in')
            ax2.tick_params(direction='in')

            # make space
            fig.tight_layout()

            plotName = (
                str.split(self.RunDir, '/')[-1][6:]
                + 'ObjectiveMaxConstraintConvergence'
            )

        if savePNG:
            plt.savefig(
                plotName + '.png',
                dpi=400,
                transparent=True,
                bbox_inches='tight',
                pad_inches=0,
            )
        if saveTikZ:
            import tikzplotlib

            tikzplotlib.save(
                plotName + '.pgf',
                show_info=False,
                strict=False,
                extra_axis_parameters={
                    'ylabel style={rotate=90.0}',
                    'height=\\figureheight',
                    'width=\\figurewidth',
                    'xmin=0',
                    'ymin=' + str(np.min(r)),
                    'ymax=' + str(np.max(r)),
                },
            )
            # plt.savefig(plotName + '.pgf', transparent=True)
        if saveSVG:
            plt.savefig(
                plotName + '.svg',
                transparent=True,
                bbox_inches='tight',
                pad_inches=0,
            )
        if savePDF:
            plt.savefig(
                plotName + '.pdf',
                backend='pgf',
                transparent=True,
                bbox_inches='tight',
                pad_inches=0,
            )
        if show:
            plt.show()

    if self.xIt is None:
        ConvergencePlot(self.xAll, 'x', 'design variable value', xAxis='eval')
        # ConvergencePlot(self.xNormAll,
        #                "\hat{x}",
        #                "normalized\ndesign variable value",
        #                xAxis="eval")
        ConvergencePlot(
            self.fAll, 'f', 'objective function value', xAxis='eval'
        )
        if self.g is not None:
            ConvergencePlot(
                self.gAll, 'g', 'constraint function value', xAxis=self.nEval
            )
            ConvergencePlot(
                [self.fAll, self.gMax], ['f', 'g'], plotType=2, xAxis='eval'
            )

    else:
        ConvergencePlot(self.xIt, 'x', 'design variable value')
        ConvergencePlot(
            self.xNormIt, '\\hat{x}', 'normalized\ndesign variable value'
        )
        ConvergencePlot(self.fIt, 'f', 'objective function value')
        if self.g is not None:
            ConvergencePlot(self.gIt, 'g', 'constraint function value')
            ConvergencePlot([self.fIt, self.gMaxIt], ['f', 'g'], plotType=2)

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


def plotBeforeAfter(
    self,
    show=True,
    savePDF=False,
    savePNG=False,
    saveSVG=False,
    saveTikZ=False,
):
    def BarPlot(r0, rOpt, legend, ylabel=[], xlabelextra='', color='blue'):
        nx = len(r0)
        labels = [
            '$' + legend + '_{' + str(i) + ' }$' for i in range(1, nx + 1)
        ]
        labels = labels[::-1]

        index = list(range(1, nx + 1))
        index1 = np.array(index) + 0.1
        index2 = np.array(index) - 0.1
        if nx == 1:
            ysize = 0.1
        else:
            ysize = 0.3 + nx * 0.5
        fig, ax = plt.subplots(figsize=(6.2, ysize))

        plt.hlines(
            y=index1,
            xmin=0,
            xmax=r0[::-1],
            color='tab:' + color,
            alpha=0.25,
            linewidth=10,
            clip_on=False,
        )
        plt.hlines(
            y=index2,
            xmin=0,
            xmax=rOpt[::-1],
            color='tab:' + color,
            linewidth=10,
            clip_on=False,
        )

        ax.set_xlabel(xlabelextra + 'value')
        ax.set_ylabel(
            ylabel,
            rotation='horizontal',
            verticalalignment='baseline',
            loc='top',
        )

        ax.tick_params(axis='both', which='major')
        plt.yticks(index, labels)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.spines['left'].set_bounds((1, len(index)))

        if xlabelextra == '':
            val = 0
        else:
            val = 1

        ax.set_xlim(
            np.min([0, np.min(r0), np.min(rOpt)]),
            np.max([0, np.max(r0), np.max(rOpt), val]),
        )

        ax.spines['left'].set_position(('outward', 24))
        ax.spines['bottom'].set_position(('outward', -10))

        # ticks inward
        ax.tick_params(direction='in')

        # make space
        fig.tight_layout()

        plotName = (
            str.split(self.RunDir, '/')[-1][6:]
            + xlabelextra.replace(' ', '').title()
            + str.split(ylabel, ' ')[0].title()
            + 'Bar'
        ).replace('\n', '')

        if savePNG:
            plt.savefig(
                plotName + '.png',
                dpi=400,
                transparent=True,
                bbox_inches='tight',
                pad_inches=0,
            )
        if saveTikZ:
            import tikzplotlib

            tikzplotlib.save(
                plotName + '.pgf',
                show_info=False,
                strict=False,
                extra_axis_parameters={
                    'ylabel style={rotate=90.0}',
                    'height=\\figureheight',
                    'width=\\figurewidth',
                },
            )
            # plt.savefig(plotName + '.pgf', transparent=True)
        if saveSVG:
            plt.savefig(
                plotName + '.svg',
                transparent=True,
                bbox_inches='tight',
                pad_inches=0,
            )
        if savePDF:
            plt.savefig(
                plotName + '.pdf',
                backend='pgf',
                transparent=True,
                bbox_inches='tight',
                pad_inches=0,
            )
        if show:
            plt.show()

    BarPlot(self.x0, self.xOpt, 'x', 'design variable')
    BarPlot(
        np.array(self.xNorm0),
        self.xNormOpt,
        '\\hat{x}',
        'design variable',
        'normalized ',
    )
    # BarPlot(self.fIt, "f", "objective function value")
    if self.g is not None:
        BarPlot(self.g0, self.gOpt, 'g', 'constraint function', color='red')


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
