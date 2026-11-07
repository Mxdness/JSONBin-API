FROM jenkins/jenkins:lts-jdk21

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git curl ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER jenkins

# Plugins (git, pipeline, credentials, Allure, Configuration-as-Code)
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

# Pre-configures the Allure Commandline tool and the JSONBin credential
COPY casc.yaml /usr/share/jenkins/casc/casc.yaml
ENV CASC_JENKINS_CONFIG=/usr/share/jenkins/casc/casc.yaml
