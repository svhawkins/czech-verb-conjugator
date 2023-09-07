# tests verb utilities

import sys, os
sys.path.insert(0, os.getenv("BASE_DIR") + "\\src")
import src.verb_utils as vutils

import pytest
def test_hello():
    assert 493 == 493
    print("hello world! :)")

def test_goodbye():
    assert 493 != 493
    print("goodbye world! :(")