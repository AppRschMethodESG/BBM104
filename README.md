# BBM104 Applied Research Methods in ESG - Demo codes

### Installation

- To set up R and install the required packages (e.g., tidyverse for R 4.4.2) in a Github Codespaces / Lightning.ai Studio created from this repo,
   - execute the commands below in a terminal (bash shell) of the Codespaces / Studio (after replacing the filename **`SetupRunOnce.sh`** accordingly):

`chmod +x SetupRunOnce.sh`  
`./SetupRunOnce.sh`

---

**!!! Note**: 

- For Github _**Codespaces**_:
   - Replace `SetupRunOnce.sh` with `SetupRunOnce_Codespaces.sh`

- For Lightning.ai _**Studio**_ (click [here](https://lightning.ai/pricing) to sign up for a free-tier account using your school email address):
   - Must do the following first:
      - Click `File` on the dropdown menu; select `Open Folder...`
      - In the popup window, click `this_studio` then `BBM104` to  
          get the path `/teamspace/studios/this_studio/BBM104/` and select it by clicking the `OK` button
      - The window will reload and rebase with the path above as the current working directory   
      - Click `Terminal` on the dropdown menu; select `New Terminal`
      - In the terminal, execute the two commands by replacing `SetupRunOnce.sh` with `SetupRunOnce_Lightning.ai.sh`

- Can use the following command to _**log the output and error to files**_ while also displaying them in the terminal (after replacing the filename `SetupRunOnce.sh` accordingly):
   - `./SetupRunOnce.sh > >(tee script_output.log) 2> >(tee script_error.log >&2)`

