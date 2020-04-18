pipeline {
    agent { label "master" }
    stages {
        stage("Build container") {
            agent { label "docker" }
            steps {
                script {
                    sh "docker build -t localhost:5000/reevefresh:latest ."
                }
            }
        }
        stage("Deploy container") {
            agent { label "docker" }
            steps {
                sh "docker save localhost:5000/reevefresh:latest | bzip2 | ssh oracle 'bunzip2 | docker load'"
            }
        }
    }
    post {
        success { cleanWs() }
        always { sendNotifications currentBuild.result }
    }
}
