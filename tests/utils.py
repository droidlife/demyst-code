# pylint: disable=too-few-public-methods, invalid-name
import math
from functools import reduce
from itertools import zip_longest

from prettytable import PrettyTable
from pyspark import Row
from pyspark.sql import DataFrame


class SchemasNotEqualError(Exception):
    """The schemas are not equal"""

    pass


class BColors:
    NC = "\033[0m"  # No Color, reset all
    Bold = "\033[1m"
    Underlined = "\033[4m"
    Blink = "\033[5m"
    Inverted = "\033[7m"
    Hidden = "\033[8m"
    Black = "\033[30m"
    Red = "\033[31m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Purple = "\033[35m"
    Cyan = "\033[36m"
    LightGray = "\033[37m"
    DarkGray = "\033[30m"
    LightRed = "\033[31m"
    LightGreen = "\033[32m"
    LightYellow = "\033[93m"
    LightBlue = "\033[34m"
    LightPurple = "\033[35m"
    LightCyan = "\033[36m"
    White = "\033[97m"


def blue(s: str) -> str:
    return BColors.LightBlue + str(s) + BColors.LightRed


def isnan(x):
    try:
        return math.isnan(x)
    except TypeError:
        return False


def nan_safe_equality(x, y) -> bool:
    return (x == y) or (isnan(x) and isnan(y))


def are_rows_equal(r1: Row, r2: Row) -> bool:
    return r1 == r2


def are_rows_equal_enhanced(r1: Row, r2: Row, allow_nan_equality: bool) -> bool:
    if r1 is None and r2 is None:
        return True
    if (r1 is None and r2 is not None) or (r2 is None and r1 is not None):
        return False
    d1 = r1.asDict()
    d2 = r2.asDict()
    if allow_nan_equality:
        for key in d1.keys() & d2.keys():
            if not nan_safe_equality(d1[key], d2[key]):
                return False
        return True

    return r1 == r2


def are_rows_approx_equal(r1: Row, r2: Row, precision: float) -> bool:
    if r1 is None and r2 is None:
        return True
    if (r1 is None and r2 is not None) or (r2 is None and r1 is not None):
        return False
    d1 = r1.asDict()
    d2 = r2.asDict()
    all_equal = True
    for key in d1.keys() & d2.keys():
        if isinstance(d1[key], float) and isinstance(d2[key], float):
            if abs(d1[key] - d2[key]) > precision:
                all_equal = False
        elif d1[key] != d2[key]:
            all_equal = False
    return all_equal


def are_structfields_equal(sf1, sf2, ignore_nullability=False):
    if ignore_nullability:
        if sf1 is None and sf2 is not None:
            return False
        if sf1 is not None and sf2 is None:
            return False
        if sf1.name != sf2.name or sf1.dataType != sf2.dataType:
            return False

        return True

    return sf1 == sf2


def assert_schema_equality(s1, s2, ignore_nullable=False):
    if ignore_nullable:
        assert_schema_equality_ignore_nullable(s1, s2)
    else:
        assert_basic_schema_equality(s1, s2)


def assert_basic_schema_equality(s1, s2):
    if s1 != s2:
        t = PrettyTable(["Expected Schema", "Actual Schema"])
        zipped = list(zip_longest(s1, s2))
        for sf1, sf2 in zipped:
            if sf1 == sf2:
                t.add_row([blue(sf1), blue(sf2)])
            else:
                t.add_row([sf1, sf2])
        raise SchemasNotEqualError("\n" + t.get_string())


def assert_schema_equality_ignore_nullable(s1, s2):
    if not are_schemas_equal_ignore_nullable(s1, s2):
        t = PrettyTable(["Expected Schema", "Actual Schema"])
        zipped = list(zip_longest(s1, s2))
        for sf1, sf2 in zipped:
            if are_structfields_equal(sf1, sf2, True):
                t.add_row([blue(sf1), blue(sf2)])
            else:
                t.add_row([sf1, sf2])
        raise SchemasNotEqualError("\n" + t.get_string())


def are_schemas_equal_ignore_nullable(s1, s2):
    if len(s1) != len(s2):
        return False
    zipped = list(zip_longest(s1, s2))
    for sf1, sf2 in zipped:
        names_equal = sf1.name == sf2.name
        types_equal = check_type_equal_ignore_nullable(sf1, sf2)
        if not names_equal or not types_equal:
            return False
    return True


def check_type_equal_ignore_nullable(sf1, sf2):
    """Checks StructField data types ignoring nullables.
    Handles array element types also.
    """
    dt1, dt2 = sf1.dataType, sf2.dataType
    if dt1.typeName() == dt2.typeName():
        # Account for array types by inspecting elementType.
        if dt1.typeName() == "array":
            return dt1.elementType == dt2.elementType

        return True

    return False


def assert_equal_row_counts(df1, df2):
    if df1.count() != df2.count():
        raise RowCountNotEqualError


def are_dfs_equal(df1, df2):
    if df1.schema != df2.schema:
        return False
    if df1.collect() != df2.collect():
        return False
    return True


def assert_approx_df_equality(
    expected: DataFrame,
    actual: DataFrame,
    precision: float,
    transforms=None,
    ignore_column_order=True,
    ignore_row_order=True,
    ignore_nullable=False,
):
    if transforms is None:
        transforms = []
    if ignore_column_order:
        transforms.append(lambda df: df.select(sorted(df.columns)))
    if ignore_row_order:
        transforms.append(lambda df: df.sort(df.columns))
    expected = reduce(lambda acc, fn: fn(acc), transforms, expected)
    actual = reduce(lambda acc, fn: fn(acc), transforms, actual)

    assert_schema_equality(expected.schema, actual.schema, ignore_nullable)
    assert_generic_rows_equality(expected, actual, are_rows_approx_equal, [precision])


def assert_generic_rows_equality(df1, df2, row_equality_fun, row_equality_fun_args):
    df1_rows = df1.collect()
    df2_rows = df2.collect()
    zipped = list(zip_longest(df1_rows, df2_rows))
    t = PrettyTable(["Expected", "Actual"])
    all_rows_equal = True
    for r1, r2 in zipped:
        # rows are not equal when one is None and the other isn't
        if (r1 is not None and r2 is None) or (r2 is not None and r1 is None):
            all_rows_equal = False
            t.add_row([r1, r2])
        # rows are equal
        elif row_equality_fun(r1, r2, *row_equality_fun_args):
            first = BColors.LightBlue + str(r1) + BColors.LightRed
            second = BColors.LightBlue + str(r2) + BColors.LightRed
            t.add_row([first, second])
        # otherwise, rows aren't equal
        else:
            all_rows_equal = False
            t.add_row([r1, r2])
    if not all_rows_equal:
        raise DataFramesNotEqualError("\n" + t.get_string())


def assert_basic_rows_equality(df1, df2):
    rows1 = df1.collect()
    rows2 = df2.collect()
    if rows1 != rows2:
        t = PrettyTable(["Expected", "Actual"])
        zipped = list(zip_longest(rows1, rows2))
        for r1, r2 in zipped:
            if r1 == r2:
                t.add_row([blue(r1), blue(r2)])
            else:
                t.add_row([r1, r2])
        raise DataFramesNotEqualError("\n" + t.get_string())


def assert_df_equality(
    expected: DataFrame,
    actual: DataFrame,
    ignore_nullable=True,
    transforms=None,
    allow_nan_equality=False,
    ignore_column_order=True,
    ignore_row_order=True,
):
    if transforms is None:
        transforms = []
    if ignore_column_order:
        transforms.append(lambda df: df.select(sorted(df.columns)))
    if ignore_row_order:
        transforms.append(lambda df: df.sort(df.columns))
    expected = reduce(lambda acc, fn: fn(acc), transforms, expected)
    actual = reduce(lambda acc, fn: fn(acc), transforms, actual)
    assert_schema_equality(expected.schema, actual.schema, ignore_nullable)
    if allow_nan_equality:
        assert_generic_rows_equality(expected, actual, are_rows_equal_enhanced, [True])
    else:
        assert_basic_rows_equality(expected, actual)
