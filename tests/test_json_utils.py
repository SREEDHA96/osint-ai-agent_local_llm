import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from backend.utils.json_utils import extract_json


def test_basic_json():
    assert extract_json('{"a": 1}') == {"a": 1}


def test_prefix_result():
    assert extract_json('Result: {"a": 2}') == {"a": 2}


def test_code_fence():
    text = '```json\n{"a":3}\n```'
    assert extract_json(text) == {"a": 3}


def test_trailing_fence():
    text = '{"a":4}\n```'
    assert extract_json(text) == {"a": 4}


def test_required_keys_missing():
    with pytest.raises(ValueError):
        extract_json('{"a":5}', required_keys=['b'])

