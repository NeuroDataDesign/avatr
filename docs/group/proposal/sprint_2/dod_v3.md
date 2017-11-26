# Revised Definitions of Done for Sprint 2 Deliverables  

## Improve Annotation workflow by decreasing the number of terminal commands required.  
**Definition of Done**:  
Have the annotation workflow require two terminal commands at most to run from end to end. The first terminal command should be to pull data from the BOSS. The second terminal command should be to push data to the BOSS.  

## Create a MVP LIMS for the m2g.io datasets :  

### Dataset Registration  
**Definition of Done**:  
We will create csv and web parsers to scrape m2g.io dataset information into a database. The data should be organized in a manner such that CSV metadata information and appropriate links to graph are inserted in relation with each subject.
  - **Scrapers**:
    - CSV scraper to extract subject metadata from dataset covariates.  
    - Web parser for m2g.io to extract links for aligned images, tensors, fibers, graphs, QA plots, and version of code.
  - **Database Schema**:
    - Formatted database schema for structuring scraped data into database.
    - Schema should be designed based off of feedback from Eric and Jovo.
  - **Database Manager**:
    - Scripts to load data correctly into database based off of specified schema.
    - Reach: Scripts to handle database migrations (schema change), missing data, and delete entries.

### Dataset Query  
**Definition of Done**:  
The LIMS will have a route to display m2g.io datasets in an organized tree structure. Users will be able to explore individual subject information by clicking on a specific dataset and a specific subject.  

Once a specific subject is selected, metadata information and relevant links related to the subject should be displayed in an organized interface.  


### Documentation  
**Definition of Done**:  
Thorough documentation outlining how each feature in the LIMS works will be up in Sphinx.   

**Definition of Done for MVP LIMS**: Have a locally deployed LIMS that runs on the web and can demo dataset query. LIMS should also demo proof that m2g.io subjects are properly stored in database through the query function.

## Explore pipeline logging tools and implement basic pipeline logging for Eric's data    
**Definition of Done**:  
Have at least two tech evaluations on current pipeline logging tools (StackDriver, DataJoin?). Demo running pipeline on Eric's data and results being logged correctly.
