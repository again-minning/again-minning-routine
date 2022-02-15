from assertpy import assert_that

from base.utils.collection import to_dict


def test_to_dict():
    items = []
    for i in range(5):
        items.append({
            'id': i+1,
            'value': f'value{i+1}'
        })
    items.append({
        'id': 5,
        'value': f'value{5}'
    })
    hash_maps = to_dict(items=items, to_key='id')
    for i in range(4):
        assert_that(len(hash_maps[i+1])).is_equal_to(1)
    assert_that(len(hash_maps[5])).is_equal_to(2)


def test_to_dict_invalid_key():
    items = []
    for i in range(5):
        items.append({
            'id': i+1,
            'value': f'value{i+1}'
        })
    items.append({
        'id': 5,
        'value': f'value{5}'
    })
    assert_that(to_dict).raises(ValueError).when_called_with(items, 'error_id')
