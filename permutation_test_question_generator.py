import numpy as _np
import matplotlib.pyplot as _plt
import pandas as _pd
from IPython.display import display, Markdown


def perm_question_cont_2_group():
    """This function generates data for a two-sample permutation test of
    a mean difference. It also prints out instructions to the user about
    which hypothesis to test. This function returns:

    * a dataframe containing the simulated data
    * a 'correct' p-value from a correctly computed permutation test with
      the same number of iterations as the test that the user is instructed to
      perform
    * two strings containing hints to the user about how to correctly perform
      their test

    The user can compare the p-value from their test to the 'correct' p-value
    using the check_my_p_value() function."""

    # making plots look like R

    _plt.style.use('ggplot')
    _plt.rc('axes', facecolor='white', edgecolor='black',
            axisbelow=True, grid=False)

    # a list of colours for the plots

    colours = [
        'tab:blue',
        'tab:orange',
        'tab:green',
        'tab:red',
        'tab:purple',
        'tab:brown',
        'tab:pink',
        'tab:gray',
        'tab:olive',
        'tab:cyan',
        ]

    # selection two colours (one for each group histogram)

    two_colours = _np.random.choice(colours, size=2, replace=False)

    # a selection of possible outcome variables (chosen so the drug intervention
    #  should reduce them, to make instructions about calculating the p-value
    #  simple (e.g. the direction of the hypothesis test)

    outcome_variable_continuous = _np.array([
        'back_pain_score',
        'aggression_score',
        'memory_impairment_score',
        'maths_test_anxiety_score',
        'writing_test_anxiety_score',
        'neuroticism_score',
        'stress_score',
        'pain_score',
        'depression_score',
        'anxiety_score',
        'mania_score',
        'paranoia_score',
        'fatigue_score',
        'mood_instability_score',
        'agoraphobia_score',
        ])

    # selecting what the outcome variable will be

    outcome = _np.random.choice(outcome_variable_continuous)

    # deciding on whether there will be a large or small (and probably not
    # significant) difference between the sample means

    coinflip = _np.random.choice(['small', 'large'])

    # setting the size of each group (but keeping them somewhat close)

    n1 = int(_np.random.uniform(15, 200))
    n2 = _np.abs(n1 + int(_np.random.normal(0, n1 / 10)))

    # setting the mean and sd of the first sample

    mu_1 = _np.random.randint(20, 75)
    sd_1 = _np.random.randint(1, 7)

    # setting the mean of the second sample (needed if the difference is to
    # potentially be large)

    mu_2 = mu_1 - int(_np.random.uniform(1, 5))
    sd_2 = sd_1 + _np.random.randint(0, 5)

    if coinflip == 'large':

        sample_1 = _np.random.normal(mu_1, sd_1, n1).astype('int')

        sample_2 = _np.random.normal(mu_2, sd_2, n2).astype('int')
    else:

    # if the difference between the samples is to be small, sample 2's mean should
    # be sample_1's mean plus or minus a small amount

        sample_1 = _np.random.normal(mu_1, sd_1, n1).astype('int')

        sample_2 = _np.random.normal(mu_1 + _np.random.normal(0, 0.5),
                sd_2, n2).astype('int')

    # printing instructions for the user and showing plots of each group

    display(Markdown(f'''
\nThe graphs below show the {outcome.replace('_', ' ')}s of two groups of 
participants.'''))
    display(Markdown(f'''
\nOne group received a placebo; one group received a drug which is hypothesized
 to reduce {outcome.replace('_score', '').replace('_', ' ')}.'''))
    display(Markdown('''
Participants were randomly assigned to each group.
'''))

    # plotting the first sample

    _plt.figure()
    _plt.hist(sample_1, color=two_colours[0], label='placebo', bins=6)
    _plt.axvline(sample_1.mean(), color='red', label='placebo group average')

    # plotting the other sample, invisibly, to ensure the axes are comparable on both plots

    _plt.hist(sample_2, alpha=0)
    _plt.xlabel(outcome.replace('_', ' '))
    _plt.ylabel('Frequency')
    _plt.legend()

    # plotting the second sample

    _plt.figure()
    _plt.hist(sample_2, color=two_colours[1], label='drug', bins=6)
    _plt.axvline(sample_2.mean(), color='blue', label='drug group average')

    # plotting the other sample, invisibly, to ensure the axes are comparable on both plots

    _plt.hist(sample_1, alpha=0)
    _plt.xlabel(outcome.replace('_', ' '))
    _plt.ylabel('Frequency')
    _plt.legend()
    _plt.show()

    # creating labels for each group, to put in a dataframe

    placebo_labels = _np.repeat('placebo', len(sample_1))
    drug_labels = _np.repeat('drug', len(sample_2))

    display(Markdown('''
The raw data for each group is contained in the dataframe below, which is stored
in the variable called `df`:
'''))

    # creating a dataframe for the user to get the data from

    df = _pd.DataFrame({'group': _np.append(placebo_labels,
                       drug_labels), outcome: _np.append(sample_1,
                       sample_2)})

    display(df)

    display(Markdown('''
\nType `df` in an empty cell and run it to access the dataframe.'''
            ))

    display(Markdown(f'''
\nPerform a permutation test with 10000 iterations. Test whether the difference
between the mean {outcome.replace('_', ' ')} of \neach group is large enough to
convince us that the drug works.'''))

    display(Markdown(f'''
\nTo get the actual mean difference, subtract the mean {str(outcome.replace('_', ' '))}
of the drug group from the mean {outcome.replace('_', ' ')} of the placebo group
. E.g:'''))
    display(Markdown('\n`mean difference = placebo mean - drug mean`'))

    # performing a permutation test to get a p-value to check the user's p-value against

    n_iters = 10000

    fake_differences = _np.zeros(n_iters)

    for i in _np.arange(n_iters):

        together = _np.append(sample_1, sample_2)

        shuffled = _np.random.permutation(together)

        fake_1 = shuffled[:len(sample_1)]

        fake_2 = shuffled[len(sample_1):]

        fake_diff = fake_1.mean() - fake_2.mean()

        fake_differences[i] = fake_diff

    actual_diff = sample_1.mean() - sample_2.mean()
    answer_p = _np.count_nonzero(fake_differences >= actual_diff) \
        / 10000

    # More instructions to the user

    display(Markdown('''\n
To check your answer, save the p-value calculated from
your permutation test in a variable called `my_p_value`.'''
            ))
    display(Markdown('''
Then scroll down to the bottom of the notebook, to the "check your answer" 
section.'''
            ))
    display(Markdown('''
If you need a hint about what to do for the actual permutation test, run the 
following command in an empty cell:

`display(Markdown((hint_test))`'''))
    display(Markdown('''
If you need a hint about how to calculate the p-value from your permutation test
run the following command in an empty 
cell:

`display(Markdown(hint_p_value))`'''))

    # defining a hint string to explain what the user's permutation test should
    # do, if the user is stuck

    hint_test = \
        """
The structure of the permutation test should be as follows. You need to:
		   
* Create an array to store the results of your simulation, this should be 10000
 elements long.
		   
* Set up a for loop with 10000 iterations.
		   
* On each iteration you should combine the """ \
        + str(outcome.replace('_', ' ')) \
        + """s of the placebo group and the drug group into one array.
		   
* You should then shuffle the combined scores. Under the null hypothesis that the
 drug doesn't reduce the """ \
        + str(outcome.replace('_', ' ')) \
        + """s,
then the scores should be exchangable between the groups. (E.g. if the drug does
not work, we would expect the scores, on average, to be similar in the placebo group
and the drug group).
		   
* You should then split the shuffled scores into two groups, a fake placebo group and
a fake drug group. The groups should be the same size as the original groups. 
		   
* You should then calculate the fake mean difference (placebo placebo mean - fake drug mean) 
between the two fake groups, and store this difference in the results array.
                   
* You should then calculate a p-value by calculating the proportion of the simulated
mean differences which are greater than or equal to the actual mean difference
(`placebo mean - drug mean`})"""

    # defining a hint string to explain how to calculate the p-value, if the user is stuck

    hint_p_value = \
        """\nBecause the experimental hypothesis is that the drug *reduces* """ \
        + str(outcome.replace('_', ' ')) \
        + """s, then, if the drug is effective, \nthe """ \
        + str(outcome.replace('_', ' ')) \
        + """s in the placebo group should be much higher than the """ \
        + str(outcome.replace('_', ' ')) \
        + """s in the drug group. \nSo the mean difference in """ \
        + str(outcome.replace('_', ' ')) \
        + """s between the placebo group and the drug group should be large....
		      
The permutation test simulates a world where the drug is not effective, where the """ \
        + str(outcome.replace('_', ' ')) \
        + """s are \nexchangable between the two groups, because the drug doesn't work, and doesn't reduce the """ \
        + str(outcome.replace('_', ' ')) \
        + """s.
                      
We can calculate the p-value by finding the proportion of simulated mean differences which were
greater than or equal to the actual mean difference.
                      
This tells us how likely/unlikely our actual mean difference would be if the drug was not effective.
                      
If the p-value is large, this means the actual mean difference is not unlikely in the 'null world' 
which we have simulated (a world in which receiving the drug or placebo makes no difference to the """ \
        + str(outcome.replace('_', ' ')) \
        + """s...).
		      
If the p-value is small, this means that the actual mean difference between the placebo and drug
group is very unlikely in the 'null world', and so we can conclude that the actual world is probably
not like the null world, and therefore we can conclude that that drug works.
                      
To calculate the p-value you should use the >= operator to find the simulated mean differences
which were greater than or equal to the actual mean difference.
		      
Using the >= operator correctly on the simulation results array will give you a boolean array 10000
elements long, which is True where the simulated mean difference was larger than or equal to the actual
mean difference. It will be False otherwise.
		      
Then you should count how many simulated mean differences were greater than or equal to the actual mean
difference. Because python treats True as 1, and False as 0, you can count the number of trues by taking
the sum of the boolean array.
		      
Once you have counted the number of simulated mean differences were greater than or equal to the actual
mean difference, you should divide the count by the number of simulated scores (10000)."""

    # return the dataframe for the user to get the data from, the correct 
    # p-value to compare the user's against, and the two hint strings

    return (df, answer_p, hint_test, hint_p_value)


