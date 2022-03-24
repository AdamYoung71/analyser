FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        bison \
        build-essential \
        clang \
        cmake \
        doxygen \
        flex \
        g++ \
        git \
        libffi-dev \
        libncurses5-dev \
        libsqlite3-dev \
        make \
        mcpp \
        python \
        sqlite3 \
        zlib1g-dev \
        wget \
        unzip \
        lsb-release \
        python3-pip \
        graphviz

RUN wget https://github.com/souffle-lang/souffle/archive/refs/tags/2.1.zip \
    && unzip 2.1.zip \
    && cd souffle-2.1 \
    && cmake -S . -B build -DCMAKE_INSTALL_PREFIX=/usr \
    && cmake --build build --target install

RUN mkdir -p /comp0174

COPY requirements.txt /comp0174

RUN python3 -m pip install -r /comp0174/requirements.txt

COPY analyse.py /comp0174/analyse.py

COPY analyses /comp0174/analyses

COPY examples /comp0174/examples

WORKDIR /comp0174/
