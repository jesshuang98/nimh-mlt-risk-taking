## visualize weights

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
import seaborn as sns
import csv

# https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, orientation= "horizontal", ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=0, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=["black", "white"],
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A list or array of two color specifications.  The first is used for
        values below a threshold, the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts




LAMBDA = 10.0


ET1 = "random"
ET2 = "1block"

wnames = np.load('x_random_normed_standardized_Actual_EV0.5_interactions_names.npy')
w1 = np.load(ET1 +"_lambda" + str(LAMBDA) + "_weights.npy")
w2 = np.load(ET2 +"_lambda" + str(LAMBDA) + "_weights.npy")

print w1
print w2

wm = [np.maximum(np.absolute(i),np.absolute(j)) for i,j in zip(w1,w2)]
print wm

print wnames[:10]

print sorted(zip(wm,w1), reverse=True)

w1 = [x for _,x in sorted(zip(wm,w1), reverse=True)]
w2 = [x for _,x in sorted(zip(wm,w2), reverse=True)]
wnames = [x for _,x in sorted(zip(wm,wnames), reverse=True)]



NFEATS = 10
print wnames[:NFEATS]

with open('names.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    for i in range(NFEATS):
        writer.writerow([wnames[i]])


matrix = np.transpose(np.array([w1[:NFEATS], w2[:NFEATS]]))

cmap = sns.diverging_palette(250, 10, as_cmap=True)
ax = sns.heatmap(matrix, center=0, annot=True, fmt=".1f",
                yticklabels=wnames[:NFEATS], xticklabels=[ET1, ET2], cmap=cmap)
plt.show()


# fig, ax = plt.subplots()

# im, cbar = heatmap(matrix, [ET1, ET2], wnames, ax=ax,
#                    cmap="bwr")
#                    # , cbarlabel="some title for the color legend")
# texts = annotate_heatmap(im, valfmt="{x:.1f}")

# fig.tight_layout()
# plt.show()
