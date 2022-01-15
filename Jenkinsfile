pipeline {
  agent {
    kubernetes {
      yamlFile 'jenkins-pod.yaml'
    }
  }
  environment {
    registry = "thecase/neurio-influx"
  }
  stages {
    stage('Build and Publish') {
      environment {
        registryCredential = 'dockerhub'
      }
      steps {
        script { 
          sh 'ls -la /usr/local/bin'
          def appimage = docker.build registry + ":$BUILD_NUMBER"
          docker.withRegistry('', registryCredential) {
            appimage.push()
            appimage.push('latest')
          }
        }
      }
    }
    /*
      stage ('Deploy') {
           steps {
               script{
                   def image_id = registry + ":$BUILD_NUMBER"
                   sh "ansible-playbook  playbook.yml --extra-vars \"image_id=${image_id}\""
               }
           }
       }
   */
  }
}
