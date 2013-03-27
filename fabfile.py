from fabric.api import run, env, local, lcd, cd, put, sudo
from fabric.decorators import task, runs_once

#env.hosts = ['henham@172.16.54.129'] # -H
#tomcat_name = 'generic_tomcat'       # argv

tomcat_home='/opt/{0}'.format(env.tomcat_name)
tomcat_script='/etc/init.d/{0}'.format(env.tomcat_name)
app_lib='opt/{0}/lib'.format(env.tomcat_name)
releasesDir = '/tmp/localReleases'

#------- Main Deploy Task -------#
@task
def deploy(group, webapp, version):
	# trigger a puppet update
	#sudo('puppet agent -t --confdir /etc/ab/puppet')
	sudo('puppet apply --modulepath /puppet/puppet/modules /puppet/puppet/manifests/site.pp --certname ab-generic-app1.aftonbladet.se')
	fetch_nexus_artefact(group, webapp, version)

	tomcat('stop')
	deploy_properties(webapp)  # put props into tomcat classpath
	redeploy_artifact(webapp, version)
	tomcat('start')

#------- Fetch artifacts -------#	
def fetch_nexus_artefact(group, artifact, version):
	grp=group.replace('.','/')
	warfile = '{0}-{1}.war'.format(artifact, version)
	run('mkdir -p {0}'.format(releasesDir))
	run('wget http://maven-repo.aftonbladet.se:8081/nexus/content/repositories/releases/{0}/{1}/{2}/{3} -O {4}/{3}'.format(grp, artifact, version, warfile, releasesDir))

#------- Update artifact -------#
@task
def deploy_properties(webapp):
	sudo( 'cp /home/wwwadm/properties/{0}.properties_latest /home/wwwadm/properties/{0}.properties'.format(webapp, app_lib) )

#------- Restart Tomcat -------#
def tomcat(action):
	sudo('{0} {1}'.format(tomcat_script, action))

# ------ Deploy/Undeploy Artifact -------#
def redeploy_artifact(webapp, version):
	undeploy_artifact(webapp)
	deploy_artifact(webapp, version)

def undeploy_artifact(webapp):
	sudo('if [ -f {0}/webapps/{1} ]; then rm {0}/webapps/{1}; fi'.format(tomcat_home, webapp))
	sudo('if [ -d {0}/webapps/{1} ]; then rm {0}/webapps/{1}.war; fi'.format(tomcat_home, webapp))
	sudo('if [ -d {0}/work/Catalina/localhost/{1} ]; then rm -rf {0}/work/Catalina/localhost/{1}; fi'.format(tomcat_home, webapp))

def deploy_artifact(webapp, version):
	sudo('cp {0}/{1}-{2}.war {3}/webapps/{1}.war'.format(releasesDir, webapp, version, tomcat_home))
