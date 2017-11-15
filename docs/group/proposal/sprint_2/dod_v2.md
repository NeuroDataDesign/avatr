# Definitions of Done for Sprint 2 Deliverables  

## Improve Annotation workflow by decreasing the number of terminal commands required.  
**Definition of Done**:  
Have the annotation workflow require two terminal commands at most to run from end to end. The first terminal command should be to pull data from the BOSS. The second terminal command should be to push data to the BOSS.  

## Create a MVP LIMS that has the following features:  

### Dataset Registration  
**Definition of Done**:  
Users will be able to manually fill out a webform with the following fields for each dataset: 
- owner, 
- link to data, 
- description of dataset, 
- references and links.  
Once this form is submitted, the LIMS will correctly store the dataset in a global database. Users will also be able to see their registered dataset through the Dataset Query function.  

### Dataset Query  
**Definition of Done**:  
The LIMS will have a route to display all datasets in a readable format onto a webpage. Users can then search for their registered dataset manually.  

### Documentation  
**Definition of Done**:  
Thorough documentation outlining how each feature in the LIMS works will be up in Sphinx.   

**Definition of Done for MVP LIMS**: Have a locally deployed LIMS that runs on the web and can demo each feature.

## Explore pipeline logging tools and implement basic pipeline logging for Eric's data    
**Definition of Done**:  
Have at least two tech evaluations on current pipeline logging tools (StackDriver, DataJoin?). Demo running pipeline on Eric's data and results being logged correctly.


*This is a great start.  But we need to specify which datasets will be incorporated into the LIMS system.  I would say we should start with data that already exist.  In particular, every [graph](http://openconnecto.me/graphs/) and [image](https://neurodata.io/data/).  If all those data are in at the end of Sprint 2, this is success of having build a LIMS. *

*Note that an even better success is for the neurodata.io webpage to use your LIMS system to query and get links to all the information it needs.  Doing so requires, however, integration with neurodata.io, so I would not scope it necessarily for this semester.*

*You will need a "specification" for both `image` & `graph` datasets.  If you speak with `lemurs`, you will also want to think about a specification for `tabular` datasets, to include various metadata and data derivatives. I would not scope it to include tabular data this semester.* 
