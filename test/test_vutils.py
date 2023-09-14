# tests verb utilities

import pytest
import src.verb_utils as vutils

def test_hello():
    print("hello world! :)")
    assert 493 == 493

def test_goodbye():
    print("goodbye world! :(")
    assert 493 == 493