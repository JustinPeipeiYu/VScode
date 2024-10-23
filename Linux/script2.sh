# creates new users
# adds user to root group to give it administrator access
#! /bin/bash
useradd -m jane
sudo passwd
sudo usermod -aG root jane
