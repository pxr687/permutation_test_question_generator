# permutation_test_question_generator

First version of a permutation test question generator. This probabilistically generates data and instructs the user to carry out a permutation test on the data. There is also a function for the user to compare their p-value to a precomputed p-value, to check they have done the test correctly.

The notebook that a user will see is `permutation_test_question_generator.ipynb`. This notebook imports the question generating functions (and question marking functions) from `permutation_test_question_generator.py`.

This notebook be used interactively on Deepnote via the following link:
https://deepnote.com/project/Permutation-Test-Question-Generator-JHSmvd00SfSJn5-Mj7bQcw/%2Fpermutation_test_question_generator%2Fpermutation_test_question_gen.ipynb

Currently, there is only one question generating function, which generates data for a two-sample permutation test of a difference in means.

In the future, maybe a question generating function for a two sample permutation test of proportions etc. could also be added.

