pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('CI Test') {
            steps {
                sh 'echo "Jenkins CI is working!"'
            }
        }
    }
}