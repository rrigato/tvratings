docker build -t ask-runtime:latest -f layers/Dockerfile .

docker run --name layer-container -it ask-runtime:latest


docker rm