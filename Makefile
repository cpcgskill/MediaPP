.PHONY: clean build

clean:
	rm -rf "build"

build: clean
	echo "Build Start"
	mkdir build
	python setup.py build
	#python setup.py bdist_msi
	mkdir ./build/tmp/
	mv ./build/exe.win-amd64-3.10/ ./build/tmp/MediaPP/
	7z a -SFX -mx9 ./build/MediaPP.exe ./build/tmp/*
	echo "Build End"