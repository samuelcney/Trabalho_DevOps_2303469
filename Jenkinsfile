pipeline {
    agent any
    stages {
        stage('Cloning repository') {
            steps {
		echo 'Cloning repository...'
                git branch: 'main', url: 'https://github.com/samuelcney/Trabalho_DevOps_2303469.git'
            }
        }
	stage('List files') {
            steps {
                sh 'ls -la'
            }
        }
	stage('Install dependecies'){
	     steps {
	     	sh 'cd flask/'
		sh 'pip install -r requirements.txt'
             }
	}
    }
}

