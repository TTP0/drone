# What is TTP0 DRONE
It is an operational acronym based on the TTP0 approach to key focus areas of the Security Operations (SecOps) world.  
This operational acronym is specific to cyber security **Incident Management**.

The intent of DRONE is to immediately help you:


Term   |  Purpose
---------------|----------------------------
**D***efine* |Your opertional criteria, its context, priorities, impact, and data of interest (OSINT, IoC, Observables)
**R***educe* | The frustration of not knowing where to start regardless of your team's size, and minimize data entry errors
**O***utline* |Outline fundamental key measurements to account for **good security work** to scale services & team size
**N***otify*  |Provide effective communication of incidents between practitioners, business leaders with the necessary context
**E***nable*  | Your focus on leading people and growing their skills while minimizing the burden of creating the basics


# TTP0 - DRONE by @DFIRENCE

> "The TTP0 DRONE is resource to deliver the usage of a custom workflow used for cyber security operations, and 
specifically
> the use by security teams to manage incidents with a platform neutral approach where security practitioners can be 
enabled to achieve rather than stalling them with limitations due to a product's constraint.
" -@dfirence
***

As of today, DRONE leverages the powerful open source project called "**TheHive**" as an example of using the DRONE 
workflow.

The intent of **DRONE is to remain agnostic to a product or platform**, it is focused on the technique(s) and procedure(s) 
that are important when managing an operational group and its services from the ground up.  By technique and procedure we refer to the **information design** applied to the subject of incident management.  

The design is carefully considerate of providing a solid state of awareness of how an 
incident may affect an organization, its people and systems used for either general or critical business efforts.

The TTP0 DRONE is a **WIP** (Work In Progress) being matured into different main stream platforms that can be used for
managing demand and work efforts (e.g., Ajira, ServiceNow, Remedy, etc.)

***
# RECORDING INCIDENTS WITH TTP0 DRONE & TheHive

### Use TheHive Incident Management Platform with TTP0 DRONE

[![TTP DRONE](https://i.imgur.com/agn5kch.png)](https://i.imgur.com/agn5kch.png "TTP0 DRONE & TheHive")

***
### Use the Command Line and the Observables MiniShell

BY TYPE | WITH CONTEXT | PLUS RICH DATA
--------|--------------|-----------------------------
[![TTP0 DRONE FRAMEWORK](https://i.imgur.com/vETHUSc.png)]([Imgur](https://i.imgur.com/vETHUSc.png "Incident Categorization")|[![TTP0 DRONE CONTEXT](https://i.imgur.com/oDSnrDN.png)](https://i.imgur.com/oDSnrDN.png "Context")|[![TTP0 DRONE OBSERVABLES](https://i.imgur.com/hTbFeuT.png)](https://i.imgur.com/hTbFeuT.png "Observables")

***

# BEFORE YOU START

* Ensure you have python 2.7 installed and that the PIP package manager is working correctly

* You have installed a working instance of the CERT-BDF TheHive incident management platform - [TheHive 
Project](https://github.com/TheHive-Project/TheHive)

* We **highly suggest** you to watch this overview of the TTP0 DRONE before you start - [TTP0 DRONE 
Video](https://youtu.be/zoItQ1KFb2o) 


# GETTING STARTED

Assuming the above is complete, you can get started below.

## Clone This Repo
```
      git clone https://github.com/TTP0/drone.git
```
## Navigate TO App Directory
```
    cd drone
```
## Install Dependencies
```
      pip install -r ttp0-drone-requirements.txt
```
## Configure Your SOC, ZONES, BUSINESS UNITS
```
      python ttp0_drone.py configure
```
## Run DRONE ( ensure you ran configure as shown in YOUTUBE VIDEO )
```
     python ttp0_drone.py run
```

# DRONE FRAMEWORK WIKI
The custom framework that is driven from the U.S. CERT Incident Categorization is represented in the [**TTP0 DRONE WIKI**](https://github.com/TTP0/drone/wiki/OVERVIEW)

# FUTURE ROADMAP - FEATURES & DOCUMENTATION
Priority | Feature
---------|-----------
P1 | Email Support for Linux, Windows
P1 | Framework Documentation Wiki
P1 | Ansible Playbook for TTP0 - TheHive Deployment (Debian, Arch, CENTOS)
P2 | Custom SOC Incident Reporting Template
P2 | Local Case Manager released from private codebase
P3 | Integrations with Commodity APIs
P4 | Web Application Platform
