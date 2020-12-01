from rest_api.utils.parsers import OptFields, _SubTree


def opt_fields_parser_test():
    parsed = OptFields("abcd, asd[1,2,3]{ hgh[]{lkj}, kjk[2,3,ads] }")

    assert parsed.fields == {
        "abcd": _SubTree(),
        "asd": _SubTree(
            ["1", "2", "3"],
            {
                "hgh": _SubTree([], {"lkj": _SubTree()}),
                "kjk": _SubTree(["2", "3", "ads"]),
            },
        ),
    }
