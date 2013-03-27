require 'erb'

# /home/git
git_home = "/tmp/git"

def process_erb(webapp)
	template = ERB.new(IO.readlines("#{git_home}/#{webapp/}/#{webapp/}.properties.erb").to_s

	file_name = "#{webapp/}.properties"
	f = File.new("#{file_name}",'w')

	dataset = {:test, "false"}

	f.puts(template.result(binding))
	f.close
end

def render()
    ERB.new(@template).result(binding)
 end



