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
        DISCORD_ID   = "smashed-alerts"
        COMPOSE_FILE = "docker-compose-swarm.yml"

        BUILD_CAUSE = getBuildCause()
        VERSION = getVersion("${GIT_BRANCH}")
        GIT_ORG = getGitGroup("${GIT_URL}")
        GIT_REPO = getGitRepo("${GIT_URL}")
        REPO_ORG = "public"
    }
    stages {
        stage('Init') {
            steps {
                echo "\n--- Build Details ---\n" +
                        "GIT_URL:       ${GIT_URL}\n" +
                        "JOB_NAME:      ${JOB_NAME}\n" +
                        "BUILD_CAUSE:   ${BUILD_CAUSE}\n" +
                        "GIT_BRANCH:    ${GIT_BRANCH}\n" +
                        "VERSION:       ${VERSION}\n" +
                        "GIT_ORG:       ${GIT_ORG}\n" +
                        "GIT_REPO:      ${GIT_REPO}\n"
                verifyBuild()
                sendDiscord("${DISCORD_ID}", "Pipeline Started by: ${BUILD_CAUSE}")
            }
        }
        stage('Dev Deploy') {
            when {
                allOf {
                    not { branch 'master' }
                }
            }
            environment {
                BUILD_TAG = "${REPO_ORG}/${GIT_REPO}:${VERSION}"
            }
            steps {
                echo "\n--- Starting Dev Build ---\n" +
                        "VERSION:       ${VERSION}\n" +
                        "GIT_ORG:       ${GIT_ORG}\n" +
                        "GIT_BRANCH:    ${GIT_BRANCH}\n" +
                        "BUILD_TAG:     ${BUILD_TAG}\n"
                sendDiscord("${DISCORD_ID}", "Dev Build Started for: ${BUILD_TAG}")
                buildPush("${BUILD_TAG}")
                sendDiscord("${DISCORD_ID}", "Dev Push Finished for: ${BUILD_TAG}")
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
                BUILD_TAG = "${REPO_ORG}/${GIT_REPO}:${VERSION}"
            }
            steps {
                echo "\n--- Starting Prod Build ---\n" +
                        "VERSION:       ${VERSION}\n" +
                        "GIT_ORG:       ${GIT_ORG}\n" +
                        "GIT_BRANCH:    ${GIT_BRANCH}\n" +
                        "BUILD_TAG:     ${BUILD_TAG}\n"
                sendDiscord("${DISCORD_ID}", "Prod Build Started for: ${BUILD_TAG}")
                buildPush("${BUILD_TAG}")
                sendDiscord("${DISCORD_ID}", "Prod Push Finished for: ${BUILD_TAG}")
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
