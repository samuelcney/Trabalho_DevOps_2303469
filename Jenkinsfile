pipeline {
    agent any
    stages {
        stage('Cloning repository') {
            steps {
		echo 'Cloning repository...'
                git branch: 'main', url: 'https://github.com/samuelcney/Trabalho_DevOps_2303469.git'
            }
        }
	stage('Build'){
	     steps {
	        sh 'docker-compose up --build'
             }
	}
    }
}

