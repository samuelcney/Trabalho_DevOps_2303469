pipeline {
    agent any

    environment {
        REPOSITORY_URL = 'https://github.com/samuelcney/Trabalho_DevOps_2303469.git'
        BRANCH_NAME = 'test/run-test-pipes'
    }

    stages {
        stage('Cloning repository') {
            steps {
                git branch: "${BRANCH_NAME}", url: "${REPOSITORY_URL}"
            }
        }

        stage('Build') {
            steps {
                script {
                    echo 'Stopping and removing existing containers...'
                    sh 'docker-compose down -v'

                    echo 'Building Docker images...'
                    sh 'docker-compose build'
                }
            }
        }

	stage('Start Containers') {
            steps {
                script {
                    echo 'Starting Docker containers...'
                    sh 'docker-compose up -d'
                    sleep 10
                }
            }
        } 

        stage('Run Tests') {
            steps {
                script {
                    echo 'Running tests...'
                    sh 'sleep 20'
                    sh 'docker-compose run --rm test'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully'
        }
        failure {
            echo 'The pipeline fails to execute'
        }
    }
}
