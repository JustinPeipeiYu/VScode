# creates new users
# adds user to root group to give it administrator access
#! /bin/bash
useradd -m jane
sudo passwd jane
sudo usermod -aG wheel jane
