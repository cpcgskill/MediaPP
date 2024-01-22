.PHONY: clean build

clean:
	rm -rf "build"

build: clean
	echo "Build Start"
	mkdir build
	#python setup.py build
	#python setup.py bdist_msi
	python build.py
	mkdir ./build/MediaPP/
	mv ./build/out/ ./build/MediaPP/MediaPP/
	7z a -SFX -mx9 ./build/MediaPP.exe ./build/MediaPP/*
	# 7z -tzip a ./build/MediaPP.zip ./build/MediaPP/*
	echo "Build End"