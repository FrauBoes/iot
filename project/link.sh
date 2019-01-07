#!/usr/bin/env bash

# ps aux | grep sshfs
# sudo kill -9 PID
# sudo diskutil umount force project

# Allow remote access to Dev folder on rp
sudo sshfs -o allow_other,defer_permissions pi@rpjulia.local:Dev ./rp