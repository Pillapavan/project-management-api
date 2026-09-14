pipeline {

    agent {
        docker {
            image 'python:3.12'
        }
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Python Version') {
            steps {
                sh 'python --version'
            }
        }

    }
}