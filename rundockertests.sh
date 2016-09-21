#!/bin/bash
# Run the tests locally using the qgis testing environment docker
# Note: to run the tests you need to download websdk from a github
#       private repo, you need an authorised id_rsa to do that and
#       the id_rsa key must be copied to the travis_setup folder
#       before launching this script.


PLUGIN_NAME="webappbuilder"

docker rm -f qgis-testing-environment

# replace latest with master if you wish to test on master, latest is
# latest supported Boundless release

QGIS_VERSION_TAG=release

docker pull elpaso/qgis-testing-environment:$QGIS_VERSION_TAG

docker run -d  --name qgis-testing-environment  -e DISPLAY=:99 -v /tmp/.X11-unix:/tmp/.X11-unix -v `pwd`:/tests_directory elpaso/qgis-testing-environment:$QGIS_VERSION_TAG


docker exec -it qgis-testing-environment sh -c "qgis_setup.sh $PLUGIN_NAME"

# SSH key
docker exec -it qgis-testing-environment sh -c "mkdir -p /root/.ssh"
docker exec -it qgis-testing-environment sh -c "printf 'Host *\n\tStrictHostKeyChecking no\n\tUserKnownHostsFile=/dev/null\n' > /root/.ssh/config"
docker exec -it qgis-testing-environment sh -c "cp /tests_directory/travis_setup/id_rsa /root/.ssh/id_rsa"
docker exec -it qgis-testing-environment sh -c "chmod 600 /root/.ssh/id_rsa"

# Install the plugin
docker exec -it qgis-testing-environment sh -c "pip install paver"
docker exec -it qgis-testing-environment sh -c "cd /tests_directory && paver setup"
docker exec -it qgis-testing-environment sh -c "ln -s /tests_directory/$PLUGIN_NAME /root/.qgis2/python/plugins/$PLUGIN_NAME"

# run the tests
docker exec -it qgis-testing-environment sh -c "qgis_testrunner.sh webappbuilder.tests.layerstest.run_tests"
docker exec -it qgis-testing-environment sh -c "qgis_testrunner.sh webappbuilder.tests.symbologytest.run_tests"
docker exec -it qgis-testing-environment sh -c "qgis_testrunner.sh webappbuilder.tests.widgetstest.run_tests"
docker exec -it qgis-testing-environment sh -c "qgis_testrunner.sh webappbuilder.tests.settingstest.run_tests"
docker exec -it qgis-testing-environment sh -c "qgis_testrunner.sh webappbuilder.tests.appdefvaliditytest.run_tests"
