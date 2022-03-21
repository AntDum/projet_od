def tokenizer(filename : str, tokens : dict):
    """Yield every tile with x y and the token

    Args:
        filename (str): Name of a file
        tokens (dict): Dict of convertion

    Yields:
        tuple (x, y, token): coord and token
    """
    with open(filename, 'r') as f:
        raws = [[line.strip().split(',')] for line in f]
    
    for y, line in enumerate(raws):
        for x, t in enumerate(line):
            yield x, y, tokens.get(t, None)