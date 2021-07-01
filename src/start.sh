#!/bin/bash
~/.steam/bin32/steam-runtime/run.sh ~/.steam/steam/steamapps/common/SteamVR/bin/vrstartup.sh &
sleep 5s;
python tracker_pose.py
