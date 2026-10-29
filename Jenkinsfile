pipeline {
    agent any

    environment {
        APP_NAME = "devops-mini-project"
        IMAGE_NAME = "devops-mini-project"
        IMAGE_TAG = "${BUILD_NUMBER}"
        CONTAINER_NAME = "devops-app-live"
        HOST_PORT = "5000"
        CONTAINER_PORT = "5000"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "=== Stage 1: Checkout Source Code ==="
                checkout scm
            }
        }

        stage('Install Test Dependencies') {
            steps {
                echo "=== Stage 2: Install or Prepare Dependencies ==="
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv venv || python -m venv venv
                            . venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            python -m venv venv
                            call venv\\Scripts\\activate.bat
                            python -m pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        stage('Run Automated Tests') {
            steps {
                echo "=== Stage 3: Automated Testing with pytest ==="
                script {
                    if (isUnix()) {
                        sh '''
                            . venv/bin/activate
                            python -m pytest --junitxml=test-results.xml -v
                        '''
                    } else {
                        bat '''
                            call venv\\Scripts\\activate.bat
                            python -m pytest --junitxml=test-results.xml -v
                        '''
                    }
                }
            }
            post {
                always {
                    junit testResults: 'test-results.xml', allowEmptyResults: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "=== Stage 4: Build Docker Container Image ==="
                script {
                    if (isUnix()) {
                        sh """
                            docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .
                        """
                    } else {
                        bat """
                            docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .
                        """
                    }
                }
            }
        }

        stage('Deploy Application') {
            steps {
                echo "=== Stage 5: Deploy Docker Container ==="
                script {
                    if (isUnix()) {
                        sh """
                            # Stop and remove existing container if running
                            docker stop ${CONTAINER_NAME} || true
                            docker rm ${CONTAINER_NAME} || true
                            # Launch new container version
                            docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${CONTAINER_PORT} ${IMAGE_NAME}:latest
                        """
                    } else {
                        bat """
                            docker stop ${CONTAINER_NAME} 2>nul || ver>nul
                            docker rm ${CONTAINER_NAME} 2>nul || ver>nul
                            docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${CONTAINER_PORT} ${IMAGE_NAME}:latest
                        """
                    }
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                echo "=== Stage 6: Health Verification ==="
                script {
                    // Give container 3 seconds to bind port
                    sleep(time: 3, unit: 'SECONDS')
                    if (isUnix()) {
                        sh """
                            curl -f http://localhost:${HOST_PORT}/health || exit 1
                        """
                    } else {
                        powershell """
                            \$response = Invoke-RestMethod -Uri 'http://localhost:${HOST_PORT}/health' -Method Get
                            if (\$response.status -eq 'healthy') {
                                Write-Output 'Verification SUCCESS: Health check returned healthy status'
                            } else {
                                Write-Error 'Verification FAILED: Status is not healthy'
                                exit 1
                            }
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "=========================================================="
            echo "CI/CD PIPELINE SUCCEEDED!"
            echo "Application is live at: http://localhost:${HOST_PORT}"
            echo "Health endpoint: http://localhost:${HOST_PORT}/health"
            echo "=========================================================="
        }
        failure {
            echo "=========================================================="
            echo "CI/CD PIPELINE FAILED!"
            echo "Check console logs and test results for details."
            echo "=========================================================="
        }
    }
}
