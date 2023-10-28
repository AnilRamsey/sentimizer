# sentimizer
This is the original version of the ChairsFX Sentimizer app. You can use its logic to build your own custom sentimization tool. It uses open-source machine-learning libraries within a desktop application (GUI not included). There's no limit on how many entries you can sentimize, nor any fees for processing large data sets. 
![sentimize-app-github](https://github.com/AnilRamsey/sentimizer/assets/149247651/bf363580-b76a-4de1-8ed6-47615630a1ff)
This version's workflow: 
1. The user uploads a CSV file with one set of raw user review data per row.
2. Sentimizer will categorize each review as positive, neutral, or negative.
3. Sentimizer will plot the positive, neutral, and negative scores into a pie chart.
4. Sentimizer will summarize each raw review into a shorter version.
5. Once it processes all entries, the user can click 'export'.
6. Export will produce a spreadsheet filled with each raw review, a summarized version, and a sentiment score (positive, negative, or neutral)

![sentimizer-output](https://github.com/AnilRamsey/sentimizer/assets/149247651/71b422d8-2eea-4696-af84-87a5b72f55f1)

The finished output that the user can export adds two new columns to the original data set: 
1. A summarized version of the raw data 
2. A sentiment score (positive, negative, or neutral).

## Accuracy

We ran tests using 200 rows of genuine user reviews. Then, we had a human reviewer manually check each positive, negative, or neutral sentiment score for accuracy. Accuracy is around 90%; the program sometimes confuses neutral and negative sentiments. 

This means a human editor should always check the final results for accuracy. 

## Developing Version 1.0

At present, it takes a human reviewer around 3 hours to manually verify 200 rows of Sentimizer output. Version 1.0 aims to cut that down by adding more quick-glance data:

1. Categorizing raw review sentences as likes or dislikes.
2. Extracting the keywords from all columns of likes and dislike sentences
3. Plotting the likes and dislikes as bar charts.
4. Exportable charts and CSV data
