FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    python3 \
    python3-pip \
    wget \
    openssh-server \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz -O /tmp/hadoop.tar.gz \
    && tar -xzf /tmp/hadoop.tar.gz -C /opt/ \
    && mv /opt/hadoop-3.3.6 /opt/hadoop \
    && rm /tmp/hadoop.tar.gz

RUN mkdir /var/run/sshd \
    && useradd -m -s /bin/bash usuario \
    && ssh-keygen -A \
    && mkdir -p /home/usuario/.ssh \
    && ssh-keygen -t rsa -N "" -f /home/usuario/.ssh/id_rsa \
    && cat /home/usuario/.ssh/id_rsa.pub >> /home/usuario/.ssh/authorized_keys \
    && chown -R usuario:usuario /home/usuario/.ssh \
    && chmod 700 /home/usuario/.ssh \
    && chmod 600 /home/usuario/.ssh/authorized_keys

WORKDIR /workspace

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
