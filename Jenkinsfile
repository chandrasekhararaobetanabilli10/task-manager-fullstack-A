pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate Python') {
            steps {
                sh 'python3 -m py_compile backend/app.py'
            }
        }

        stage('Build and Deploy with Docker') {
            steps {
                sh 'docker compose -p task-manager-fullstack up -d --build'
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'docker compose -p task-manager-fullstack ps'
            }
        }
    }

    post {
        success {
            echo 'Task Manager deployed successfully!'
            echo 'Application URL: http://localhost:5000'
        }
        failure {
            echo 'Pipeline failed. Check the Jenkins console output.'
        }
    }
}
