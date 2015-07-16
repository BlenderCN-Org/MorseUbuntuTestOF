#!bin/bash
cd ~/morse/build/
sudo make install
cd ~/mysim
gnome-terminal -x sh -c "cd ~;morse run mysim; bash";sleep 50;exit;
# sleep 7;python3 droneTraj.py

#sleep 30;exit;
