.PHONY: clean build

clean:
	rm -rf "build"

build: clean
	echo "Build Start"
	mkdir build
	python build.py
	mkdir ./build/MediaPP/
	mv ./build/out/ ./build/MediaPP/MediaPP/
	7z a -SFX -mx9 ./build/MediaPP.exe ./build/MediaPP/*
	echo "Build End"