from fabric.api import run, env, local, lcd, cd, put
from fabric.decorators import task, runs_once

env.hosts = ['henham@172.16.54.129']
tomcat_home='/opt/generic_tomcat'
tomcat_script='/etc/init.d/generic_tomcat'

releasesDir = '/tmp/localReleases'

@task
def deploy(group, webapp, version):
	run(fetch_nexus_artifact(group, webapp, version))
	run(fetch_properties(webapp))

	run(tomcat('stop'))
	run(deploy_properties(webapp))  # puts it in tomcta classpath
	run(redeploy_artifact(webappp))
	run(tomcat('start'))

#------- Fetch artifacts -------#	
def fetch_nexus_artefact(group, artifact, version):
	grp=group.replace('.','/')
	warfile = '{0}-{1}.war'.format(artifact, version)
	get_war_command = 'wget http://maven-repo.aftonbladet.se:8081/nexus/content/repositories/releases/{0}/{1}/{2}/{3}'.format(grp, artifact, version, warfile)
	with lcd(releasesDir):
		local(get_war_command)

def fetch_properties(webapp):
    # TODO mock implementation, needs proper implementation
	local('mkdir -p {0}/WEB-INF/classes'.format(releasesDir))
	local('cp hockey-web.properties {0}/WEB-INF/classes'.format(releasesDir))

#------- Update artifact -------#
@task
def deploy_properties(webapp)
	run('cp {0}/{1}.properties {2}/lib/'.format(releasesDir, webapp, tomcat_home))

def inject_properties(webapp):		
	update_command = 'jar -uf {0} -C WEB-INF/classes /tmp/{0}.properties'.format(webapp)
	with lcd(releasesDir):
		local(update_command)

#------- Push artifacts -------#
@task
def push_artifacts(webapp, version):
	run('mkdir -p {0}'.format(targetDir))
	warfile = '{0}/{1}-{2}.war'.format(releasesDir, webapp, version)
	put(warfile, targetDir)

#------- Restart Tomcat -------#
def tomcat(action):
	run('{0} {1}'.format(tomcat_script, action))

def redeploy_artifact(webapp)
	undeploy_artifact(webapp)
	deploy_artifact(webapp)

def undeploy_artifact(webapp):
	run('rm -rf {0}/webapps/{1}'.format(tomcat_home, webapp)
	run('rm {0}/webapps/{1}.war'.format(tomcat_home, webapp)
	run('rm -rf {0}/work/Catalina/localhost/{1}'.format(tomcat_home, webapp)	

def deploy_artifact(webapp):
	cp(targetDir, '{0}/webapps/'.format(tomcat_home)
