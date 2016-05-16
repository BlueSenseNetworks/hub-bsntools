clean:
	rm -rf out

test:
	python -m unittest discover -s tests -p '*.py' -v

at: clean
	vagrant up && vagrant ssh -- "cd /vagrant && mkdir out && sudo lettuce --with-xunit --xunit-file=out/test_results.xml -v 3"; vagrant destroy -f
