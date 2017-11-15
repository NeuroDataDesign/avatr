# Definitions of Done for Sprint 2 Deliverables  

## Improve Annotation workflow by decreasing the number of terminal commands required.  
**Definition of Done**:  
Have the annotation workflow require two terminal commands at most to run from end to end. The first terminal command should be to pull data from the BOSS. The second terminal command should be to push data to the BOSS.  

## Create a MVP LIMS that has the following features:  

### Dataset Registration  
**Definition of Done**:  
Users will be able to manually fill out a webform with the following fields for each dataset: owner, link to data, description of dataset, references and links.  
Once this form is submitted, the LIMS will correctly store the dataset in a global database. Users will also be able to see their registered dataset through the Dataset Query function.  

### Dataset Query  
**Definition of Done**:  
The LIMS will have a route to display all datasets in a readable format onto a webpage. Users can then search for their registered dataset manually.  

### Documentation  
**Definition of Done**:  
Thorough documentation outlining how each feature in the LIMS works will be up in Sphinx.   

**Definition of Done for MVP LIMS**: Have a locally deployed LIMS that runs on the web and can demo each feature.

## Explore pipeline logging tools and implement basic pipeline logging for a NeuroData team  
**Definition of Done**:  
Have at least two tech evaluations on current pipeline logging tools (StackDriver, DataJoin?). Have NeuroData team demo running their pipeline and the results of that run being logged correctly.
