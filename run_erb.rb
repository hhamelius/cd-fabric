#!/usr/bin/ruby
# Quick and dirty template processing script. It takes
# as an argument the name of the first template script
# and then executes it to standard output.

require "erb"

text = File.read(ARGV[0]).gsub(/^  /, '')
props = ARGV[1]
props = eval(props)
props.each_pair do |key,value|
	key_no_dots = key.gsub(".", "_")
	ivar_name = "@#{key_no_dots}"
    instance_variable_set(ivar_name, value)
end
template = ERB.new(text, 0, "%<>")

result = template.result
puts result
