"""Module with matplotlib plotting routines. These are not hooked up to
any particular qcdb data structures but can be called with basic
arguments.

"""
from __future__ import absolute_import
from __future__ import print_function
import os

def ternary(sapt, title='', labeled=True, view=True,
            saveas=None, relpath=False, graphicsformat=['pdf']):
    """Takes array of arrays *sapt* in form [elst, indc, disp] and builds formatted
    two-triangle ternary diagrams. Either fully-readable or dotsonly depending
    on *labeled*. Saves in formats *graphicsformat*.

    """
    import hashlib
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from matplotlib.path import Path
    import matplotlib.patches as patches

    # initialize plot
    fig, ax = plt.subplots(figsize=(6, 3.6))
    plt.xlim([-0.75, 1.25])
    plt.ylim([-0.18, 1.02])
    plt.xticks([])
    plt.yticks([])
    ax.set_aspect('equal')

    if labeled:
        # form and color ternary triangles
        codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
        pathPos = Path([(0., 0.), (1., 0.), (0.5, 0.866), (0., 0.)], codes)
        pathNeg = Path([(0., 0.), (-0.5, 0.866), (0.5, 0.866), (0., 0.)], codes)
        ax.add_patch(patches.PathPatch(pathPos, facecolor='white', lw=2))
        ax.add_patch(patches.PathPatch(pathNeg, facecolor='#fff5ee', lw=2))

        # form and color HB/MX/DD dividing lines
        ax.plot([0.667, 0.5], [0., 0.866], color='#eeb4b4', lw=0.5)
        ax.plot([-0.333, 0.5], [0.577, 0.866], color='#eeb4b4', lw=0.5)
        ax.plot([0.333, 0.5], [0., 0.866], color='#7ec0ee', lw=0.5)
        ax.plot([-0.167, 0.5], [0.289, 0.866], color='#7ec0ee', lw=0.5)

        # label corners
        ax.text(1.0, -0.15, u'Elst (\u2212)',
            verticalalignment='bottom', horizontalalignment='center',
            family='Times New Roman', weight='bold', fontsize=18)
        ax.text(0.5, 0.9, u'Ind (\u2212)',
            verticalalignment='bottom', horizontalalignment='center',
            family='Times New Roman', weight='bold', fontsize=18)
        ax.text(0.0, -0.15, u'Disp (\u2212)',
            verticalalignment='bottom', horizontalalignment='center',
            family='Times New Roman', weight='bold', fontsize=18)
        ax.text(-0.5, 0.9, u'Elst (+)',
            verticalalignment='bottom', horizontalalignment='center',
            family='Times New Roman', weight='bold', fontsize=18)

    xvals = []
    yvals = []
    cvals = []
    for sys in sapt:
        [elst, indc, disp] = sys

        # calc ternary posn and color
        Ftop = abs(indc) / (abs(elst) + abs(indc) + abs(disp))
        Fright = abs(elst) / (abs(elst) + abs(indc) + abs(disp))
        xdot = 0.5 * Ftop + Fright
        ydot = 0.866 * Ftop
        cdot = 0.5 + (xdot - 0.5) / (1. - Ftop)
        if elst > 0.:
            xdot = 0.5 * (Ftop - Fright)
            ydot = 0.866 * (Ftop + Fright)
        #print elst, indc, disp, '', xdot, ydot, cdot

        xvals.append(xdot)
        yvals.append(ydot)
        cvals.append(cdot)

    sc = ax.scatter(xvals, yvals, c=cvals, s=25, marker="o", \
        cmap=mpl.cm.jet, edgecolor='none', vmin=0, vmax=1, zorder=10)

    # remove figure outline
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # save and show
    pltuid = title + '_' + ('lbld' if labeled else 'bare') + '_' + hashlib.sha1(title + repr(sapt)).hexdigest()
    pltfile = 'tern_'
    files_saved = {}
    for ext in graphicsformat:
        savefile = pltfile + '.' + ext.lower()
        plt.savefig(savefile, transparent=True, format=ext, bbox_inches='tight',
                    frameon=False, dpi=450, edgecolor='none', pad_inches=0.0)
        files_saved[ext.lower()] = savefile
    if view:
        plt.show()
    plt.close()
    return files_saved

