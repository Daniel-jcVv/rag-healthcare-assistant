# Custom Jenkins CI/CD Setup

Custom Jenkins Docker image with Docker-in-Docker, Trivy security scanning, AWS CLI, and pre-installed plugins for the Medical RAG Chatbot CI/CD pipeline.

---

## 📦 What's Included

### Tools Installed

- ✅ **Docker CE** - Build and push images
- ✅ **Docker Compose v2.24.0** - Multi-container orchestration
- ✅ **Aqua Trivy** - Container security vulnerability scanning
- ✅ **AWS CLI v2** - Push images to AWS ECR
- ✅ **Git** - Source control

### Jenkins Plugins Pre-installed

| Plugin | Purpose |
|--------|---------|
| **docker-workflow** | Docker Pipeline steps |
| **docker-plugin** | Docker integration |
| **github** | GitHub integration |
| **git** | Git SCM support |
| **workflow-aggregator** | Pipeline as Code |
| **pipeline-stage-view** | Visualize pipeline stages |
| **credentials-binding** | Secure credentials management |
| **amazon-ecr** | AWS ECR push support |
| **timestamper** | Add timestamps to console |
| **ansicolor** | Colorized console output |

---

## 🚀 Quick Start

### 1. Build and Start Jenkins

```bash
cd custom_jenkins/

# Build the custom Jenkins image
docker-compose build

# Start Jenkins
docker-compose up -d

# View logs
docker-compose logs -f
```

### 2. Access Jenkins

Open: http://localhost:8080

**Initial Admin Password:**

```bash
# Get the initial admin password
docker exec jenkins-cicd cat /var/jenkins_home/secrets/initialAdminPassword
```

**Note:** Setup wizard is disabled (`runSetupWizard=false`), but you still need the admin password for first login.

### 3. Verify Installations

```bash
# Enter Jenkins container
docker exec -it jenkins-cicd bash

# Check versions
docker --version
docker-compose --version
trivy --version
aws --version
```

Expected output:
```
Docker version 24.0.x
Docker Compose version v2.24.0
Version: 0.x.x
aws-cli/2.x.x
```

---

## 🔧 Configuration

### AWS Credentials

#### Option 1: Environment Variables (docker-compose.yml)

Create `.env` file in `custom_jenkins/`:

```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
```

Then uncomment AWS env vars in `docker-compose.yml`.

#### Option 2: Jenkins Credentials (Recommended)

1. Go to **Jenkins → Manage Jenkins → Credentials**
2. Add **AWS Credentials** (ID: `aws-credentials`)
3. Use in Jenkinsfile:
   ```groovy
   withCredentials([aws(credentialsId: 'aws-credentials')]) {
       sh 'aws ecr get-login-password | docker login ...'
   }
   ```

---

### GitHub Integration

#### 1. Create Personal Access Token

Go to: https://github.com/settings/tokens

**Permissions needed:**
- `repo` (full control)
- `admin:repo_hook` (webhooks)

#### 2. Add to Jenkins

1. **Jenkins → Manage Jenkins → Credentials**
2. **Add Credentials → Secret text**
   - **ID:** `github-token`
   - **Secret:** Your PAT token

#### 3. Configure Webhook

**GitHub Repository → Settings → Webhooks → Add webhook**

- **Payload URL:** `http://your-jenkins-url:8080/github-webhook/`
- **Content type:** `application/json`
- **Events:** Push, Pull Request

---

## 📝 Jenkinsfile Example

Create `Jenkinsfile` in your repository root:

```groovy
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'medical-rag-chatbot'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        ECR_REGISTRY = '123456789.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPO = 'medical-rag-chatbot'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/yourusername/medical-rag-chatbot.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Trivy Security Scan') {
            steps {
                script {
                    sh """
                        trivy image --severity HIGH,CRITICAL \
                        --exit-code 1 \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                    """
                }
            }
        }

        stage('Push to ECR') {
            steps {
                withCredentials([aws(credentialsId: 'aws-credentials')]) {
                    script {
                        sh """
                            aws ecr get-login-password --region us-east-1 | \
                            docker login --username AWS --password-stdin ${ECR_REGISTRY}

                            docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} \
                            ${ECR_REGISTRY}/${ECR_REPO}:${DOCKER_TAG}

                            docker push ${ECR_REGISTRY}/${ECR_REPO}:${DOCKER_TAG}
                        """
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    sh "docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
```

