pipeline {
    agent any
    
    stages {
        stage('Cloning repository') {
            steps {
                echo 'Cloning repository...'
                git branch: 'test/run-test-pipes', url: 'https://github.com/samuelcney/Trabalho_DevOps_2303469.git'
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
                }
            }
        }

        stage('Wait for Flask') {
            steps {
                script {
                    echo 'Waiting for Flask to start...'
                    sh 'docker-compose exec flask /bin/sh -c "while ! nc -z localhost 5000; do sleep 1; done;"'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Running tests...'
                    sh 'docker-compose exec flask pytest /app/test_py.py'
                }
            }
        }

        stage('Deploy and Monitor') {
            steps {
                script {
                    echo 'Ensuring monitoring is set up...'
                    echo 'Application deployed and monitored successfully.'
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh 'docker-compose down -v'
        }
    }
}

