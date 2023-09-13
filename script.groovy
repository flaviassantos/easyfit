def buildImage() {
    echo "building the docker image..."
    withCredentials([usernamePassword(credentialsId: 'docker-hub-repo', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
        sh 'docker build -t flaviassantos/easyfit:1.0.0 .'
        sh "echo $PASS | docker login -u $USER --password-stdin"
        sh 'docker push flaviassantos/easyfit:1.0.0'
    }
}

def deployApp() {
    echo 'deploying the application...'
}

return this