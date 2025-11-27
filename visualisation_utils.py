from py3dbp import Bin, Item
import matplotlib.pyplot as plt

def visualize_bin(bin : Bin):
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    