# Context:
- Scientific Goal: Understand how emotional valence affects risk-taking
- Data Set: 35 subjects participating in a 90 trial mood manipulation task
- Statistical Goal: Create a statistical test to detect if mood belongs in the Markov blanket of risk-taking behavior
- Computational Goal: Explore the data sets, build task-specific features, build features that encode competing scientific hypotheses about emotional valence and risk-taking, examine the stability of features over varying regularization and data resampling, build logisitc regressions and neural networks and interpret their coefficients
- [Full Thesis](https://drive.google.com/file/d/1suI2_G2Yr0xgezhOJGKc8gicD7TjD2y3/view?usp=share_link): Play it Safe or Take a Risk? Computational Modeling & Statistical Inference for the Effect of Emotional Valence on Risk-Taking
- IPython Notebook of All User-Friendly Updated Code: [all_code_best_version.ipynb](https://nbviewer.org/github/jesshuang98/nimh-mlt-risk-taking/blob/main/all_code_best_version.ipynb)

# Subjects:

## [Explore Subject Characteristics](https://nbviewer.org/github/jesshuang98/nimh-mlt-risk-taking/blob/main/all_code_best_version.ipynb#Load)
- Start: Raw Data from Mood Manipulation Interface Task
- End: csv file called 'gps_[experiment].csv' which lists subjects and their characteristics. The subject ids in this file will be used for future analyses that look at cross-subject validation for example

# Feature Selection:

## [Create Main Features](https://nbviewer.org/github/jesshuang98/nimh-mlt-risk-taking/blob/main/all_code_best_version.ipynb#Create-Normalized-Main-Features-and-Evaluate-Collinearity)
- Start: Raw Data from Mood Manipulation Interface Task
  - Maps all features to the same general space of centered at 0 and with standard deviation 1 
  - 'normed' option: Converts raw point values of the task to normalized point values, such that 0 remains in the same place but the raw point values have standard deviation 1 
  - features calculated: 
    - The subject characteristics will be age, gender, and diagnosis. 
    - The trial parameters pertaining to the current trial will an indicator (with 1 if for this trial, choosing to gamble will always yield more money than choosing not to gamble), current expected reward (average of not gamble reward option and two gamble reward options), and gambling range (difference between higher gamble reward option and lower gamble reward option). 
    - The trial parameters pertaining to the outcomes of past trials are an exponential sum of past reward prediction errors and an exponential sum of past outcomes. To elaborate, reward prediction error is actual reward outcome - expected reward outcome while the exponential sums are weighed so more recent trials have large weights closer to 1 and more previous trials have smaller weights closer to 0.
- End: x and y csv files where x contains main features to predict gambling probability (0 - 1) and y contains the target gambles themselves (1's or 0's)

## [Calculate Quadratic Interactions](https://nbviewer.org/github/jesshuang98/nimh-mlt-risk-taking/blob/main/all_code_best_version.ipynb#Calculate-Quadratic-Features)
- Start: x csv file where x contains main features to predict gambling probability (0 - 1) and y contains the target gambles themselves (1's or 0's)
- End: x csv file with interactions, npy file with all column names

## [Standardize All Features](https://nbviewer.org/github/jesshuang98/nimh-mlt-risk-taking/blob/main/all_code_best_version.ipynb#General-Function-to-Standardize-Features)
- Start: any x csv file
- End: x csv file with interactions, npy file with all column names, all features are standardized. This is useful for stability selection which has stability results/ rankings that are very sensitive to standard deviation of features.

## [Stability Plots and Regularization Plots](https://nbviewer.org/github/jesshuang98/nimh-mlt-risk-taking/blob/main/all_code_best_version.ipynb#Stability-Plots-and-Regularization-Plots)
- Start: x csv file with interactions, npy file with all column names, all features are standardized.
- End: stability and regularization plots

## [Average Stability Calculations](https://nbviewer.org/github/jesshuang98/nimh-mlt-risk-taking/blob/main/all_code_best_version.ipynb#Average-Stability-Calculations)
- Start: npy files for the stability values at different levels of L1 regularization
- End: csv file with the names and average stabilities of all features (averaged across lambda values), npy file with ranking of indices of the top most stable (on average) features

## [Picking Number of Most Stable Features](https://nbviewer.org/github/jesshuang98/nimh-mlt-risk-taking/blob/main/all_code_best_version.ipynb#Picking-Number-of-Most-Stable-Features)
- Start: ranking of indices of most stable features
- End: graph of LOOCV accuracy of models trained on 0 features, 1 top most stable feature, top 2 most stable features, top 3 most stable features, ..., all the way to 45 features (9 main features + 36 interactions). You can pick a sufficient number of features by seeing which # of features achieves the global maximum LOOCV accuracy
- example: you can go back and visualize stability and regularization plots for only these features by using running the following commands in lr_stab2_features.py to use NFEATS:
  - ind_a = np.load("areas_areas_indices_" + ET + ".npy")
  - ind_m = np.load("areas_maxes_indices_" + ET + ".npy")
  - print ind_a
  - print ind_m
  - l = ind_a[:NFEATS]
  - print len(l)
  - stabgraphsavefeat(x, y, l)
  - reggraphsavefeat(x, y, l)



# Modeling:

## Logistic Regression:

### [Estimate LOOCV accuracy](https://nbviewer.org/github/jesshuang98/nimh-mlt-risk-taking/blob/main/all_code_best_version.ipynb#Estimate-LR-LOOCV-accuracy)
- End: csv file of results

### [Estimate Weights of a Model Trained on Entire Data Set](https://nbviewer.org/github/jesshuang98/nimh-mlt-risk-taking/blob/main/all_code_best_version.ipynb#Estimate-Weights-of-a-Model-Trained-on-Entire-Data-Set)
- End: npy files with weights of logistic regression

### [Visualize Weights of a Model Trained on Entire Data Set](https://nbviewer.org/github/jesshuang98/nimh-mlt-risk-taking/blob/main/all_code_best_version.ipynb#Visualize-Weights-of-a-Model-Trained-on-Entire-Data-Set)
- End: csv file of model weights

### [Compare Weights of a Model Trained on Entire Data Set](https://nbviewer.org/github/jesshuang98/nimh-mlt-risk-taking/blob/main/all_code_best_version.ipynb#Compare-Weights-of-a-Model-Trained-on-Entire-Data-Set)
- End: heatmap with weights of logistic regression


## Neural Network:

### [Estimate LOOCV accuracy](https://nbviewer.org/github/jesshuang98/nimh-mlt-risk-taking/blob/main/all_code_best_version.ipynb#Estimate-NN-LOOCV-accuracy)
- End: csv file of results

[comment]: <> ([Estimate Weights of a Model Trained on Entire Data Set and Bootstrap Resamplings]
Run nn_boot_hessians_gradients.py
[DOESNT WORK YET] setting the seed = 0 gets us the original dataset
setting the seed to > 0 gets us some bootstrap resampling of the original dataset
End: npy files with hessian variables)

### Visualize average weights of quadratic terms of models, Averaged Across 100 Bootstraps, using [Hessian matrices](https://nbviewer.org/github/jesshuang98/nimh-mlt-risk-taking/blob/main/all_code_best_version.ipynb#Generate-Hessian-Values)

- End: heatmaps of prevalence, positive ratios, negative ratios and average hessian values

[comment]: <> ([Visualize average weights of linear main effect terms of models, Averaged Across 100 Bootstraps, using gradients]
[DOESNT WORK YET] Run visualize_gradient.py
End: heatmaps of prevalence, positive ratios, negative ratios and average gradient values)
