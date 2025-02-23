
#===================================================================================
# !!! Note: 
#   1. Do NOT change the sequence of code lines or combine code chunks;
#      The sequence is critical, so is the break between two [bash] code chunks
#   2. If this repo comes with a non-empty R_Library, it must be deleted first
#      (Otherwise, it would cause a mysterious error.)
#===================================================================================


# Run commands below (**only once**) to set up the R environment

#================================================================
# Add the R-library directory to the search path (Run in R after R is installed but before any R library is installed)
repo_path <- normalizePath(getwd())
lib_path <- file.path(repo_path, "R_Library")
.libPaths(c(lib_path, .libPaths()))
# Add the R-library directory to LD_LIBRARY_PATH
Sys.setenv(LD_LIBRARY_PATH = paste(file.path(normalizePath(getwd()), "R_Library"), Sys.getenv("LD_LIBRARY_PATH"), sep = ":"))
Sys.getenv("LD_LIBRARY_PATH")
#================================================================

install.packages("tidyr")  
# this also installs ‘utf8’, ‘generics’, ‘pillar’, ‘R6’, ‘stringi’, ‘fansi’, ‘pkgconfig’, ‘withr’, ‘cli’, ‘dplyr’, ‘glue’, ‘lifecycle’, 
#   ‘magrittr’, ‘purrr’, ‘rlang’, ‘stringr’, ‘tibble’, ‘tidyselect’, ‘vctrs’, ‘cpp11’
install.packages("bslib")  
# this also installs ‘digest’, ‘fs’, ‘rappdirs’, ‘base64enc’, ‘cachem’, ‘fastmap’, ‘htmltools’, 
#   ‘jquerylib’, ‘jsonlite’, ‘memoise’, ‘mime’, ‘sass’
install.packages("xml2")
                                    #install.packages("stringi")
                                    #install.packages("rlang")
                                    #install.packages("vctrs")  # this also installs "glue"
                                    #install.packages("withr")  # this also installs "ellipsis", "rlang"                      
install.packages("systemfonts") # this also installs "jsonlite"
install.packages("ps")
install.packages("fontawesome") # this also installs "base64enc", "digest", "fastmap", "htmltools"
install.packages("ids")  # this also installs ‘sys’, ‘askpass’, ‘openssl’, ‘uuid’
install.packages("tinytex")  # also installs "xfun"
install.packages("knitr")  # also installs ‘evaluate’, ‘highr’, ‘yaml’
install.packages("readr") # this also installs "bit64", "clipr", "crayon", "hms", "progress", "vroom",
install.packages("scales") 
# this also installs ‘bit’, ‘prettyunits’, ‘bit64’, ‘progress’, ‘clipr’, ‘crayon’, ‘hms’, ‘vroom’, ‘tzdb’
install.packages("rvest") # also installs ‘curl’, ‘mime’, ‘httr’, ‘selectr’
install.packages("remotes")
install.packages("languageserver")  
# this also installs ‘lazyeval’, ‘pkgbuild’, ‘R.methodsS3’, ‘R.oo’, ‘R.utils’, ‘processx’, ‘backports’, ‘rex’, ‘brew’, ‘commonmark’, 
#   ‘desc’, ‘pkgload’, ‘R.cache’, ‘rprojroot’, ‘callr’, ‘collections’, ‘fs’, ‘lintr’, ‘roxygen2’, ‘styler’, ‘xmlparsedata’



#================================================================
# Run the below once to install the necessary packages

# Load necessary libraries
library(rvest) 
library(magrittr) 

required_packages <- c()
tar_gz_files <- c()
exact_files <- c()
# Save the required packages into a vector of strings
required_packages <- c("rematch2", "svglite", "textshaping", "rmarkdown", "knitr", "evaluate", "rematch", 
              "blob", "DBI", "gtable", "isoband", "rstudioapi", "processx", "timechange", "tzdb"   
              #'sys', 'askpass', 'openssl', "uuid", #"ids", 
              #'curl', 'mime', 'httr', 'selectr', #"xfun", 
              #'utf8', "generics", 'pillar', 'fansi', 'pkgconfig', 'cli', "purrr", "tibble", "tidyselect", 
              #"colorspace", "farver", "labeling", "munsell", "RColorBrewer", "viridisLite", 
              #"bit", "prettyunits", 
              #"lintr", "roxygen2", "styler", 
              #"digest", "fs", "rappdirs", "base64enc", "cachem", "fastmap", "htmltools", "jquerylib", "memoise", "sass", 
                       
                       )
