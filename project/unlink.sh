#!/usr/bin/env bash

# Create backup before removal
mkdir -p "./backup/$(date +%Y-%m-%d-%H-%M-%S)" && cp -a "./rp" "$_"

sudo umount ./rp

rm -rf ./rp