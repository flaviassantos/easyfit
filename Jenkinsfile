#!/usr/bin/env groovy

library identifier: 'jenkins-shared-library@master', retriever: modernSCM(
        [$class: 'GitSCMSource',
         remote: 'https://github.com/flaviassantos/jenkins-shared-library.git',
         credentialsId: 'github-credentials'
        ]
)

def gv

pipeline {
    agent any
    environment {
        DOCKER_REPO = "flaviassantos/easyfit"
    }
    stages {
        stage("test") {
            steps {
                script {
                    echo "testing"
                }
            }
        }
        stage('read version') {
            steps {
                script {
                    readVersion()
                }
            }
        }
        stage("build image") {
            environment {
                IMAGE_NAME = "${DOCKER_REPO}:${env.TAG}"
            }
            steps {
                script {
                    buildImage(env.IMAGE_NAME)
                    dockerLogin()
                    dockerPush(env.IMAGE_NAME)
                }
            }
        }
        stage('provision server') {
            environment {
                AWS_ACCESS_KEY_ID = credentials('jenkins_aws_access_key_id')
                AWS_SECRET_ACCESS_KEY = credentials('jenkins_aws_secret_access_key')
                TF_VAR_env_prefix = 'test'
            }
            steps {
                script {
                    dir('terraform') {
                        sh "terraform init"
                        sh "terraform apply --auto-approve"
                        EC2_PUBLIC_IP = sh(
                            script: "terraform output ec2_public_ip",
                            returnStdout: true
                        ).trim()
                    }
                }
            }
        }
        stage('deploy') {
            environment {
                DOCKER_CREDS = credentials('docker-hub-repo')
                IMAGE_NAME = "${DOCKER_REPO}:${env.TAG}"
            }
            steps {
                script {
                   echo "waiting for EC2 server to initialize..."
                   sleep(time: 90, unit: "SECONDS")

                   echo 'deploying docker image to EC2...'
                   echo "${EC2_PUBLIC_IP}"

                   def shellCmd = "bash ./server-cmds.sh ${IMAGE_NAME} ${DOCKER_CREDS_USR} ${DOCKER_CREDS_PSW}"
                   def ec2Instance = "ec2-user@${EC2_PUBLIC_IP}"
                   echo "ok"
                   sshagent(['server_ssh_key_pair']) {
                       sh "scp -o StrictHostKeyChecking=no server-cmds.sh ${ec2Instance}:/home/ec2-user"
                       sh "scp -o StrictHostKeyChecking=no mongodb_docker_compose.yaml ${ec2Instance}:/home/ec2-user"
                       sh "ssh -o StrictHostKeyChecking=no ${ec2Instance} ${shellCmd}"
                   }
                }
            }
        }
    }
}