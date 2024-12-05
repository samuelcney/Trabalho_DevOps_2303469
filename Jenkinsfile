pipeline {
    agent any

    environment {
        REPOSITORY_URL = 'https://github.com/samuelcney/trabalho-devops-2303469.git'
        BRANCH_NAME = 'main'
        CONTAINERS = 'mariadb flask test mysqld_exporter prometheus grafana'
    }

    stages {
        stage('Cloning repository') {
            steps {
                git branch: "${BRANCH_NAME}", url: "${REPOSITORY_URL}"
            }
        }

        stage('Build containers') {
            steps {
                script {
                    echo 'Stopping existing containers...'
                    sh 'docker-compose down'

                    echo 'Building Docker images...'
                    sh 'docker-compose build'
                }
            }
        }

        stage('Start Containers') {
            steps {
                script {
                    echo 'Starting Docker containers...'
                    sh "docker-compose up -d ${CONTAINERS}"
                    sleep 40
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    try {
                        echo 'Running tests...'
                        sh 'docker-compose run --rm test'
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error 'Pipeline process stopped because tests failed'
                    }
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
            sh 'docker-compose down'
        }
    }
}

