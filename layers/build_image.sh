docker build -t ask-runtime:latest -f layers/Dockerfile .

# to create a writable layer for testing
docker run --name layer-container -it ask-runtime:latest

