#!/usr/bin/env groovy

@Library('jenkins-libraries')_

pipeline {
    agent {
        label 'manager'
    }
    options {
        buildDiscarder(logRotator(numToKeepStr:'5'))
        timeout(time: 1, unit: 'HOURS')
    }
    environment {
        DEV_PORT     = '10101'
        DEV_PORT2    = '10102'
        PROD_PORT    = '10103'
        PROD_PORT2   = '10104'
        DISCORD_ID   = "smashed-alerts"
        COMPOSE_FILE = "docker-compose-swarm.yml"

        BUILD_CAUSE = getBuildCause()
        VERSION = getVersion("${GIT_BRANCH}")
        GIT_ORG = getGitGroup("${GIT_URL}")
        GIT_REPO = getGitRepo("${GIT_URL}")
        NFS_HOST = getOvhNfsInfo('host')
        NFS_ID   = getOvhNfsInfo('id')
        NFS_BASE = "/export/ftpbackup/${NFS_ID}/docker/nfs"

        BASE_NAME = "${GIT_ORG}-${GIT_REPO}"
        SERVICE_NAME = "${BASE_NAME}"
    }
    stages {
        stage('Init') {
            steps {
                echo "\n--- Build Details ---\n" +
                        "GIT_URL:       ${GIT_URL}\n" +
                        "JOB_NAME:      ${JOB_NAME}\n" +
                        "SERVICE_NAME:  ${SERVICE_NAME}\n" +
                        "NFS_HOST:      ${NFS_HOST}\n" +
                        "NFS_BASE:      ${NFS_BASE}\n" +
                        "BASE_NAME:     ${BASE_NAME}\n" +
                        "BUILD_CAUSE:   ${BUILD_CAUSE}\n" +
                        "GIT_BRANCH:    ${GIT_BRANCH}\n" +
                        "VERSION:       ${VERSION}\n"
                verifyBuild()
                sendDiscord("${DISCORD_ID}", "Pipeline Started by: ${BUILD_CAUSE}")
                getConfigs("${SERVICE_NAME}")   // use this to get service configs from deploy-configs
            }
        }
        stage('Dev Deploy') {
            when {
                allOf {
                    not { branch 'master' }
                }
            }
            environment {
                ENV_FILE = "deploy-configs/services/${SERVICE_NAME}/dev.env"
                STACK_NAME = "dev_${BASE_NAME}"
                DOCKER_PORT = "${DEV_PORT}"
                FTP_PORT = "${DEV_PORT2}"
                NFS_DIRECTORY = "${NFS_BASE}/${STACK_NAME}"
            }
            steps {
                echo "\n--- Starting Dev Deploy ---\n" +
                        "STACK_NAME:    ${STACK_NAME}\n" +
                        "DOCKER_PORT:   ${DOCKER_PORT}\n" +
                        "FTP_PORT:      ${FTP_PORT}\n" +
                        "NFS_HOST:      ${NFS_HOST}\n" +
                        "NFS_DIRECTORY: ${NFS_DIRECTORY}\n" +
                        "ENV_FILE:      ${ENV_FILE}\n"
                sendDiscord("${DISCORD_ID}", "Dev Deploy Started")
                setupOvhNfs("${STACK_NAME}")
                stackPush("${COMPOSE_FILE}")
                stackDeploy("${COMPOSE_FILE}", "${STACK_NAME}")
                sendDiscord("${DISCORD_ID}", "Dev Deploy Finished")
            }
        }
        stage('Prod Deploy') {
            when {
                allOf {
                    branch 'master'
                    triggeredBy 'UserIdCause'
                }
            }
            environment {
                ENV_FILE = "deploy-configs/services/${SERVICE_NAME}/prod.env"
                STACK_NAME = "prod_${BASE_NAME}"
                DOCKER_PORT = "${PROD_PORT}"
                FTP_PORT = "${PROD_PORT2}"
                NFS_DIRECTORY = "${STACK_NAME}"
            }
            steps {
                echo "\n--- Starting Prod Deploy ---\n" +
                        "STACK_NAME:    ${STACK_NAME}\n" +
                        "DOCKER_PORT:   ${DOCKER_PORT}\n" +
                        "FTP_PORT:      ${FTP_PORT}\n" +
                        "NFS_HOST:      ${NFS_HOST}\n" +
                        "NFS_DIRECTORY: ${NFS_DIRECTORY}\n" +
                        "ENV_FILE:      ${ENV_FILE}\n"
                sendDiscord("${DISCORD_ID}", "Prod Deploy Started")
                setupNfs("${STACK_NAME}")
                stackPush("${COMPOSE_FILE}")
                stackDeploy("${COMPOSE_FILE}", "${STACK_NAME}")
                sendDiscord("${DISCORD_ID}", "Prod Deploy Finished")
            }
        }
    }
    post {
        always {
            cleanWs()
            script { if (!env.INVALID_BUILD) {
                sendDiscord("${DISCORD_ID}", "Pipeline Complete: ${currentBuild.currentResult}")
            } }
        }
    }
}
