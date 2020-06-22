# Final Project
<h6>Course CMSC-6950</h6>
<h6>Title Computer base tools and applications</h6>


<h6>File doubling.sh (Shell Script)</h6>  

Shell Script to compute doubling rate

<h6>Required Arguments</h6> 

    province > i.e Canada | Alberta | Ontario 
    string   > 'number of cases' | 'number of deaths' 
    date     > format dd-mm-yyyy (01-04-2020)
    
<h6>Execution</h6>
    
     bash doubling.sh  Canada 'number of cases' 01-04-2020 

<h6>Output</h6>
    
     output.txt file province fromDate NoOfCases DoublingDate NoOfDays
     example Canada 01-04-2020 9613 08-04-2020 19289 7
     
 
<h6>File main.py (Python3)</h6>  

<h6>Execution</h6>
  
      1. Donload COVID19 Data from https://health-infobase.canada.ca/src/data/covidLive/covid19.csv 
      1. Read CSV covid19.csv
      2. Create plot Number Of Total Cases for each province over time. 
      output: 
  ![alt text](https://i.ibb.co/KKBX89P/Snip20200621-1-1.png) 
         
      3. Create a second plot showing the number of individuals tested in each province over time.
        
  ![alt text](https://i.ibb.co/8cNkfqf/Snip20200621-2.png)      
   
      4. Create a third plot demonstrating the number of new cases per day.
        
  ![alt text](https://i.ibb.co/XZr8xS6/Snip20200621-3.png)       
  
      5|6. calculates the doubling rate Plot
        
  ![alt text](https://i.ibb.co/SQpLfQ5/Snip20200621-4.png) 