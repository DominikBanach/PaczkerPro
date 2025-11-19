from py3dbp import Packer, Bin, Item
from config import PARCEL_SIZES


def _normalized_item(name, w, h, d, weight):
    """
    Calls py3dbp.Item constructor using sorted dimensions.
    """
    sorted_dims = sorted([w, h, d], reverse=True)
    return Item(name, *sorted_dims, weight)


def _tuples_to_items(items):
    """
    Returns list of Items based on list of tuples defining them.
    """
    
    return [_normalized_item(*item) for item in items]


def _get_empty_bin(size):
    """
    Returns an empty bin of given size, where size is key from config.PARCEL_SIZES dictionary.
    """

    if size not in PARCEL_SIZES.keys():
        return None
    
    return Bin(*PARCEL_SIZES.get(size))


def _get_bins_list():
    """
    Returns a list (sorted by width) containing empty bins of all sizes (one for each size) defined in config.PARCEL_SIZES dictionary.
    """

    return [_get_empty_bin(size) for size in sorted(PARCEL_SIZES.keys(), key = lambda x: PARCEL_SIZES[x][1])]


def _try_packing(bin, items):
    """
    Tries packing given list of items into single given bin and returns success (True/False) and used packer object.
    """

    packer = Packer()
    packer.add_bin(bin)

    for item in items: 
        packer.add_item(item)

    packer.pack()

    success = len(packer.bins[0].unfitted_items) == 0

    return success, packer


def _try_packing_into_all_possible_bins(items):
    """
    Tries packing given list of items into all possible bins and return list of tuples (success, packer)
    """
    return [_try_packing(bin, _tuples_to_items(items)) for bin in _get_bins_list()]


def describe_packability(items):
    """
    Returns string describing given items list packability for all avaliable parcel sizes.
    """

    results = _try_packing_into_all_possible_bins(items)

    if not results:
        return ""
    
    description = "Possible packings:"
    for success, packer in results:

        description += "\n"

        bin = packer.bins[0]
        unfitted_items = bin.unfitted_items
        unfitted_items_count = len(unfitted_items)
        bin_name = bin.name
        success_icon = '❌' if unfitted_items_count else '✅'

        description += f"{success_icon} | {bin_name}"

        if not success: 
            description += f" ({unfitted_items_count} left)\n"
            for item in unfitted_items:
                description += f"\t- {item.name}\n"

        else:  
            description += "\n"
    
    return description
