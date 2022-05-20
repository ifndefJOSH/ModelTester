#!/bin/sh

set -e

installPrism() {
	rm -rf prism
	git clone https://github.com/prismmodelchecker/prism prism
	cd prism/prism
	git checkout v4.5
	make -j$(nproc --all)
	make install
	echo "[INFO]: Finished installing PRISM"
}

installPrism
