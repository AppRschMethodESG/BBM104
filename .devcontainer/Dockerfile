# Use the official image as a parent image 
FROM rocker/r-ver:4.4.2

# Install Python and radian
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Create a virtual environment and install radian
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install radian

# Set the virtual environment as the default Python environment
ENV PATH="/opt/venv/bin:$PATH"

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install git
RUN apt-get update && apt-get install -y git

# Create the vscode user and set it as the default user
RUN useradd -ms /bin/bash vscode

# Grant sudo privileges to the vscode user
RUN apt-get update && apt-get install -y sudo && \
    echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER vscode

# Set the library path, create the directory, and install the packages
# Set the library path, create the directory, set permissions, and install the packages

#RUN R -e 'print(getwd()); repo_path <- "/workspaces/BBM104"; lib_path <- file.path(repo_path, "R_Library"); dir.create(lib_path, recursive = TRUE, showWarnings = FALSE); system(paste("sudo chown -R vscode:vscode", lib_path)); system(paste("sudo chmod -R 777", lib_path)); .libPaths(c(lib_path, .libPaths())); install.packages(c("tidyverse"), lib=lib_path, repos="http://cran.rstudio.com/")'

RUN R -e 'print(getwd()); repo_path <- "/workspaces/BBM104"; lib_path <- file.path(repo_path, "R_Library"); dir.create(lib_path, recursive = TRUE, showWarnings = FALSE); .libPaths(c(lib_path, .libPaths())); install.packages(c("tidyverse"), lib=lib_path, repos="http://cran.rstudio.com/")'
#!!!Note: Each RUN command in a Dockerfile is executed in a separate shell, and variables are not persisted between them.
# Therefore, the lib_path variable is not available in a second RUN command. To avoid this issue, you can combine the two RUN commands into a single command as shown below:



#RUN R -e "repo_path <- normalizePath(getwd()); lib_path <- file.path(repo_path, 'R_Library'); dir.create(lib_path, recursive = TRUE, showWarnings = FALSE); .libPaths(c(lib_path, .libPaths()))"

# Install multiple R packages
#RUN R -e "install.packages(c('tidyverse'), lib=lib_path, repos='http://cran.rstudio.com/')"

#RUN R -e "install.packages(c('tidyverse', \
## 'lubridate', \
#'kableExtra'), repos='http://cran.rstudio.com/')"