# ---- Base Image ----
FROM nvidia/cuda:12.6.3-cudnn-runtime-ubuntu24.04 AS base

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/opt/conda/bin:$PATH

# ---- System Setup ----
RUN apt-get update && \
    apt-get install -y wget git curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# ---- Install Miniconda ----
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh && \
    /opt/conda/bin/conda clean -afy

# ---- Set Workdir ----
WORKDIR /workspace

# ---- Create Conda Env ----
ARG ENV_FILE=environment.gpu.yml
# Copy only the environment file
COPY $ENV_FILE /workspace/
RUN conda update -n base -c defaults conda && \
    conda env create -f $ENV_FILE && \
    echo "conda activate traveller-gpu" >> ~/.bashrc && \
    rm $ENV_FILE

# Set environment name
ARG ENV_NAME=traveller-gpu
SHELL ["conda", "run", "-n", "traveller-gpu", "/bin/bash", "-c"]

# ---- Create non-root user ----
RUN useradd -m appuser && \
    chown -R appuser:appuser /workspace
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# ---- Default to bash for interactive use ----
CMD ["/bin/bash"]