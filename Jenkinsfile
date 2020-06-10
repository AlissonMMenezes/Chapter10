pipeline {
    agent  any;
    stages {
        stage('Preparing the environment') {
            steps {
                sh 'python -m pip install -r requirements.txt'
            }
        }
        stage('Code Quality') {
            steps {
                sh 'python -m pylint app.py'
            }
        }
        stage('Tests') {
            steps {
                sh 'python -m pytest'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build https://github.com/AlissonMMenezes/Chapter10.git -t chapter10:latest'
            }
        }        
        stage('Deploy') {
            steps {
                sh 'docker run -tdi -p 5000:5000 chapter10:latest'
            }
        }
    }
}
