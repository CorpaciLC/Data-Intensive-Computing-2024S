# DIC2024S - exercise 2

## Using Spark to Process Large Text Corpora

### Dataset
- Amazon Review Dataset

### Tasks

#### Part 1 RDDs
The usage of RDDs enabled efficient preprocessing and calculations by using the available transformations, which allowed grouping the data by the necessary keys easily. Figuring out
how and when to use broadcast variables and at which times it was necessary to perform actions on the RDDs was a bit of a challenge at first. At times it made the RDDs feel very
inefficient due to the lazy evaluation and sudden very long runtimes at the actions. 


#### Part 2 DatasetsDataFrames - SparkML and Pipelines
The Spark Pipeline seems to be a user-friendly abstraction of a machine learning pipeline, with a variation of tools available. Of note is the lack in flexibility of modelling, being limited
to these transformations and problematic beyond them. For example, we struggled with implementing a filter for single characters, after applying the tokenizer & stopwords remover.


#### Part 3 Text Classification
The task of multi-class classification of the reviews dataset proves to be an appropriate use-case for showcasing the challenges of data-intensive computing. We reached f1-score values of
60%+ for the dev set, with fit_time approx 2min, transform_time approx. 6s, evaluate_time approx 22s.



We observed that unreliable access to cluster resources made our experimental setup unreliable too, especially for high-demand contexts.

[Overleaf project](httpswww.overleaf.com2915981151zzqyhfznckzc#dcbaeb)
	