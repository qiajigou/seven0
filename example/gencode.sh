#!/bin/bash

protoc --plugin=protoc-gen-custom=../seven0/seven0.py --custom_out=./build r2d2.proto
