def readVersion() {
    echo 'reading the application version...'
    def latestVersion = sh(returnStdout: true, script: 'git describe --tags --abbrev=0 --match *.*.* 2> /dev/null || echo 0.0.0').trim()
    env.TAG = latestVersion
    echo "version: ${TAG}"
}


def buildImage() {
    echo "building the docker image..."
    withCredentials([usernamePassword(credentialsId: 'docker-hub-repo', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
        sh "docker build -t flaviassantos/easyfit:${TAG} ."
        sh "echo $PASS | docker login -u $USER --password-stdin"
        sh "docker push flaviassantos/easyfit:${TAG}"
    }
}

def deployApp() {
    echo 'deploying the application...'
}

return this