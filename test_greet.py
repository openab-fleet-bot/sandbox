import pytest

from greet import greet


class TestGreetHappyPath:
    def test_simple_name(self):
        assert greet("Ada") == "Hello, Ada!"

    def test_strips_leading_and_trailing_whitespace(self):
        assert greet("  Ada  ") == "Hello, Ada!"

    def test_strips_leading_and_trailing_tabs_and_newlines(self):
        assert greet("\t\nAda\n\t") == "Hello, Ada!"

    def test_preserves_internal_whitespace(self):
        assert greet("  Ada  Lovelace  ") == "Hello, Ada  Lovelace!"

    def test_single_character_name(self):
        assert greet("A") == "Hello, A!"

    def test_unicode_name(self):
        assert greet("Adaレース") == "Hello, Adaレース!"

    def test_name_with_punctuation(self):
        assert greet("O'Brien-Smith") == "Hello, O'Brien-Smith!"

    def test_strips_unicode_whitespace_like_nbsp_and_em_space(self):
        # Python's str.strip() removes any character where str.isspace() is
        # True, which includes non-breaking space (\xa0) and em space
        # ( ), not just ASCII whitespace.
        assert greet("\xa0Ada ") == "Hello, Ada!"

    def test_very_long_name(self):
        long_name = "A" * 100_000
        assert greet(long_name) == f"Hello, {long_name}!"

    def test_str_subclass_is_accepted(self):
        class MyStr(str):
            pass

        assert greet(MyStr("Ada")) == "Hello, Ada!"

    def test_name_of_non_whitespace_control_character_is_kept(self):
        # A null byte is not whitespace, so it should survive stripping and
        # count as non-empty content rather than raising ValueError.
        assert greet("\x00") == "Hello, \x00!"


class TestGreetInvalidType:
    @pytest.mark.parametrize(
        "bad_value",
        [None, 123, 3.14, [], {}, (), set(), True, False, b"Ada", object()],
        ids=[
            "none",
            "int",
            "float",
            "empty_list",
            "empty_dict",
            "empty_tuple",
            "empty_set",
            "bool_true",
            "bool_false",
            "bytes",
            "plain_object",
        ],
    )
    def test_raises_value_error_for_non_string_input(self, bad_value):
        with pytest.raises(ValueError):
            greet(bad_value)


class TestGreetEmptyOrWhitespaceOnly:
    @pytest.mark.parametrize(
        "bad_value",
        [
            "",
            " ",
            "\t",
            "\n",
            "   \t\n  ",
            "\xa0",
            " ",
            "\xa0\t\n ",
        ],
        ids=[
            "empty_string",
            "single_space",
            "tab",
            "newline",
            "mixed_ascii_whitespace",
            "nbsp_only",
            "em_space_only",
            "mixed_unicode_whitespace",
        ],
    )
    def test_raises_value_error_for_empty_or_whitespace_only(self, bad_value):
        with pytest.raises(ValueError):
            greet(bad_value)

    def test_raised_error_is_exactly_value_error_type(self):
        # Guards against a future change that swaps ValueError for a
        # broader/narrower exception type without updating callers.
        with pytest.raises(ValueError) as exc_info:
            greet("   ")
        assert type(exc_info.value) is ValueError
