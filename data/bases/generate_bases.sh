#!/bin/sh

if [ -z "$1" ]; then
    HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
else
    HERE=$1
fi

echo $HERE

singularity build $HERE/ubuntu.simg docker://ubuntu:latest
singularity build $HERE/centos.simg docker://centos:latest
singularity build $HERE/debian.simg docker://debian:latest
singularity build $HERE/alpine.simg docker://alpine:latest
singularity build $HERE/busybox.simg docker://busybox:latest
