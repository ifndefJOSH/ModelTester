#!/bin/sh

set -e

source prism.sh

installStamina() {
	dir=$(pwd)
	git clone https://github.com/fluentverification/stamina stamina
	cd stamina
	make -j$(nproc --all) PRISM_HOME=$dir/prism/prism
	echo "[INFO]: Finished installing STAMINA"
}

setEnvironmentVariable() {
	touch ~/.staminarc
	echo "export_JAVA_OPTIONS=-Xmx12288m" >> ~/.staminarc
	echo "export PRISM_HOME=$(pwd)/prism/prism" >> ~/.staminarc
	echo "export STAMINA_HOME=$(pwd)/stamina" >> ~/.staminarc
}

installStamina
setEnvironmentVariable
