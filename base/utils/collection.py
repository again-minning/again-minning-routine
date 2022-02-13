from collections import defaultdict


def to_dict(items: list, to_key):
    res = defaultdict(list)
    for item in items:
        key = get_attr(item, to_key)
        if key is None:
            raise ValueError('존재하지 않는 key 값입니다.')
        res[key].append(item)
    return res


def get_attr(item, to_key):
    if isinstance(item, dict):
        return item.get(to_key)
    else:
        return getattr(item, to_key)
