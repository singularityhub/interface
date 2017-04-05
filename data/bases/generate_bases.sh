#!/bin/sh

if [ -z "$1" ]; then
    HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
else
    HERE=$1
fi

echo $HERE

singularity create $HERE/ubuntu.img
singularity import $HERE/ubuntu.img docker://ubuntu:latest
singularity create $HERE/centos.img
singularity import $HERE/centos.img docker://centos:latest
singularity create $HERE/debian.img
singularity import $HERE/debian.img docker://debian:latest
singularity create $HERE/alpine.img
singularity import $HERE/alpine.img docker://alpine:latest
singularity create $HERE/busybox.img
singularity import $HERE/busybox.img docker://busybox:latest