# Collect the list of .tar.gz files from the webpage
url <- "https://cran.r-project.org/src/contrib/"
page <- rvest::read_html(url)
tar_gz_files <- page %>% rvest::html_nodes("a") %>% rvest::html_attr("href") %>% 
                grep("\\.tar\\.gz$", ., value = TRUE)

# Extract the exact full names of the .tar.gz files to be downloaded
exact_files <- tar_gz_files[grepl(paste0("^(", paste(required_packages, collapse = "|"), ")_.*\\.tar\\.gz$"), basename(tar_gz_files))]

# Start a loop over the list of exact full names of .tar.gz files to download all the files
for (file in exact_files) {
  #print(paste0(url, file))
  download.file(paste0(url, file), destfile = file)
}

# Use a vector-based syntax to install all the downloaded packages
install.packages(exact_files, repos = NULL, type = "source", dependencies = TRUE)
# Use remotes::install_local to install all the downloaded packages
#for (file in exact_files) {
#  remotes::install_local(file, dependencies = TRUE)
#}



#================================================================
# Run the below once to install more packages

# Load necessary libraries
library(rvest) 
library(magrittr) 

required_packages <- c()
tar_gz_files <- c()
exact_files <- c()
# Save the required packages into a vector of strings       
required_packages <- c("ggplot2",  #"bslib", #"dplyr", 
                       "broom", "cellranger", "conflicted", "data.table", "dbplyr", "dtplyr", "forcats", 
                       "gargle", "googledrive", "googlesheets4", "haven", "modelr", "ragg", "readxl", "reprex"
                       #"lubridate", "tidyverse", "kableExtra"
                       )

# Collect the list of .tar.gz files from the webpage
url <- "https://cran.r-project.org/src/contrib/"
page <- rvest::read_html(url)
tar_gz_files <- page %>% rvest::html_nodes("a") %>% rvest::html_attr("href") %>% 
                grep("\\.tar\\.gz$", ., value = TRUE)

# Extract the exact full names of the .tar.gz files to be downloaded
exact_files <- tar_gz_files[grepl(paste0("^(", paste(required_packages, collapse = "|"), ")_.*\\.tar\\.gz$"), basename(tar_gz_files))]

# Start a loop over the list of exact full names of .tar.gz files to download all the files
for (file in exact_files) {
  #print(paste0(url, file))
  download.file(paste0(url, file), destfile = file)
}

# Use a vector-based syntax to install all the downloaded packages
install.packages(exact_files, repos = NULL, type = "source", dependencies = TRUE)
# Use remotes::install_local to install all the downloaded packages
#for (file in exact_files) {
#  remotes::install_local(file, dependencies = TRUE)
#}


#===================================================================================
# Run the below once to install the final target packages 


# Load necessary libraries
library(rvest) 
library(magrittr) 

required_packages <- c()
tar_gz_files <- c()
exact_files <- c()
# Save the required packages into a vector of strings
required_packages <- c(                                               
                       "lubridate", "tidyverse", "kableExtra"
                       )


# Collect the list of .tar.gz files from the webpage
url <- "https://cran.r-project.org/src/contrib/"
page <- rvest::read_html(url)
tar_gz_files <- page %>% rvest::html_nodes("a") %>% rvest::html_attr("href") %>% 
                grep("\\.tar\\.gz$", ., value = TRUE)

# Extract the exact full names of the .tar.gz files to be downloaded
exact_files <- tar_gz_files[grepl(paste0("^(", paste(required_packages, collapse = "|"), ")_.*\\.tar\\.gz$"), basename(tar_gz_files))]

# Start a loop over the list of exact full names of .tar.gz files to download all the files
for (file in exact_files) {
  #print(paste0(url, file))
  download.file(paste0(url, file), destfile = file)
}

# Use a vector-based syntax to install all the downloaded packages
install.packages(exact_files, repos = NULL, type = "source", dependencies = TRUE)
# Use remotes::install_local to install all the downloaded packages
#for (file in exact_files) {
#  remotes::install_local(file, dependencies = TRUE)
#}


#===================================================================================
# Clean up downloaded files

system("rm *.tar.gz*", wait = TRUE)
Sys.getenv("LD_LIBRARY_PATH")


