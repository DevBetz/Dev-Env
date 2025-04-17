FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    git curl nano \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Optional aliases or tooling
RUN echo "alias python=python3" >> ~/.bashrc
