pipeline {
  agent {
    kubernetes {
      yamlFile 'jenkins-pod.yml'
    }
  }
  stages {
    stage ('build and push') {
      steps {
         checkout scm
         def customImage = docker.build("my-image:${env.BUILD_ID}")
         customImage.push()
         customImage.push('latest')
      }
    }
  }
}
