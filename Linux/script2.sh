# creates a new user
# gives new user login password
# adds user to root group to give it administrator access
useradd jane
sudo passwd
sudo usermod -aG root jane
