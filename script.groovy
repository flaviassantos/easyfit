def provisionServer(){
                        dir('terraform') {
                        sh "terraform init"
                        sh "terraform apply --auto-approve"
                        EC2_PUBLIC_IP = sh(
                            script: "terraform output ec2_public_ip",
                            returnStdout: true
                        ).trim()
                    }
}


def deployApp() {
    echo 'deploying the application...'
    echo "waiting for EC2 server to initialize..."
    sleep(time: 90, unit: "SECONDS")

    echo 'deploying docker image to EC2...'
    echo "${EC2_PUBLIC_IP}"

    def shellCmd = "bash ./server-cmds.sh ${IMAGE_NAME} ${DOCKER_CREDS_USR} ${DOCKER_CREDS_PSW}"
    def ec2Instance = "ec2-user@${EC2_PUBLIC_IP}"

    sshagent(['server_ssh_key_pair']) {
       sh "scp -o StrictHostKeyChecking=no server-cmds.sh ${ec2Instance}:/home/ec2-user"
       sh "scp -o StrictHostKeyChecking=no mongodb_docker_compose.yaml ${ec2Instance}:/home/ec2-user"
       sh "ssh -o StrictHostKeyChecking=no ${ec2Instance} ${shellCmd}"
}

return this