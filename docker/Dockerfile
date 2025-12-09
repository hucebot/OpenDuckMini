FROM nvidia/opengl:1.2-glvnd-devel-ubuntu22.04
LABEL maintainer="clemente.donosok@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Europe/Paris \
    ROS_DISTRO=humble \
    DISPLAY=:0 \
    LIBGL_ALWAYS_INDIRECT=0

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get upgrade -yy

##### Install dependencies for the base system
RUN apt-get install -y \
    curl \
    gnupg2 \
    lsb-release


###### Install Python Dependencies
RUN apt-get install -y \
    python-is-python3 \
    python3-pip

##### Install ROS 2 Humble
RUN export ROS_APT_SRC_VER=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}') && \
    curl -L -o /tmp/ros2-apt-source.deb \
      "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SRC_VER}/ros2-apt-source_${ROS_APT_SRC_VER}.$(. /etc/os-release && echo $VERSION_CODENAME)_all.deb" && \
    dpkg -i /tmp/ros2-apt-source.deb && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
      ros-${ROS_DISTRO}-desktop-full \
      ros-dev-tools \
      ros-${ROS_DISTRO}-cv-bridge \
      ros-${ROS_DISTRO}-rviz2 \
      ros-${ROS_DISTRO}-rviz-imu-plugin && \
    rosdep init && \
    rosdep update && \
    rm -rf /var/lib/apt/lists/* /tmp/ros2-apt-source.deb

RUN echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> /etc/bash.bashrc

##### Install Open Duck Runtime
WORKDIR /
RUN git clone https://github.com/apirrone/Open_Duck_Mini_Runtime
WORKDIR /Open_Duck_Mini_Runtime
RUN pip install -e .
