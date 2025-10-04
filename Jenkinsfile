// Jenkinsfile - CI/CD Pipeline for Medical RAG Chatbot
// This file defines the automated build, scan, and deployment process

pipeline {
    // Agent: Specifies where the pipeline will execute
    // "any" means any available Jenkins agent
    agent any

    // Environment: Global variables available throughout the entire pipeline
    environment {
        // Docker image naming
        DOCKER_IMAGE = 'medical-rag-chatbot'
        DOCKER_TAG = "${env.BUILD_NUMBER}"  // Dynamic tag: build-1, build-2, etc.
        DOCKER_REGISTRY = 'docker.io'        // Change to your registry (Docker Hub or AWS ECR)

        // AWS ECR Configuration (will be configured when AWS is ready)
        AWS_REGION = 'us-east-1'
        // AWS_ACCOUNT_ID will be set via credentials in the Push to AWS ECR stage
        ECR_REPOSITORY = 'medical-rag-chatbot'

        // Trivy scan configuration
        TRIVY_SEVERITY = 'HIGH,CRITICAL'     // Only report high/critical vulnerabilities
        TRIVY_EXIT_CODE = '0'                // 0 = don't fail build, 1 = fail if vulnerabilities found
    }

    // Stages: Pipeline phases executed in order
    stages {

        // STAGE 1: CHECKOUT
        // Clone code from GitHub (automatic if Jenkins is connected to GitHub)
        stage('Checkout') {
            steps {
                echo 'Cloning code from GitHub...'
                // Git checkout is automatic, this echo is informative only
                checkout scm
            }
        }

        // STAGE 2: BUILD
        // Build Docker image using our multi-stage Dockerfile
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${DOCKER_IMAGE}:${DOCKER_TAG}"

                    // docker.build() is provided by docker-workflow plugin
                    // Executes: docker build -t medical-rag-chatbot:123 .
                    dockerImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")

                    // Also tag as 'latest'
                    sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                }
            }
        }

        // STAGE 3: SECURITY SCAN
        // Scan image with Trivy to detect vulnerabilities
        stage('Security Scan with Trivy') {
            steps {
                script {
                    echo "Scanning for vulnerabilities with Trivy..."

                    // Trivy scans the newly built image
                    // --severity: Only HIGH and CRITICAL
                    // --exit-code: 0 = don't fail build (warning only), 1 = fail build
                    // --no-progress: Don't show progress bar (better for logs)
                    sh """
                        trivy image \
                        --severity ${TRIVY_SEVERITY} \
                        --exit-code ${TRIVY_EXIT_CODE} \
                        --no-progress \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                    """

                    // Save report in JSON format (for later analysis)
                    sh """
                        trivy image \
                        --severity ${TRIVY_SEVERITY} \
                        --format json \
                        --output trivy-report.json \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                    """

                    // Archive the report for download from Jenkins UI
                    archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
                }
            }
        }

        // STAGE 4A: PUSH TO DOCKER HUB
        // Upload image to Docker Hub for public portfolio visibility
        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing image to Docker Hub..."

                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh """
                            echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                            docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} \$DOCKER_USER/${DOCKER_IMAGE}:${DOCKER_TAG}
                            docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} \$DOCKER_USER/${DOCKER_IMAGE}:latest
                            docker push \$DOCKER_USER/${DOCKER_IMAGE}:${DOCKER_TAG}
                            docker push \$DOCKER_USER/${DOCKER_IMAGE}:latest
                        """
                    }
                }
            }
        }

        // STAGE 4B: PUSH TO AWS ECR
        // Upload image to AWS ECR for private registry and AWS deployment
        stage('Push to AWS ECR') {
            steps {
                script {
                    echo "Pushing image to AWS ECR..."

                    withCredentials([
                        string(credentialsId: 'aws-account-id', variable: 'AWS_ACCOUNT_ID'),
                        aws(credentialsId: 'aws-credentials')
                    ]) {
                        sh """
                            # Set ECR registry URL
                            ECR_REGISTRY=\${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

                            # Login to AWS ECR
                            aws ecr get-login-password --region ${AWS_REGION} | \
                            docker login --username AWS --password-stdin \$ECR_REGISTRY

                            # Tag for ECR
                            docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} \$ECR_REGISTRY/${ECR_REPOSITORY}:${DOCKER_TAG}
                            docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} \$ECR_REGISTRY/${ECR_REPOSITORY}:latest

                            # Push to ECR
                            docker push \$ECR_REGISTRY/${ECR_REPOSITORY}:${DOCKER_TAG}
                            docker push \$ECR_REGISTRY/${ECR_REPOSITORY}:latest
                        """
                    }
                }
            }
        }

        // STAGE 5: DEPLOY (Optional)
        // Deploy application using docker-compose
        stage('Deploy') {
            // Only deploy from main/master branch
            when {
                branch 'main'
            }
            steps {
                script {
                    echo "Deploying application..."

                    // OPTION A: Local deployment (for testing)
                    sh """
                        docker-compose down
                        docker-compose up -d
                    """

                    // OPTION B: Remote deployment via SSH (uncomment if using remote server)
                    /*
                    sshagent(['ssh-credentials']) {
                        sh """
                            ssh user@server.com 'cd /app && docker-compose pull && docker-compose up -d'
                        """
                    }
                    */

                    // OPTION C: Deploy to Kubernetes (uncomment if using K8s)
                    /*
                    sh """
                        kubectl set image deployment/medical-rag-app \
                        app=${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_TAG}
                    """
                    */
                }
            }
        }

        // STAGE 6: CLEANUP
        // Clean old Docker images to save disk space
        stage('Cleanup') {
            steps {
                script {
                    echo "Cleaning old images..."

                    // Remove dangling images (no tag)
                    sh 'docker image prune -f'

                    // Optional: Remove images from previous builds
                    // Keep only the last 5 images
                    sh """
                        docker images ${DOCKER_IMAGE} --format '{{.Tag}}' | \
                        tail -n +6 | \
                        xargs -I {} docker rmi ${DOCKER_IMAGE}:{} || true
                    """
                }
            }
        }
    }

    // Post: Actions after pipeline (success or failure)
    post {
        // ALWAYS: Runs every time (success or failure)
        always {
            echo "Pipeline completed in ${currentBuild.durationString}"

            // Clean workspace (optional)
            cleanWs()
        }

        // SUCCESS: Only if pipeline succeeded
        success {
            echo "Pipeline successful! Image ${DOCKER_IMAGE}:${DOCKER_TAG} is ready."

            // Optional: Send Slack/Discord notification
            /*
            slackSend(
                color: 'good',
                message: "Build #${env.BUILD_NUMBER} succeeded: ${env.JOB_NAME}"
            )
            */
        }

        // FAILURE: Only if pipeline failed
        failure {
            echo "Pipeline failed. Check logs above for details."

            // Optional: Send error notification
            /*
            slackSend(
                color: 'danger',
                message: "Build #${env.BUILD_NUMBER} FAILED: ${env.JOB_NAME}"
            )
            */
        }

        // UNSTABLE: If there are warnings but no fatal errors
        unstable {
            echo "Pipeline unstable (warnings found)"
        }
    }
}
