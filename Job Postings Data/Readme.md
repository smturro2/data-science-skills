# Files

- keyword_frequencies.csv - Main datafile of the project. The frequency of each keyword with category lables.
- Job Posting Results.pdf - Visualizations of the data
- loaded_data.csv
- keyword_by_job_posting.csv - The number of references of each keyword indexed by the job postings.
- every_word_by_job_posting.csv - Similar to keyword_by_job_posting.csv but for every word in the description.
- raw_data.txt - 8 Additional details on the 1100 job postings. Indexes match with the 2 data files above.
- The symbol "}" was used as a separator and the following code can be run to import the data using pandas in python:

        import pandas as pd
        df_jobs = pd.read_csv("raw.txt", sep="}")
