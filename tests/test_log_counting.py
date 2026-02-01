import os
import sys

# Add project root (the folder that contains log_counting.py) to sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from log_counting import count_requests_per_user, get_top_users, parse_log_line


def test_parse_valid_line():
    line = "2025-11-28T10:01:12Z alice GET /api/items 200"
    result = parse_log_line(line)

    assert result == (
        "2025-11-28T10:01:12Z",
        "alice",
        "GET",
        "/api/items",
        "200",
    )


def test_parse_invalid_line():
    line = "INVALID LINE"
    assert parse_log_line(line) is None


def test_count_requests():
    lines = [
        ("t", "alice", "GET", "/", "200"),
        ("t", "bob", "GET", "/", "200"),
        ("t", "alice", "GET", "/", "200"),
    ]
    counts = count_requests_per_user(lines)
    assert counts == {"alice": 2, "bob": 1}


def test_get_top_users():
    counts = {"alice": 6, "bob": 4, "charlie": 2}
    result = get_top_users(counts, n=2)
    assert result == [("alice", 6), ("bob", 4)]
