def norm(x, _min, _max):
    return (x - _min) / (_max - _min)

def lerp(x, _min, _max):
    return (_max - _min) * x + _min

def map(x, source_min, source_max, dest_min, dest_max):
    return lerp(norm(x, source_min, source_max), dest_min, dest_max)

def clamp(x, min_val, max_val):
    return min(max(x, min_val), max_val)
