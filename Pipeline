pipeline {
    agent any
    environment {
        REMOTE_HOST = "ubuntu-2@10.0.0.250"
        ZIP_NAME = "python-test.zip"
        LOCAL_PROJECT_PATH = "/var/lib/jenkins/workspace/python-test"
        REMOTE_TMP = "/tmp"
        REMOTE_TARGET = "/var/www/html"
    }
    stages {
        stage('Zip Project') {
            steps {
                sh '''
                    cd /var/lib/jenkins/workspace
                    zip -r ${ZIP_NAME} python-test
                '''
            }
        }

        stage('SCP to Remote Server') {
            steps {
                sshagent(credentials: ['remote-ssh-key']) {
                    sh '''
                        scp -o StrictHostKeyChecking=no /var/lib/jenkins/workspace/${ZIP_NAME} ${REMOTE_HOST}:${REMOTE_TMP}/
                    '''
                }
            }
        }

        stage('Unzip and Move on Remote Server') {
            steps {
                sshagent(credentials: ['remote-ssh-key']) {
                    sh '''
                        ssh -tt -o StrictHostKeyChecking=no ${REMOTE_HOST} << 'EOF'
                        set -e
                        sudo rm -rf ${REMOTE_TARGET}/*
                        unzip -o ${REMOTE_TMP}/${ZIP_NAME} -d ${REMOTE_TMP}/unzipped
                        sudo cp -r ${REMOTE_TMP}/unzipped/python-test/* ${REMOTE_TARGET}/
                        sudo systemctl restart nginx
                        exit
                        EOF
                    '''
                }
            }
        }
    }
}
