from fabric.api import run, env, local, lcd, cd, put
from fabric.decorators import task, runs_once

env.hosts = ['henham@172.16.54.128']
releasesDir = '/tmp/localReleases'
targetDir = '/tmp/targetReleases'

@task
@runs_once
def deploy(group, webapp, version):
	print 'hepp'
	#fetch_artifacts()

#------- Fetch artifacts -------#
@task
@runs_once
def fetch_artifacts(group, artifact, version):
	fetch_properties(artifact)
	fetch_nexus_artefact(group, artifact, version)
	
def fetch_nexus_artefact(group, artifact, version):
	grp=group.replace('.','/')
	warfile = '{0}-{1}.war'.format(artifact, version)
	get_war_command = 'wget http://maven-repo.aftonbladet.se:8081/nexus/content/repositories/releases/{0}/{1}/{2}/{3}'.format(grp, artifact, version, warfile)
	with lcd(releasesDir):
		local(get_war_command)

def fetch_properties(webapp):
    # mock implementation 
	local('mkdir -p {0}/WEB-INF/classes'.format(releasesDir))
	local('cp hockey-web.properties {0}/WEB-INF/classes'.format(releasesDir))

#------- Update artifact -------#
@task
@runs_once
def update_artifact(webapp):		
	update_command = 'jar -uf {0} -C WEB-INF/classes /tmp/{0}.properties'.format(webapp)
	with lcd(releasesDir):
		local(update_command)

#------- Push artifacts -------#
@task
def push_artifacts(webapp, version):
	run('mkdir -p {0}'.format(targetDir))
	warfile = '{0}/{1}-{2}.war'.format(releasesDir, webapp, version)
	put(warfile, targetDir)

#------ Restart Tomcat -------#
tomcat_home='not set'

@task
def get_tomcat_home():
	tomcat_home = run('echo $TOMCAT_HOME')

def stop_tomcat():
	with cd(tomcat_home):
		run('./init.tomcat stop $TOMCAT_HOME')

def start_tomcat():
	with cd(TOMCAT_HOME):
		run('./init.tomcat start', pty=False)

def undeploy(webapp):
	run('rm -rf {0}/webapps/{1}'.format(tomcat_home, webapp)
	run('rm {0}/webapps/{1}.war'.format(tomcat_home, webapp)
	run('rm -rf {0}/work/Catalina/localhost/{1}'.format(tomcat_home, webapp)	

#put('/tmp/assets.tgz', '/tmp/assets.tgz')
#    with cd('/var/www/myapp/'):
#        run('tar xzf /tmp/assets.tgz')