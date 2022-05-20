#!/bin/sh

set -e

source prism.sh

installStaminaPrismOne() {
	dir=$(pwd)
	git clone https://github.com/fluentverification/stamina stamina-one
	git checkout d8dd29583571d0d39226b699a08d845ca9168b0c
	cd stamina-one/stamina
	make -j$(nproc --all) PRISM_HOME=$dir/prism/prism
	echo "[INFO] Finished installing Stamina 1.0"
}
