import csv


def load_data(path):
    """
    Loads csv file form path and returns it as python dict for fast access.
    """
    data = {}
    with open(path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: continue
            try: data[row[0]] = tuple(map(float, row[1:]))
            except ValueError: print(f"Pominięto wiersz z błędem danych: {row}"); continue
    return data


def get_item_as_tuple_by_reference(data, ref):
    """
    Tries to get item info from given dict and returns item as tuple. Ready to pass to packing_utils._normalized_item().
    """
    item_dims = data.get(ref, None)
    if not item_dims: return None
    return (ref, *item_dims)
