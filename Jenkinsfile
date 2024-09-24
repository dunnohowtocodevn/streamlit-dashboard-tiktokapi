pipeline {
    agent any
   
        
     
    stages {
        stage('Clone repository') {
            steps {
                echo 'Cloning repository...'
                git 'https://github.com/dunnohowtocodevn/streamlit-dashboard-tiktokapi.git' 
            }
        }
        stage('Build') {
            steps {
                echo 'Building the project...'
                
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'pytest --junitxml=test-results.xml'
            }
        }

        stage('Code Quality Analysis') {
            steps {
                echo 'Running code quality analysis with SonarQube...'
                withSonarQubeEnv('state-design') { // SonarQubeServer is the name of your SonarQube instance in Jenkins
                    sh 'sonar-scanner \
                        -Dsonar.projectKey=streamlit_project \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://localhost:9000 \
                        -Dsonar.login=${SONAR_TOKEN}'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying to test environment...'
                sh 'docker build -t streamlit_app .'
                sh 'docker run -d -p 8501:8501 streamlit_app'
            }
        }

        stage('Release') {
            steps {
                echo 'Releasing to production...'
                withCredentials([string(credentialsId: 'HEROKU_API_KEY', variable: 'HEROKU_API_KEY')]) {
                    sh 'heroku container:push web --app my-streamlit-app'
                    sh 'heroku container:release web --app my-streamlit-app'
                }
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Monitoring the production environment...'
                // Example command to interact with Datadog or New Relic API
                sh 'curl -X GET https://api.datadoghq.com/api/v1/monitor'
            }
        }
    }

    post {
        always {
            junit 'test-results.xml'
        }
    }
}
