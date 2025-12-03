from py3dbp import Bin
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def visualize_bin(bin : Bin):
    """
    Shows 3D visualization for given bin
    """

    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(projection="3d")
    fig.canvas.manager.set_window_title("PaczkerPro - 3D visualization")
    ax.set_title(f"Visualization of {len(bin.items)} items packed into {bin.name}")

    colormap = plt.get_cmap('tab10')

    w, h, d = map(float, (bin.width, bin.height, bin.depth))
    max_dim = max(w, h, d)
    ax.set_box_aspect((w/max_dim, h/max_dim, d/max_dim))

    # Bin contour
    ax.plot((0, w, w, 0, 0), (0, 0, h, h, 0), (0, 0, 0, 0, 0), color='black', linewidth=3)
    ax.plot((0, w, w, 0, 0), (0, 0, h, h, 0), (d, d, d, d, d), color='black', linewidth=3)
    ax.plot((0, 0), (0, 0), (0, d), color='black', linewidth=3)
    ax.plot((w, w), (0, 0), (0, d), color='black', linewidth=3)
    ax.plot((w, w), (h, h), (0, d), color='black', linewidth=3)
    ax.plot((0, 0), (h, h), (0, d), color='black', linewidth=3)

    # Items as 3d bars
    for i, item in enumerate(bin.items):        
        ax.bar3d(*map(float, item.position), 
                 *map(float, item.get_dimension()), 
                 color=colormap(i % 10), alpha=0.5, edgecolor='k', linewidth=1.5)

    ax.set_xlabel('Width (X)')
    ax.set_ylabel('Height (Y)')
    ax.set_zlabel('Depth (Z)')

    locator = MaxNLocator(nbins=10, integer=True)
    
    ax.xaxis.set_major_locator(locator)
    ax.yaxis.set_major_locator(locator)
    ax.zaxis.set_major_locator(locator)

    ax.tick_params(axis='both', which='major', labelsize=8, pad=2)

    plt.show()
