# Use the official image as a parent image 
FROM rocker/r-ver:4.4.2

# Install Python and radian
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install radian

# Install additional R packages
#RUN R -e "install.packages('tidyverse', repos='http://cran.rstudio.com/')"

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*