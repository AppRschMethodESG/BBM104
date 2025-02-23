#!/bin/bash

# Run the commands below **once** to 

#   1. install R (instructions from https://cran.r-project.org/bin/linux/ubuntu/)
#
#   2. install Ubuntu packages harfbuzz, libfribidi, etc
#      - harfbuzz is primarily a text shaping library used for rendering text
#      - fribidi is a library that provides support for the Unicode Bidirectional Algorithm (Bidi)
#
#   3. create the R_Library directory and add lines to the end of ~/.bashrc 
#
#   4. install radian Terminal and Jupyter (if you know how to use them)
#
# Use a Terminal to execute the following commands:

#================================================================

# update indices
sudo apt update -qq

# install two helper packages we need
sudo apt install --no-install-recommends software-properties-common dirmngr

# add the signing key (by Michael Rutter) for these repos
# To verify key, run gpg --show-keys /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc 
# Fingerprint: E298A3A825C0D65DFD57CBB651716619E084DAB9
wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | sudo tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc

# add the repo from CRAN -- lsb_release adjusts to 'noble' or 'jammy' or ... as needed
sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"

# install R itself
sudo apt install -y --no-install-recommends r-base

sudo apt-get update
# Install Ubuntu packages harfbuzz, libfribidi, etc; then find the installed locations
sudo apt-get install -y libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev libssl-dev libxml2-dev &&
dpkg-query -L libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev libssl-dev libxml2-dev
#sudo apt-get install -y libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev &&
#dpkg-query -L libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev

# Create the R_Library directory and add lines to the end of ~/.bashrc  
mkdir -p "$(pwd)/R_Library"

# Add the following lines to the end of ~/.bashrc  
echo '

# Add R Library to LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$(pwd)/R_Library:$LD_LIBRARY_PATH

# Set PKG_CONFIG_PATH to ensure the compiler can find the FreeType headers
export PKG_CONFIG_PATH="/usr/local/lib/x86_64-linux-gnu/pkgconfig:/usr/local/lib/pkgconfig:/usr/local/share/pkgconfig:/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/lib/pkgconfig:/usr/share/pkgconfig"

' >> ~/.bashrc

# Source the ~/.bashrc file to apply the changes
source ~/.bashrc

# Upgrade pip and install radian
python3 -m pip install --upgrade pip
pip3 install -U radian

# Add the following lines to the end of ~/.bashrc  
echo '

# Alias for radian
alias r="radian"

' >> ~/.bashrc

# Source the ~/.bashrc file to apply the changes
source ~/.bashrc

# Call .Rmd file to install packages 
Rscript SetupRunOnce.R
