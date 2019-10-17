
# Enron Email Identification
**Using Graph Algorithms to segemnt participants in an information network and Identify meaningful patterns in email communication**
<br>Nathan Laird
<br>
[Linkedin](http://www.linkedin.com/in/nathn-laird) | [Github](https://github.com/nathanlaird)

## Table of Contents

* [Motivation](#motivation)
  * [Personal](#personal)
  * [Business](#business)
* [Data Understanding](#data-understanding)
  * [Data Sources](#data-sources)
  * [Data Processing](#data-processing)
  * [Evaluation](#evaluation)
* [Future Improvements](#future-improvements)
* [Built With](#built-with)
* [Acknowledgements](#acknowledgements)
* [Contact Me](#contact-me)


## Motivation

### Personal


While working at Netskope I became fascinated helping others manage risk and uncertainty, I got to a variety of people all working on the goal of securing those things that are most precious to them. I was enamoured by the idea that looking at network data could create models to better inform people about the risks they face.

### Business

96% percent of all cyber attacks begin via email. identifying anomalous emails is difficult for many reasons, one of which is that Anomalous Behavior for one user could be completely normal for another. By grouping users by thier position in the communication network I want to create a model to predict group membership by email content. If a user sending or recieving a large number of emails that dissimiliar in terms of content from thier peers, this could be a sign of anomalous behavior that deserves more investagation.

## Data Understanding

### Data Sources

* [Comprehensive, Multi-Source Cyber-Security Events](https://csr.lanl.gov/data/cyber1/) 

* Auth.txt - Contains All Authentification Events for the Network, used to identify human owned computers
<img src="Viz/Human_Filtered_Auth.png" align="center" width = "500" />
* Flow.txt - contains all data flows in the network with source IP Destination IP and ByteCount
<img src="Viz/Flow_initial.png" align="center" width = "500" />
Redteam.txt - contains a list of all compromised machines



### Data Processing

To deal with the 100GB of Log data Computation for Data Processing is outsourced to an EMR cluster composed on EC2s running spark queries.

In order to filter down to only human owned computers we look for the IPs of computer making 

Interactive Logins using known employee accounts.

To create the DataFrame of compromised users we additional filter down to where dstIP and srcIP are in the list of compromised users.

Once Human users have been identified, we filter Flow.txt to include on those records whose srcIP or dstIP is a human user.

depending on whether a flow begins or terminates on a known users we assign it as either Upload or Download.

Using Upload/Download and the size of the flow transfer, we fill in Upload_Bytes and Download_Bytes accordingly.

Using Upload/Download and the dstIP and srcIP, we fill in user and service accordingly.

Filled_DataFrame_Flow.png
<img src="Viz/Filled_DataFrame_Flow.png" align="center" width = "500" />

we then summarize these flow events by time interval and user to create a time series of data transfers up and down as well as a distribution of data movements for all users.

<img src="Viz/TrafficDataPlusUsers.png" align="center" width = "500" />

### Evaluation

To determine if there was a difference in means in the upload of individuals from the Total Population versus the Compromised Populations, We run a Mann-Whitney U Test. Our Alpha for this process should be fairly low to account for the sensitive nature of misidentifying a compromised user, .01.

our calculated p-value comes to 1.2472e-20, giving us ample evidence to reject the null hypothesis that, there is a 50% chance any random item from Compromised exceeds any random item from total
<img src="Viz/Dist_Hists.png" align="center" width = "500" />

## Future Improvements
* perform analysis on distribution of services visited
* use KDEs to identify protentially compromised machines
<img src="Viz/KDE.png" align="center" width = "500" />

## Built With

* [Python](https://www.python.org/)
* [AWS EC2](https://aws.amazon.com/ec2/)
* [Pandas](https://pandas.pydata.org/)
* [Numpy](http://www.numpy.org/)
* [Matplotlib](https://www.matplotlib.org/)


## Acknowledgements

* [Galvanize](https://www.galvanize.com/) and the Data Science Immersive Team, for their guidance and support.



## Contact Me

Nathan Laird is a Data Science Fellow at Galvanize, I have experience modeling and working with large messy Datasets. My interests include, Cloud Security, Insurance, Education,Non-profits. You can contact him at:

* Linkedin: [in/nathan-laird](http://www.linkedin.com/in/nathan-laird)
* 
* Github: [@nathanlaird](https://github.com/nathanlaird)


