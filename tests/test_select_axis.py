import pandas as pd
import pytest


from pandas_selector.axis import C, OpComposerBase


def cols(df: pd.DataFrame, col_sel: OpComposerBase) -> list:
    """Get list of column names after applying column selection."""
    return df.loc[:, col_sel].columns.to_list()


@pytest.fixture
def simple_df():
    return pd.DataFrame(
        {
            "x": range(5),
            "y": range(5),
            "z": list("abcde"),
            "u": 1.0,
        }
    )


@pytest.fixture
def mi_df():
    return pd.DataFrame(
        columns=pd.MultiIndex.from_product(
            [list("abc"), list("XYZ")],
            names=["one", "two"],
        )
    )


def test_basic(simple_df):
    col_sel = C["y", "z", "x"]
    assert cols(simple_df, col_sel) == ["y", "z", "x"]


def test_combine(simple_df):
    col_sel = C["y"] | C["z"] | C["x"]
    assert cols(simple_df, col_sel) == ["y", "z", "x"]


def test_ellipsis(simple_df):
    col_sel = C["y"] | ...
    assert cols(simple_df, col_sel) == ["y", "x", "z", "u"]


def test_startswith(simple_df):
    col_sel = C.startswith("x")
    assert cols(simple_df, col_sel) == ["x"]


def test_endswith(simple_df):
    col_sel = C.endswith("x")
    assert cols(simple_df, col_sel) == ["x"]


def test_str_dtype(simple_df):
    col_sel = C.dtype == str
    assert cols(simple_df, col_sel) == ["z"]


def test_int_dtype(simple_df):
    col_sel = C.dtype == int
    assert cols(simple_df, col_sel) == ["x", "y"]


def test_dtype_isin(simple_df):
    col_sel = C.dtype.isin((str, float))
    assert cols(simple_df, col_sel) == ["z", "u"]


def test_level0_subset(mi_df):
    expected = [
        ("c", "X"),
        ("c", "Y"),
        ("c", "Z"),
        ("a", "X"),
        ("a", "Y"),
        ("a", "Z"),
    ]

    col_sel = C.levels[0]["c", "a"]
    assert cols(mi_df, col_sel) == expected

    col_sel = C.levels["one"]["c", "a"]
    assert cols(mi_df, col_sel) == expected


def test_level0_str_methods(mi_df):
    expected = [
        ("c", "X"),
        ("c", "Y"),
        ("c", "Z"),
    ]

    col_sel = C.levels[0].startswith("c")
    assert cols(mi_df, col_sel) == expected

    col_sel = C.levels[0].endswith("c")
    assert cols(mi_df, col_sel) == expected

    col_sel = C.levels[0].contains("c")
    assert cols(mi_df, col_sel) == expected

    col_sel = C.levels[0].match("c")
    assert cols(mi_df, col_sel) == expected


def test_level0_composition(mi_df):
    expected = [
        ("c", "X"),
        ("c", "Y"),
        ("c", "Z"),
        ("a", "X"),
        ("a", "Y"),
        ("a", "Z"),
        ("b", "X"),
        ("b", "Y"),
        ("b", "Z"),
    ]
    col_sel = C.levels[0]['c'] | ...
    assert cols(mi_df, col_sel) == expected
