.PHONY: clean build

clean:
	rm -rf "build"

build: clean
	echo "Build Start"
	mkdir build
	python setup.py build
	mkdir ./build/tmp/
	mv ./build/exe.win-amd64-3.8/ ./build/tmp/MediaPP/
	7z a -SFX -mx9 -o ./out ./build/MediaPP.exe ./build/tmp/*
	echo "Build End"