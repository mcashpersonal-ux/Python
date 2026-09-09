#!/usr/bin/env python3
import pathlib
pairs = {
"docs/basics/005-collections.md": [
    ("b = {2,  \uf8cf3,  \uf8cf4}", "b = {2,3,4}"),
    ("original = [[1,  2], [3,   \uf8cf4]]", "original = [[1,2],[3,4]]"),
],
}