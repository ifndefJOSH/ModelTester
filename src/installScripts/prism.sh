#!/bin/sh

set -e

installPrism() {
	git clone https://github.com/prismmodelchecker/prism prism
	cd prism/prism
	git checkout v4.5
	make -j$(nproc --all)
	make install
	echo "[INFO]: Finished installing PRISM"
}

if [ -d prism ];
then
	echo "[INFO] PRISM already appears to be installed!"
else
	installPrism
fi
