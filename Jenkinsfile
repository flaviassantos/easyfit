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
        stage("init") {
            steps {
                script {
                    gv = load "script.groovy"
                }
            }
        }
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
                    gv.provisionServer()
                }
            }
        }
        stage("deploy") {
            steps {
                script {
                    //gv.deployApp()
                }
            }
        }
    }
}