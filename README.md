# AS graph for cyberborder paper

This repository contains two scripts, one for computing a graph showing the
connection between important ASes for a country. And one for plotting this
graph.


## Installation
Clone this repository:
```
git clone git@github.com:romain-fontugne/cyberborder-hegemony-plots.git
```

Install dependencies:
```
pip install -r requirements.txt
```

## Create the AS graph
This step is optional since this repository already provide data for March
2025.

The following command fetch data from the Internet Yellow Pages and write the
computed graph in a file. Change the country code and filename accordingly.
```
python fetch_data.py  GB > 2025-03-08_GB.json
```


## Plot the AS graph
Plot the computed graph with the following command:
```
python plot.py 2025-03-08_GB.json 
```

This creates two files (AS_graph_GB.png and AS_graph_GB.pdf).
