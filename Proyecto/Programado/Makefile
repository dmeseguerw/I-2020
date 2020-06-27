all: install_dep app clean

install_dep:
	sudo sh install_dep.sh

app:
	python3 App.py

clean:
	rm Images/* Images_Global/*
	rm -r Waves/* CSV_Files/*