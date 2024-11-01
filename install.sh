#!/bin/bash

cp vega.py /data/data/com.termux/files/usr/bin
echo "export PATH=\"\$PATH:/data/data/com.termux/files/usr/bin\"" >> ~/.bashrc
source ~/.bashrc
echo "Program has installed!"