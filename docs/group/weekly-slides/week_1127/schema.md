# Schema Proposal  
The current datasets are already formatted in the current format:  
- Dataset  
  - metadata
    - subject
  - aligned images
    - subject
  - tensors
    - subject
  - fibers
    - subject
  - graphs
    - subject
  - quality assurance

Since many of the subtrees rely on subjects and our focus on the LIMS currently is on subjects, it makes sense for the first schema iteration to focus mostly on the subjects. This means that we should rearrange the dataset such that subjects take prevalence over the calculated plots and derivatives.  

Below is our proposed solution:  
- Dataset  
  - quality assurance
  - subject
    - aligned images
    - tensors
    - fibers
    - graphs
    - metadata

With this schema, it should be fairly simple to perform search filters and queries of individual subject information while still keep track of the overall dataset quality.  

Note that this tree structure fits the specs of a MongoDB extremely well.
