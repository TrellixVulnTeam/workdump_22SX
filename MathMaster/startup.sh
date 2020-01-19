#!/usr/bin/env bash

echo "Enter root password: " && read passw
echo $passw | sudo -S apt update -y
echo $passw | sudo -S apt upgrade -y
echo "Press enter to continue..." && read
