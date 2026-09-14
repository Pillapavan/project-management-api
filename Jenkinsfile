pipeline {
    agent any

    environment {
        CI_NETWORK = 'jenkins-ci-network'
        MYSQL_CONTAINER = 'mysql-test'
        DATABASE_URL = 'mysql+pymysql://root:testpassword@mysql-test:3306/test_db'
        SECRET_KEY = 'ci-test-secret'
        ALGORITHM = 'HS256'
        ACCESS_TOKEN_EXPIRE_MINUTES = '30'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Start MySQL') {
            steps {
                sh '''
                    docker network inspect $CI_NETWORK >/dev/null 2>&1 || \
                    docker network create $CI_NETWORK

                    docker rm -f $MYSQL_CONTAINER >/dev/null 2>&1 || true

                    docker run -d \
                      --name $MYSQL_CONTAINER \
                      --network $CI_NETWORK \
                      -e MYSQL_ROOT_PASSWORD=testpassword \
                      -e MYSQL_DATABASE=test_db \
                      mysql:8.4
                '''
            }
        }

        stage('Wait for MySQL') {
            steps {
                sh '''
                    echo "Waiting for MySQL..."

                    for i in $(seq 1 30); do
                        if docker exec $MYSQL_CONTAINER \
                           mysqladmin ping \
                           -h localhost \
                           -uroot \
                           -ptestpassword \
                           --silent; then
                            echo "MySQL is ready!"
                            exit 0
                        fi

                        sleep 2
                    done

                    echo "MySQL did not become ready."
                    exit 1
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest -v
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker rm -f $MYSQL_CONTAINER >/dev/null 2>&1 || true
                docker network rm $CI_NETWORK >/dev/null 2>&1 || true
            '''
        }
    }
}