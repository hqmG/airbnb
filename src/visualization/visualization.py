"""
Function script for visualization.
"""
# Modules
from matplotlib import pyplot
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import pandas
import seaborn
from typing import Tuple


def barplot(
    series: pandas.Series,
    max_features: int = 50,
    figsize: Tuple = (18, 7.5),
) -> Tuple[Figure, Axes]:
    """
    Plotting barplot.

    Args:
        series: Data to plot.
        max_features: Maximum number of labels.
        figsize: Size of figure.

    Returns:
        Figure and axes.
    """
    # Color
    color = seaborn.cubehelix_palette(
        start=0.2,
        rot=-0.3,
        as_cmap=True,
    ).colors[int(0.5*256)]

    # Labels
    if len(series) > max_features:
        series = series[:max_features]

    # Figure and axes
    figure, axes = pyplot.subplots(2, 1, figsize=figsize)

    # Barplot
    if len(series) > 0:
        axes[0].bar(series.index, series.values, color=color)
    axes[0].set_ylabel('COUNT')
    axes[0].set_xticklabels([])

    # Log barplot
    if len(series) > 0:
        axes[1].bar(series.index, series.values, log=True, color=color)
    axes[1].set_ylabel('log(COUNT)')
    axes[1].tick_params('x', labelrotation=90)
    return figure, axes


def lineplot(
    df: pandas.DataFrame,
    x: str,
    y: str,
    hue: str = None,
    figsize: Tuple[float] = (18, 7.5)
) -> Tuple[Figure, Axes]:
    """
    Plotting lineplot.

    Args:
        df: Data to plot.
        x: Horizontal feature.
        y: Vertical feature.
        hue: Grouping feature.
        figsize: Size of figure.

    Returns:
        Figure and axes.
    """
    # Colors
    colors = seaborn.cubehelix_palette(
        n_colors=df[hue].nunique() if hue else 256,
        start=0.2,
        rot=-0.3,
        as_cmap=False if hue else True
    )
    kwargs = {
        'color': colors.colors[int(0.5*256)] if not hue else None,
        'palette': colors if hue else None,
    }

    # Figure and axes
    figure, axes = pyplot.subplots(1, 1, figsize=figsize)
    axes = [axes]

    # Lineplot
    axes[0] = seaborn.lineplot(df, x=x, y=y, hue=hue, ax=axes[0], **kwargs)
    axes[0].set_xlim(df[x].iloc[0], df[x].iloc[-1])
    return figure, axes