---

## 🔐 Security Best Practices

### 1. Never Commit Credentials

```bash
# Add to .gitignore
.env
credentials.txt
*.pem
*.key
```

### 2. Use Jenkins Credentials Store

Always use Jenkins' built-in credentials management instead of hardcoding.

### 3. Scan Images Before Push

Trivy is included to fail the pipeline if HIGH/CRITICAL vulnerabilities are found:

```bash
trivy image --severity HIGH,CRITICAL --exit-code 1 myimage:tag
```

### 4. Limit Jenkins Network Access

In production, restrict port 8080 to VPN/internal network only.

---

## 🐛 Troubleshooting

### Issue: "Permission denied" when running Docker

**Cause:** Jenkins user not in docker group

**Fix:**
```bash
docker exec -it jenkins-cicd bash
groups jenkins  # Should show 'docker'

# If not, rebuild the image:
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

### Issue: Docker socket not accessible

**Error:** `Cannot connect to the Docker daemon at unix:///var/run/docker.sock`

**Fix:**
```bash
# Check socket permissions on host
ls -l /var/run/docker.sock

# Should be: srw-rw---- 1 root docker

# Add your user to docker group on host
sudo usermod -aG docker $USER
newgrp docker
```

---

### Issue: Trivy scan fails with network error

**Error:** `Failed to download vulnerability DB`

**Fix:**
```bash
# Update Trivy DB manually
docker exec jenkins-cicd trivy image --download-db-only

# Or increase timeout
trivy image --timeout 10m myimage:tag
```

---

### Issue: AWS CLI not authenticated

**Error:** `Unable to locate credentials`

**Fix:**

Check credentials in container:
```bash
docker exec jenkins-cicd aws configure list
```

Configure via Jenkins credentials or environment variables.

---

## 📊 Resource Usage

| Component | CPU | RAM | Disk |
|-----------|-----|-----|------|
| **Jenkins (idle)** | <10% | 500MB | 1GB |
| **Jenkins (building)** | 50-100% | 1.5GB | 2GB+ |
| **Docker builds** | 80-100% | 1-2GB | Varies |

**Recommended:** 4 CPU cores, 8GB RAM, 50GB disk

---

## 🔄 Maintenance

### Update Jenkins

```bash
# Stop Jenkins
docker-compose down

# Pull latest Jenkins LTS
docker-compose build --no-cache

# Start with updated image
docker-compose up -d
```

### Backup Jenkins Data

```bash
# Backup Jenkins home
docker run --rm \
  -v jenkins-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/jenkins-backup.tar.gz -C /data .

# Restore
docker run --rm \
  -v jenkins-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/jenkins-backup.tar.gz -C /data
```

### Clean Old Builds

```bash
# Remove old Docker images
docker exec jenkins-cicd docker system prune -a -f

# Or configure in Jenkins:
# Manage Jenkins → Configure System → Discard old builds
```

---

## 📚 Additional Resources

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Jenkins Docker Plugin](https://plugins.jenkins.io/docker-plugin/)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [AWS ECR User Guide](https://docs.aws.amazon.com/ecr/)

---

## 🚀 Next Steps

1. ✅ Start Jenkins: `docker-compose up -d`
2. ✅ Get admin password: `docker exec jenkins-cicd cat /var/jenkins_home/secrets/initialAdminPassword`
3. ✅ Access UI: http://localhost:8080
4. ✅ Add AWS credentials
5. ✅ Add GitHub token
6. ✅ Create pipeline job
7. ✅ Connect GitHub webhook
8. ✅ Run first build!

---

**Last Updated:** 2025-10-03
**Jenkins Version:** LTS (JDK 17)
**Docker Version:** 24.0+
