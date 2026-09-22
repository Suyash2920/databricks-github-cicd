from src.transformations import calculate_total, transform_data


def test_transform_data():

    input_data = [1, 2, 3, 4]

    expected = [2, 4, 6, 8]

    assert transform_data(input_data) == expected


def test_calculate_total():

    input_data = [10, 20, 30]

    assert calculate_total(input_data) == 60


def test_empty_data():

    assert transform_data([]) == []


def test_empty_total():

    assert calculate_total([]) == 0
