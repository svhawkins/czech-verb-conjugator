# set up directory basename
export BASE_DIR=

# export subdirectories
export PYTHON_PATH=$PYTHON_PATH:$BASE_DIR"/src"
export PYTHON_PATH=$PYTHON_PATH:$BASE_DIR"/data"
export PYTHON_PATH=$PYTHON_PATH:$BASE_DIR"/test"

# alias for test command(s)
alias tests=". $BASE_DIR/test.sh"