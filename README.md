# Predicting Injury Disposition

The United States Consumer Product Safety Commission collects data on emergency visits to U.S. hospitals that involves an injury associated with consumer products. The resulting dataset is called the [National Electronic Injury Surveillance System (NEISS)](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/). You can access the full data from 2009 to 2014 [here](https://github.com/hadley/neiss). 

Using the above data, please build a machine learning model that predict the disposition (i.e. outcome) of an ER visit given the other information that was collected by NEISS. Since we would like to use this model as part of our production environment, please package it so other services can consume it remotely.

## Deliverable: 

- A machine learning model that predict an injury's disposition
- An interface so third-party clients can submit new injury cases and receive the predictions
- A report that details your process of experimenting and building the above

## Considerations for Submission

- Which machine learning problem are you tackling? Is it unsupervised or supervised?
- Which features do you think would have the most predictive value, and why? Is this hypothesis supported by your model?
- We are very interested in your thought process, assumptions, and design decisions with regards to both the ML model and its production interface. Please document those in a report format that you see fit.
- Documentation on your model and its public interface would be very helpful: how we can validate, deploy, and interact with your model, what is the request and response format, etc.

## Submission Rules

- The time limit for this challenge is 72 hours. You can use whichever programming languages or stack you feel most comfortable with.
- Please submit a [PR](https://help.github.com/articles/about-pull-requests/) to this repository, with the code that you have produced and the report on your process.
- Your solution should be functional, and we should be able to reproduce the results in your report.

## Honor code

As software engineers, an invaluable part of our skill set is knowing how to effectively Google our problems and bugs. As such, it is OK for you to use resources on the Internet for this challenge. We only ask you to refrain from doing two things:

1. Copying and pasting code samples from the Internet and presenting them as your own work. This would be considered plagiarism and disqualify you immediately.
2. Googling anything specific to this dataset. Please treat the dataset as if it is novel and unique to you.

## Contact/Progress

*VERY IMPORTANT*: Don't hesitate to contact us along the way and update us on your progress, so we can provide feedback on your direction.
