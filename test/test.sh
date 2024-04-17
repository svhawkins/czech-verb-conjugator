#!/bin/bash
# script to run the tests and keep you in the same directory where you called this script.

old_dir=`pwd`
cd $BASE_DIR/test
pytest test_vutils.py test_verbs.py test_conjutils.py test_conjugator.py
cd $old_dir