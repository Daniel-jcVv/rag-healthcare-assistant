# Jenkins CI/CD Pipeline Documentation

Complete guide for understanding and configuring the Jenkins CI/CD pipeline for the Medical RAG Chatbot.

---

## 📚 Table of Contents

1. [What is a Jenkinsfile?](#what-is-a-jenkinsfile)
2. [Pipeline Stages Explained](#pipeline-stages-explained)
3. [Configuration Guide](#configuration-guide)
4. [GitHub Integration](#github-integration)
5. [Credentials Setup](#credentials-setup)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Usage](#advanced-usage)

---

## What is a Jenkinsfile?

### Definition

A **Jenkinsfile** is a text file that defines your **CI/CD pipeline as code**. It automates the entire process from code commit to production deployment.

### Why Use Jenkinsfile?

**Without Jenkinsfile (Manual):**
```
Developer commits code → manually build → manually test → manually deploy
Time: 30-60 minutes
Error-prone: Yes
Reproducible: No
```

**With Jenkinsfile (Automated):**
```
Developer commits code → Jenkins automatically: build + test + scan + deploy
Time: 5-10 minutes
Error-prone: No
Reproducible: Yes
```

---

## Pipeline Stages Explained

### Overview

```
GitHub Push → Jenkins Webhook → Pipeline Execution

Pipeline Flow:
1. Checkout    (Clone code)
2. Build       (Create Docker image)
3. Scan        (Trivy security check)
4. Push        (Upload to registry)
5. Deploy      (Start containers)
6. Cleanup     (Remove old images)
```

---

### Stage 1: Checkout

**What it does:** Clones your GitHub repository into Jenkins workspace

**Code:**
```groovy
stage('Checkout') {
    steps {
        checkout scm  // scm = Source Code Management (GitHub)
    }
}
```

**Happens automatically** if you configure GitHub webhook correctly.

---

### Stage 2: Build Docker Image

**What it does:** Executes `docker build` using your multi-stage Dockerfile

**Code:**
```groovy
stage('Build Docker Image') {
    steps {
        script {
            dockerImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
            sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
        }
    }
}
```

**Equivalent bash:**
```bash
docker build -t medical-rag-chatbot:123 .
docker tag medical-rag-chatbot:123 medical-rag-chatbot:latest
```

**Variables:**
- `DOCKER_IMAGE` = "medical-rag-chatbot"
- `DOCKER_TAG` = Build number (auto-incremented: 1, 2, 3...)
- `BUILD_NUMBER` = Jenkins environment variable

**Result:** Docker image tagged as:
- `medical-rag-chatbot:123` (specific version)
- `medical-rag-chatbot:latest` (always newest)

---

### Stage 3: Security Scan with Trivy

**What it does:** Scans Docker image for vulnerabilities (CVEs)

**Code:**
```groovy
stage('Security Scan with Trivy') {
    steps {
        sh """
            trivy image \
            --severity HIGH,CRITICAL \
            --exit-code 0 \
            --no-progress \
            ${DOCKER_IMAGE}:${DOCKER_TAG}
        """
    }
}
```

**Parameters explained:**
- `--severity HIGH,CRITICAL` - Only report serious vulnerabilities
- `--exit-code 0` - Don't fail build (warning only)
  - Change to `1` to FAIL build if vulnerabilities found
- `--no-progress` - Clean logs (no progress bar)
- `--format json` - Save report as JSON

**Example output:**
```
medical-rag-chatbot:123 (debian 12.4)
===================================
Total: 2 (HIGH: 1, CRITICAL: 1)

┌─────────────┬────────────────┬──────────┬──────────────────┐
│   Library   │ Vulnerability  │ Severity │ Installed Version│
├─────────────┼────────────────┼──────────┼──────────────────┤
│ curl        │ CVE-2024-XXXX  │ HIGH     │ 7.88.1           │
│ openssl     │ CVE-2024-YYYY  │ CRITICAL │ 3.0.11           │
└─────────────┴────────────────┴──────────┴──────────────────┘
```

**Trivy report artifact:** Available for download in Jenkins UI under "Build Artifacts"

---

### Stage 4: Push to Registry

**What it does:** Uploads Docker image to Docker Hub or AWS ECR

**Option A: Docker Hub**

```groovy
withCredentials([usernamePassword(
    credentialsId: 'dockerhub-credentials',
    usernameVariable: 'DOCKER_USER',
    passwordVariable: 'DOCKER_PASS'
)]) {
    sh """
        echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_USER}/${DOCKER_IMAGE}:${DOCKER_TAG}
        docker push ${DOCKER_USER}/${DOCKER_IMAGE}:${DOCKER_TAG}
        docker push ${DOCKER_USER}/${DOCKER_IMAGE}:latest
    """
}
```

**Requires:** Docker Hub credentials configured in Jenkins (see [Credentials Setup](#credentials-setup))

**Result:** Image available at `docker.io/username/medical-rag-chatbot:123`

---

**Option B: AWS ECR**

```groovy
withCredentials([aws(credentialsId: 'aws-credentials')]) {
    sh """
        aws ecr get-login-password --region us-east-1 | \
        docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} 123456789.dkr.ecr.us-east-1.amazonaws.com/medical-rag:${DOCKER_TAG}
        docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/medical-rag:${DOCKER_TAG}
    """
}
```

**Requires:**
1. AWS ECR repository created
2. AWS credentials configured in Jenkins
3. IAM permissions for ECR push

---

### Stage 5: Deploy

**What it does:** Deploys the application using docker-compose

**Code:**
```groovy
stage('Deploy') {
    when {
        branch 'main'  // Only deploy from main branch
    }
    steps {
        sh """
            docker-compose down
            docker-compose up -d
        """
    }
}
```

**`when` condition:** Only runs on `main` branch (not feature branches)

**Example:**
- Push to `feature/cicd-deployment` → Build + Scan + Push (NO deploy)
- Push to `main` → Build + Scan + Push + **Deploy** ✅

---

### Stage 6: Cleanup

**What it does:** Removes old Docker images to save disk space

**Code:**
```groovy
stage('Cleanup') {
    steps {
        sh 'docker image prune -f'  // Remove dangling images
    }
}
```

**Why needed?** Each build creates a new image:
- Build 1: `medical-rag-chatbot:1`
- Build 2: `medical-rag-chatbot:2`
- Build 100: `medical-rag-chatbot:100`

Without cleanup: 100 images × 600MB = **60GB disk usage**

**Options:**
```bash
# Remove dangling images (no tag)
docker image prune -f

# Remove images older than 7 days
docker image prune -a --filter "until=168h"

# Keep only last 5 builds
docker images medical-rag-chatbot --format '{{.Tag}}' | tail -n +6 | xargs -I {} docker rmi medical-rag-chatbot:{}
```

---

### Post Actions

**What it does:** Runs after pipeline (success or failure)

```groovy
post {
    always {
        echo "Pipeline completed"
        cleanWs()  // Clean workspace
    }
    success {
        echo "✅ Build successful!"
        // Optional: Slack notification
    }
    failure {
        echo "❌ Build failed"
        // Optional: Send email alert
    }
}
```

**Sections:**
- `always` - Runs every time (success or failure)
- `success` - Only if pipeline succeeded
- `failure` - Only if pipeline failed
- `unstable` - If there are warnings but no errors

---

## Configuration Guide

### 1. Environment Variables

Located at top of Jenkinsfile:

```groovy
environment {
    DOCKER_IMAGE = 'medical-rag-chatbot'
    DOCKER_TAG = "${env.BUILD_NUMBER}"
    TRIVY_SEVERITY = 'HIGH,CRITICAL'
    TRIVY_EXIT_CODE = '0'  // Change to '1' to fail on vulnerabilities
}
```

**Common modifications:**

**Fail build on vulnerabilities:**
```groovy
TRIVY_EXIT_CODE = '1'  // Pipeline fails if HIGH/CRITICAL found
```

**Scan all severities:**
```groovy
TRIVY_SEVERITY = 'LOW,MEDIUM,HIGH,CRITICAL'
```

**Use semantic versioning:**
```groovy
DOCKER_TAG = "v1.0.${env.BUILD_NUMBER}"  // v1.0.1, v1.0.2, etc.
```

---

### 2. Branch-Specific Behavior

```groovy
when {
    branch 'main'  // Only on main branch
}
```

**Options:**
```groovy
when {
    branch 'develop'           // Only develop
    branch pattern: "release-.*", comparator: "REGEXP"  // release-1.0, release-2.0
    not { branch 'main' }      // All branches except main
}
```

---

### 3. Docker Registry Selection

**Using Docker Hub:**
```groovy
environment {
    DOCKER_REGISTRY = 'docker.io'
    DOCKER_USER = 'yourusername'
}
```

**Using AWS ECR:**
```groovy
environment {
    AWS_REGION = 'us-east-1'
    AWS_ACCOUNT_ID = '123456789012'
    ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
}
```

**Using private registry:**
```groovy
environment {
    DOCKER_REGISTRY = 'registry.company.com:5000'
}
```

---

## GitHub Integration

### 1. Create GitHub Webhook

**GitHub Repository → Settings → Webhooks → Add webhook**

**Configuration:**
- **Payload URL:** `http://your-jenkins-url:8080/github-webhook/`
- **Content type:** `application/json`
- **Events:**
  - ✅ Push events
  - ✅ Pull request events
- **Active:** ✅ Checked

**Example:**
```
Payload URL: http://192.168.1.100:8080/github-webhook/
Secret: (optional, for security)
Events: Just the push event
```

---

### 2. Jenkins Job Configuration

**Jenkins → New Item → Pipeline**

**Configure:**

1. **General → GitHub project:**
   - ✅ Check "GitHub project"
   - URL: `https://github.com/yourusername/medical-rag-chatbot`

2. **Build Triggers:**
   - ✅ Check "GitHub hook trigger for GITScm polling"

3. **Pipeline:**
   - **Definition:** Pipeline script from SCM
   - **SCM:** Git
   - **Repository URL:** `https://github.com/yourusername/medical-rag-chatbot.git`
   - **Credentials:** (your GitHub token)
   - **Branch:** `*/main` (or `*/develop`)
   - **Script Path:** `Jenkinsfile`

**Save** and test by pushing to GitHub.

---

## Credentials Setup

### 1. Docker Hub Credentials

**Jenkins → Manage Jenkins → Credentials → Global → Add Credentials**

**Type:** Username with password
- **ID:** `dockerhub-credentials`
- **Username:** Your Docker Hub username
- **Password:** Your Docker Hub password or [access token](https://hub.docker.com/settings/security)

**Usage in Jenkinsfile:**
```groovy
withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', ...)]) {
    // Docker commands here
}
```

---

### 2. AWS Credentials

**Jenkins → Manage Jenkins → Credentials → Global → Add Credentials**

**Type:** AWS Credentials
- **ID:** `aws-credentials`
- **Access Key ID:** Your AWS access key
- **Secret Access Key:** Your AWS secret key

**OR**

**Type:** Secret text
- **ID:** `aws-access-key-id`
- **Secret:** Your access key

**Type:** Secret text
- **ID:** `aws-secret-access-key`
- **Secret:** Your secret key

**Usage in Jenkinsfile:**
```groovy
withCredentials([aws(credentialsId: 'aws-credentials')]) {
    sh 'aws ecr ...'
}
```

---

### 3. GitHub Personal Access Token

**GitHub → Settings → Developer settings → Personal access tokens → Generate new token**

**Permissions needed:**
- ✅ `repo` (full control)
- ✅ `admin:repo_hook` (webhooks)

**Jenkins → Credentials → Add:**
- **Type:** Secret text
- **ID:** `github-token`
- **Secret:** Your PAT

---

## Troubleshooting

### Issue 1: "docker: command not found"

**Error:**
```
sh: docker: command not found
```

**Cause:** Jenkins container doesn't have Docker installed

**Fix:** Verify custom Jenkins image is being used:
```bash
docker exec jenkins-cicd docker --version
# Should output: Docker version 24.0.x
```

If not, rebuild Jenkins:
```bash
cd custom_jenkins/
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

### Issue 2: "Permission denied" on docker.sock

**Error:**
```
Got permission denied while trying to connect to the Docker daemon socket
```

**Cause:** Jenkins user not in docker group

**Fix:**
```bash
docker exec -it jenkins-cicd bash
groups jenkins  # Should show 'docker'

# If not:
exit
cd custom_jenkins/
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

### Issue 3: Trivy fails with "database error"

**Error:**
```
Failed to download vulnerability DB
```

**Fix:**
```bash
# Update Trivy DB manually
docker exec jenkins-cicd trivy image --download-db-only

# Or increase timeout in Jenkinsfile
sh "trivy image --timeout 10m ${DOCKER_IMAGE}:${DOCKER_TAG}"
```

---

### Issue 4: AWS ECR login fails

**Error:**
```
Error: Cannot perform an interactive login from a non TTY device
```

**Fix:** Use `--password-stdin`:
```bash
aws ecr get-login-password --region us-east-1 | \
docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
```

---

### Issue 5: GitHub webhook not triggering

**Checklist:**
1. ✅ Webhook URL ends with `/github-webhook/` (trailing slash important)
2. ✅ Jenkins is accessible from internet (not localhost)
3. ✅ "GitHub hook trigger" enabled in job configuration
4. ✅ Repository URL matches exactly

**Test webhook:**
GitHub → Settings → Webhooks → Edit → Recent Deliveries → Redeliver

---

## Advanced Usage

### Parallel Stages

Run tests in parallel:

```groovy
stage('Tests') {
    parallel {
        stage('Unit Tests') {
            steps {
                sh 'pytest tests/unit/'
            }
        }
        stage('Integration Tests') {
            steps {
                sh 'pytest tests/integration/'
            }
        }
        stage('Security Scan') {
            steps {
                sh 'trivy image ...'
            }
        }
    }
}
```

---

### Conditional Deployment

```groovy
stage('Deploy to Staging') {
    when {
        branch 'develop'
    }
    steps {
        sh 'docker-compose -f docker-compose.staging.yml up -d'
    }
}

stage('Deploy to Production') {
    when {
        branch 'main'
    }
    steps {
        input message: 'Deploy to production?'  // Manual approval
        sh 'docker-compose -f docker-compose.prod.yml up -d'
    }
}
```

---

### Email Notifications

```groovy
post {
    failure {
        emailext (
            subject: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body: """
                Build failed!

                Job: ${env.JOB_NAME}
                Build: ${env.BUILD_NUMBER}
                URL: ${env.BUILD_URL}
            """,
            to: 'team@company.com'
        )
    }
}
```

---

### Slack Notifications

```groovy
post {
    success {
        slackSend (
            color: 'good',
            message: "✅ Build #${env.BUILD_NUMBER} succeeded\n${env.BUILD_URL}"
        )
    }
    failure {
        slackSend (
            color: 'danger',
            message: "❌ Build #${env.BUILD_NUMBER} failed\n${env.BUILD_URL}"
        )
    }
}
```

**Requires:** Slack plugin installed and configured in Jenkins

---

## Best Practices

### 1. Always Tag Images with Build Number

```groovy
DOCKER_TAG = "${env.BUILD_NUMBER}"  // ✅ Good
DOCKER_TAG = "latest"               // ❌ Bad (no versioning)
```

### 2. Fail Build on Critical Vulnerabilities

```groovy
TRIVY_EXIT_CODE = '1'  // Fail if HIGH/CRITICAL found
```

### 3. Use Credentials, Never Hardcode

```groovy
// ❌ BAD
sh "docker login -u admin -p password123"

// ✅ GOOD
withCredentials([...]) {
    sh "docker login ..."
}
```

### 4. Clean Workspace After Build

```groovy
post {
    always {
        cleanWs()  // Prevents disk full
    }
}
```

### 5. Use Separate Stages for Clarity

```groovy
// ✅ GOOD - Clear stages
stage('Build') { ... }
stage('Test') { ... }
stage('Deploy') { ... }

// ❌ BAD - Everything in one stage
stage('Build and Deploy') { ... }
```

---

## Pipeline Visualization

**In Jenkins UI:**

```
┌─────────────┐
│  Checkout   │  (10s)
└──────┬──────┘
       │
┌──────▼──────┐
│    Build    │  (2m 30s)
└──────┬──────┘
       │
┌──────▼──────┐
│    Scan     │  (45s)
└──────┬──────┘
       │
┌──────▼──────┐
│    Push     │  (1m 15s)
└──────┬──────┘
       │
┌──────▼──────┐
│   Deploy    │  (30s)
└──────┬──────┘
       │
┌──────▼──────┐
│   Cleanup   │  (10s)
└─────────────┘

Total: ~5 minutes
```

**Green** = Success
**Red** = Failed
**Yellow** = Unstable (warnings)

---

## Resources

- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [Docker Hub Registry](https://hub.docker.com/)
- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)

---

**Last Updated:** 2025-10-03
**Jenkins Version:** LTS 2.426+
**Trivy Version:** 0.48+
