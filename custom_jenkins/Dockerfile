# Custom Jenkins with Docker, Trivy, AWS CLI, and essential plugins
FROM jenkins/jenkins:lts-jdk17

# Switch to root user to install dependencies
USER root

# Install prerequisites
RUN apt-get update -y && \
    apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    software-properties-common \
    lsb-release \
    unzip \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Docker using modern method
RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
    https://download.docker.com/linux/debian $(lsb_release -cs) stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Docker Compose (standalone binary for compatibility)
RUN curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Install Aqua Trivy for security scanning
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws/

# Add Jenkins user to the Docker group
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Create directory for Docker socket
RUN mkdir -p /var/run

# Switch back to Jenkins user
USER jenkins

# Install Jenkins plugins (using jenkins-plugin-cli)
# Let jenkins-plugin-cli auto-resolve dependencies by not specifying versions
RUN jenkins-plugin-cli --plugins \
    docker-workflow \
    docker-plugin \
    github \
    git \
    workflow-aggregator \
    pipeline-stage-view \
    credentials-binding \
    amazon-ecr \
    timestamper \
    build-timeout \
    ws-cleanup \
    ansicolor

# Expose Jenkins ports
# 8080: Web UI
# 50000: Agent communication
EXPOSE 8080 50000

# Default Jenkins environment variables
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"
ENV JENKINS_OPTS="--httpPort=8080"
