pipeline {
    agent any  // Runs on any available agent

    stages {
        stage('Clone Repository') {
            steps {
                // Git clone step
                git 'https://github.com/yourusername/yourrepository.git'  // Your repo URL
            }
        }

        stage('Install Dependencies') {
            steps {
                // Install Python dependencies
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Start Flask App') {
            steps {
                // Start the Flask app in the background
                sh 'python app/lockedRESTs.py &'
                
                // Wait for the Flask app to fully start
                sleep time: 5, unit: 'SECONDS'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                // Run Selenium tests using pytest
                sh 'pytest tests/test_flask_app.py'
            }
        }

        post {
            always {
                // Always execute after the tests run
                echo "Tests completed"
            }
            success {
                echo "Tests passed successfully!"
            }
            failure {
                echo "Tests failed. Please check the logs."
            }
        }
    }
}