def check_my_p_value(answer_p, my_p_value):
    """This function is to check the user's permutation p-value is
    close enough to a 'correct' p-value infer that they've done
    the simulation correctly, and suggest some hints to them if
    they have not..."""

    # this value is slightly larger than the one found through testing,
    # to avoid falsely concluding that the user has done the test incorrectly

    is_close = _np.abs(answer_p - my_p_value) <= 0.026

    if is_close == True:
        display(Markdown('Great! Your p-value is in the right sort of range.'
                ))
        display(Markdown('The p-value we got from a pre-computed permutation test was'
                , answer_p))

    if is_close == False:

        if answer_p > my_p_value:
            display(Markdown('\nHmmm, your p-value is too small.'))
            display(Markdown('\nThe p-value should be somewhere around: '
                    , answer_p))
            display(Markdown('''
To check you are running the permutation test correctly, consider checking out a
hint by running the following command in an empty cell:

display(Markdown(hint_test))'''))
            display(Markdown('''
To check you are calculating the p-value correctly, consider checking out a hint
by running the following command in an empty cell:

display(Markdown(hint_p_value))'''))

        if answer_p < my_p_value:
            display(Markdown('\nHmmm, your p-value is too large.'))
            display(Markdown('\nThe p-value should be somewhere around: '
                    , answer_p))
            display(Markdown('''
To check you are running the permutation test correctly, consider checking out 
a hint by running the following command in an empty cell:

`display(Markdown(hint_test))`'''))
            display(Markdown('''
To check you are calculating the p-value correctly, consider checking out a hint
by running the following command in an empty cell:

`display(Markdown((hint_p_value))`'''))
