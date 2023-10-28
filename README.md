# sentimizer
This is the original version of the ChairsFX Sentimizer app. You can use its logic to build your own custom sentimization tool. It uses open-source machine-learning libraries within a desktop application (GUI not included). There's no limit on how many entries you can sentimize, nor any fees for processing large data sets. 

This version's workflow: 
1. The user uploads a CSV file with one set of raw user review data per row.
2. Sentimizer will categorize each review as positive, neutral, or negative.
3. Sentimizer will plot the positive, neutral, and negative scores into a pie chart.
4. Sentimizer will summarize each raw review into a shorter version.
5. Once it processes all entries, the user can click 'export'.
6. Export will produce a spreadsheet filled with each raw review, a summarized version, and a sentiment score (positive, negative, or neutral)
