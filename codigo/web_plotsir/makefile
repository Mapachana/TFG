all: launch_dash launch_flask

launch_dash:
	cd app && python3 index_dash.py

launch_flask:
	cd app/app && flask run

clean_data_files:
	cd app/app && rm -rf fichero_ajuste/* files/*

build_docker:
	$(MAKE) clean_data_files
	docker-compose build

run_docker:
	docker run -t -p 5000:5000 -p 8050:8050 mapachana/plotsir:latest

install_deps:
	pip install -r requirements.txt

