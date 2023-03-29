#!/usr/bin/env ash

REQUIREMENTS_IN="../requirements.txt"

echo "wheel" > requirements.txt
# get midas line from requirements.txt but exclude lines beginning with a hashtag (-> comments)
echo $(cat ${REQUIREMENTS_IN} | grep midas-mosaik | grep -E "^[^#]") >> requirements.txt

REPOSITORY="registry.gitlab.com/pyrate-project/analyse/midas-mosaik-baseimage"
MIDAS_MOSAIK_VERSION=$(cat ${REQUIREMENTS_IN} | grep midas-mosaik | sed -r 's/midas-mosaik *~*>*<*=* *//')
echo "midas-mosaik version: ${MIDAS_MOSAIK_VERSION}"
echo ${MIDAS_MOSAIK_VERSION}>midas_version.txt

docker manifest inspect ${REPOSITORY}:${MIDAS_MOSAIK_VERSION} > /dev/null
EXIT_CODE=$?
# if EXIT_CODE == 1, this docker image tag doesn't exist, yet -> build and push it
if [ $EXIT_CODE -eq 1 ]; then
    docker build -t ${REPOSITORY}:${MIDAS_MOSAIK_VERSION} . -f Dockerfile.midas_base
    docker push ${REPOSITORY}:${MIDAS_MOSAIK_VERSION}
fi

