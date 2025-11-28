from py3dbp import Bin, Item, Packer
import matplotlib.pyplot as plt

def visualize_bin(bin : Bin):
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    colormap = plt.get_cmap('tab10')
    w, h, d = map(float, (bin.width, bin.height, bin.depth))

    max_dim = max(w, h, d)
    ax.set_box_aspect((w/max_dim, h/max_dim, d/max_dim))

    # Bin contour
    ax.plot((0, w, w, 0, 0), (0, 0, h, h, 0), (0, 0, 0, 0, 0), color='black')
    ax.plot((0, w, w, 0, 0), (0, 0, h, h, 0), (d, d, d, d, d), color='black')
    ax.plot((0, 0), (0, 0), (0, d), color='black')
    ax.plot((w, w), (0, 0), (0, d), color='black')
    ax.plot((w, w), (h, h), (0, d), color='black')
    ax.plot((0, 0), (h, h), (0, d), color='black')

    # Items as 3d bars
    for i, item in enumerate(bin.items):        
        ax.bar3d(*map(float, item.position), 
                 *map(float, item.get_dimension()), 
                 color=colormap(i % 10), alpha=0.5, edgecolor='k', linewidth=1.5)

    ax.set_xlabel('Width (X)')
    ax.set_ylabel('Height (Y)')
    ax.set_zlabel('Depth (Z)')

    plt.show()


if __name__ == "__main__":
    packer = Packer()
    packer.add_bin(Bin("InPost/B", 19, 38, 64, 25))
    packer.add_item(Item('Item 1', 25, 25, 10, 1)) 
    packer.add_item(Item('Item 2', 10, 7, 10, 1))
    packer.add_item(Item('Item 3', 10, 8, 2, 1))
    packer.add_item(Item('Item 4', 10, 10, 10, 1))
    packer.pack()

    for b in packer.bins:
        print("Box:", b.name)
        print("Items:")
        for item in b.items:
            print(f" - {item.name} on cords {item.position}")
            
        visualize_bin(b)