export BUILT_LAYER_NAME="ask_sdk_core_1_19_0.zip"
export CONTAINER_NAME="lambda-container"
export IMAGE_NAME="lambda-dependency"


docker build --build-arg BUILT_LAYER_NAME=$BUILT_LAYER_NAME \
    -t $IMAGE_NAME:latest -f layers/Dockerfile .

# to create a writable layer for testing
# docker run --name $CONTAINER_NAME -it $IMAGE_NAME:latest

#create a container in detached mode and copy lambda layer zip
docker run -i -d --name $CONTAINER_NAME $IMAGE_NAME:latest

docker cp $CONTAINER_NAME:/$BUILT_LAYER_NAME layers

#remove container
docker rm -f $CONTAINER_NAME