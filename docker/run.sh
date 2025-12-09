
isRunning=`docker ps -f name=openduck | grep -c "openduck"`;

if [ $isRunning -eq 0 ]; then
    xhost +local:docker
    docker rm openduck
    docker run  \
        --gpus all \
        --device /dev/dri \
        --name openduck  \
        --env DISPLAY=$DISPLAY \
        --env NVIDIA_DRIVER_CAPABILITIES=all \
        --env QTWEBENGINE_DISABLE_SANDBOX=1 \
        --env QT_X11_NO_MITSHM=1 \
        --net host \
        --ipc host \
        --pid host \
        --privileged \
        -it \
        -v /dev:/dev \
        -v `pwd`/../:/ros2_ws/src/openduck \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -v /run/dbus:/run/dbus \
        -w /ros2_ws \
        openduck:latest

else
    echo "Docker already running."
    docker exec -it openduck /bin/bash
fi