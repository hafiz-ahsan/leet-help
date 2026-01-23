# Initial Planning

❯ Create a plan for the following problem:                                                                                                                           
    - There is a csv file in the root of the project grind75_problems.csv                                                                                              
    - The csv file has a set of leetcode problems.                                                                                                                     
    - My ultimate goal is to create a study workbook.                                                                                                                  
    - You will write three programs for me that takes in this CSV file and produces the study workbook.                                                                

---                                                                                                                                                                
    Program 1 - Downloader                                                                                                                                             
                                                                                                                                                                       
    For each problem, you will first need to get the problem from LeetCode website. It has anti-scraping technology. So you should use Safari to download and save     
    the page in a suitable format. Name the file problem.<your chosen extension>                                                                                       
                                                                                                                                                                       
    You will them go through the problem and extract the problem description for each problem. You will save each problem in a subdirectory under problems/            
    directory. Name the directory from the URL fragment of the problem. Make sure the name starts with the leetcode problem number e.g. 20-                            
    
---                                                                                                                                                                
    Program 2 - Solver                                                                                                                                                 
                                                                                                                                                                       
    Input to this program is a csv file or one or more leetcode problem numbers. For each problem, you will first run an LLM query query to get both a pseudocode      
    and a solution. Ask the LLM to make the solution direct and heavily commented. You will use Simon Willison's llm command line tool for this. You will read a       
    config file to drive the LLM spec and LLM prompt. You will save the LLM respnse as a markdown file in the same directory where the problem is. The config file     
    may mention one or more directories where there may be code or solutions for you to use. You can first search under these directories (another LLM tool call,      
    input: directory names from all directories, output: possible directories matching the problem. If you find directories that match, read the code and add them     
    to the context before sending to LLM. Please remember that I can do this multiple times against multiple LLMs. So, you should save each response.                  
---                                                                                                                                                                

    Program 3 - Documenter.                                                                                                                                            
                                                                                                                                                                       
    Input: A CSV file or one or more problem numbers. Output: a pdf file containing rendered outputs of all problems and solutions suggested by LLM.                   
---                                                                                                                                                                
    In addition I would like you to use uv as the build/packaging tool for this project. You will have to create a README.md to show me how to use uv for building     
    and running these programs. Also, how to release this as a python package to pypi.                                                                                 
                                                                                                                                                                       
---                                                                                                                                                                
                                                                                                                                                                       
    Please create this plan and save under plans/ dir.   



# Plan Update

Instead of the documenter step in @plans/implementation-plan.md we will do something different. Update the plan this way                                                                                                               
  - Program 3 will be an Indexer: It will take in the csv file and create a markdown file in the root directory with the same name as the csv file. I changed the input file name to grind75.csv. So the output file will be             
  grind75.md. This file will have a table. Each row in the table will correspond to the input rows. The leetcode.com link will have the text "LC". There will be a Problem column that will link to the problem.md for the row. Make     
  sure the subdirectory name is correct. Then there will be columns for each llm output. The text will simply say "Solution". The links will go to the llm output.                                                                       
                                                                                                                                                                                                                                         
  - Program 4 will be the PDF file generator that creates a pdf in each subdir (skips if the pdf is newer than any llm solution). The pdf should be a most two pages. Use smaller fonts. Keep the problem statement short. Use two       
  columns in the problem statement. For solutions, use two columns and in left  Claude Opus and on right render. Make the page condense. Keep code properly formatted. Use 10 point fonts.                                               
  - Program 5 will be an anki flash card generator. For each problem you will generate a full anki flash card with both solutions. Input is thre same - csv file. Output will be a flash card module that anki can load. 