// Powered by Infostretch 

timestamps {

node () {

	stage ('Datafeed - Checkout') {
 	 checkout([$class: 'GitSCM', branches: [[name: '*/main']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: '2d203f30-8573-4625-ad33-33d5a2748d9f', url: 'https://github.com/agrosshans/datafeed.git']]]) 
	}
	stage ('Datafeed - Build') {
 	
// Unable to convert a build step referring to "hudson.plugins.ws__cleanup.PreBuildCleanup". Please verify and convert manually if required.		// Shell build step
sh """ 
if [ -d /var/lib/jenkins/workspace/Datafeed ]; then
  cd /var/lib/jenkins/workspace/Datafeed
  /bin/rpmbuild --sign --define '_topdir /var/lib/jenkins/workspace/Datafeed' -ba -vv SPECS/datafeed.spec
fi 
 """ 
	}
}
}