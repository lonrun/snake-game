#!/bin/bash

export sparrowCliVersion=bc184bb8
curl https://antsys-sparrow-data.cn-shanghai-alipay-office.oss-alipay.aliyuncs.com/sparrow/public/sparrow-cli/sparrow-cli-${sparrowCliVersion}.linux.tar.gz -o sparrow-cli.tar.gz && tar -zxvf sparrow-cli.tar.gz && rm sparrow-cli.tar.gz

echo "current sparrow cli dir is sparrow-cli-${sparrowCliVersion}"
if [ -d sparrow-cli-${sparrowCliVersion} ]; then
 echo "change sparrow cli dir"
 mv sparrow-cli-${sparrowCliVersion} sparrow-cli
fi

export PATH=${PWD}/sparrow-cli:$PATH
echo $PATH

which sparrow
sparrow version info
