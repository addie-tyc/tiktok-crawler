def convert_str_to_number(s: str) -> int:
    num_map = {'K':1000, 'M':1000000, 'B':1000000000}
    if s.isdigit():
        return int(s)
    else:
        if len(s) > 1:
            return int(float(s[:-1]) * num_map.get(s[-1].upper(), 1))
    raise Exception('the input value is not valid.')
