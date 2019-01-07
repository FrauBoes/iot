#!/usr/bin/env bash

# Allow remote access to Dev folder on rp
sudo sshfs -o allow_other,defer_permissions pi@rpjulia.local:Dev ./rp