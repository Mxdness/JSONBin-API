pipeline {
    agent any

    triggers {
        githubPush()
    }

    parameters {
        choice(
            name: 'TAG',
            choices: ['@tag1', '@tag2'],
            description: 'Which tagged group of scenarios to run'
        )
    }

    environment {
        // Secret text credential created in Jenkins (id: jsonbin-master-key)
        JSONBIN_MASTER_KEY = credentials('jsonbin-master-key')
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                // The job must execute the tests through custom_runner.py
                sh '.venv/bin/python custom_runner.py --tag "$TAG"'
            }
        }
    }

    post {
        always {
            // Automatic Allure report generation (runs even when tests fail)
            allure(
                commandline: 'allure',
                includeProperties: false,
                jdk: '',
                results: [[path: 'reports/allure-results']]
            )
            archiveArtifacts artifacts: 'screenshots/*.png', allowEmptyArchive: true
        }
    }
}
