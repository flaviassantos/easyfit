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
        stage("deploy") {
            steps {
                script {
                    echo "deploying"
                    //gv.deployApp()
                }
            }
        }
    }
}