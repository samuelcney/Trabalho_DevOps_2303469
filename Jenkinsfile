pipeline {
    agent any
    stages {
        stage('Cloning repository') {
            steps {
                echo 'Cloning repository...'
                git branch: 'test/run-test-pipes', url: 'https://github.com/samuelcney/Trabalho_DevOps_2303469.git'
            }
        }

	stage('Preparing'){
	   steps {
		script {
		    sh 'sudo chmod -R 777 /var/lib/jenkins/workspace/Trabalho-DevOps-2303469/prometheus'
		}
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
                    sh 'docker-compose exec flask pytest /app/test_app.py'
                }
            }
        }
    }
}

