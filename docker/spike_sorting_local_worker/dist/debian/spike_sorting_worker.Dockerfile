ARG PY_VER
ARG WORKER_BASE_HASH
FROM datajoint/djbase:py${PY_VER}-debian-${WORKER_BASE_HASH}

USER root
## system level dependencies
RUN apt-get update
COPY ../../apt_requirements.txt /tmp/apt_requirements.txt
RUN xargs apt-get install -y < /tmp/apt_requirements.txt
RUN xargs apt-get install -y unzip git

## NVIDIA driver is managed by nvidia-container-toolkit and nvidia-docker-2
## https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#setting-up-nvidia-container-toolkit

## Downgrade gcc/g++ for cuda
RUN apt-get install -y gcc-9 g++-9 && \
   rm /usr/bin/gcc && \
   rm /usr/bin/g++ && \
   ln -s /usr/bin/gcc-9 /usr/bin/gcc && \
   ln -s /usr/bin/g++-9 /usr/bin/g++

## CUDA Toolkit
RUN wget -P /tmp/ http://developer.download.nvidia.com/compute/cuda/11.0.2/local_installers/cuda_11.0.2_450.51.05_linux.run
RUN cd /tmp && bash cuda*.run --silent --toolkit
ENV PATH /usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/cuda-11.0/lib64:${LD_LIBRARY_PATH}
ENV CUDA_CACHE_MAXSIZE 1073741824

## Fix: libcrypto.so.1.1: version `OPENSSL_1_1_1' not found
WORKDIR /tmp
RUN wget https://www.openssl.org/source/openssl-1.1.1g.tar.gz
RUN tar -zxf openssl-1.1.1g.tar.gz
WORKDIR /tmp/openssl-1.1.1g
RUN ./config && make && make install
RUN mv /usr/bin/openssl /tmp/ && ln -s /usr/local/bin/openssl /usr/bin/openssl
ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH}
RUN rm /usr/lib/x86_64-linux-gnu/libcrypto.so.1.1

USER anaconda
WORKDIR $HOME

ARG DEPLOY_KEY
COPY --chown=anaconda $DEPLOY_KEY $HOME/.ssh/id_ed25519
RUN chmod u=r,g-rwx,o-rwx $HOME/.ssh/id_ed25519 && \
   ssh-keyscan github.com >> $HOME/.ssh/known_hosts

ENV SSL_CERT_DIR=/etc/ssl/certs
ARG REPO_OWNER
ARG REPO_NAME
ARG REPO_BRANCH
RUN git clone -b ${REPO_BRANCH} git@github.com:${REPO_OWNER}/${REPO_NAME}.git && \
   pip install --upgrade pip && \
   pip install ./${REPO_NAME}