import numpy as _np
import matplotlib.pyplot as _plt
import pandas as _pd

def TEST_perm_question_cont_2_group(n_iters):
    ''' This function is a version of the permutation test generator
    in the main repo, only this function does not print anything out.
    It is intended to be used for testing, to check the distribution of p-values
    etc., produced by the generator.'''
    
    # a list of colours for the plots
    colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive',
              'tab:cyan']
    
    # selection two colours (one for each group histogram)
    two_colours = _np.random.choice(colours, size = 2, replace = False)

    # a selection of possible outcome variables (chosen so the drug intervention should reduce them, to make instructions about 
    # calculating the p-value simple (e.g. the direction of the hypothesis test)
    outcome_variable_continuous = _np.array(['back_pain_score', 'aggression_score', 
                                            'memory_impairment_score', 'maths_test_anxiety_score', 'writing_test_anxiety_score', 'neuroticism_score',
					'stress_score', 'pain_score', 'depression_score', 'anxiety_score', 'mania_score',
					'paranoia_score', 'fatigue_score', 'mood_instability_score', 'agoraphobia_score' ])
    
    # selecting what the outcome variable will be
    outcome = _np.random.choice(outcome_variable_continuous)

    # deciding on whether there will be a large or small (and probably not significant)
    # difference between the sample means
    coinflip = _np.random.choice(['small', 'large'])
    
    # setting the size of each group (but keeping them somewhat close)
    n1 = _np.int(_np.random.uniform(15, 200))
    n2 = _np.abs(n1 + _np.int(_np.random.normal(0, n1/10)))
    
    # setting the mean and sd of the first sample
    mu_1 = _np.random.randint(20, 75)
    sd_1 = _np.random.randint(1, 7)
    
    # setting the mean of the second sample (needed if the difference is to potentially be large)
    mu_2 = mu_1 - _np.int(_np.random.uniform(1, 5))
    sd_2 = sd_1 + _np.random.randint(0, 5)

    if coinflip == 'large': 

        sample_1 = _np.random.normal(mu_1, sd_1, n1).astype('int')

        sample_2 = _np.random.normal(mu_2, sd_2, n2).astype('int')
    
    # if the difference between the samples is to be small, sample 2's mean should
    # be sample_1's mean plus or minus a small amount
    else:
        sample_1 = _np.random.normal(mu_1, sd_1, n1).astype('int')

        sample_2 = _np.random.normal(mu_1 + _np.random.normal(0,0.5), sd_2, n2).astype('int')

    
    # performing a permutation test to get a p-value to check the user's p-value against
    # n_iters is given as an argument to this function

    fake_differences = _np.zeros(n_iters)

    for i in _np.arange(n_iters):

        together = _np.append(sample_1, sample_2)

        shuffled = _np.random.permutation(together)

        fake_1 = shuffled[:len(sample_1)]

        fake_2 = shuffled[len(sample_1):]

        fake_diff = fake_1.mean() - fake_2.mean()

        fake_differences[i] = fake_diff

    actual_diff = sample_1.mean() - sample_2.mean()
    answer_p = _np.count_nonzero(fake_differences >= actual_diff)/10000
    
 
    return answer_p, sample_1, sample_2


def check_my_p_value(answer_p, my_p_value):
    
    '''This function is to check the user's permutation p-value is 
       close enough to a 'correct' p-value infer that they've done 
       the simulation correctly, and suggest some hints to them if 
       they have not...'''
    
    is_close = _np.abs(answer_p - my_p_value) <= 0.026
    
    if is_close == True:
        print('Great! Your p-value is in the right sort of range.')
    
    if is_close == False:
        
        if answer_p > my_p_value:
            print('\nHmmm, your p-value is too small.')
            print('\nThe p-value should be somewhere around: ', answer_p)
            print('\nTo check you are running the permutation test correctly, consider checking out a hint by running the following command in an \nempty cell:\n\nprint(hint_test)')
            print('\nTo check you are calculating the p-value correctly, consider checking out a hint by running the following command in an \nempty cell:\n\nprint(hint_p_value)')
                
        if answer_p < my_p_value:
            print('\nHmmm, your p-value is too large.')
            print('\nThe p-value should be somewhere around: ', answer_p)
            print('\nTo check you are running the permutation test correctly, consider checking out a hint by running the following command in an \nempty cell:\n\nprint(hint_test)')
            print('\nTo check you are calculating the p-value correctly, consider checking out a hint by running the following command in an \nempty cell:\n\nprint(hint_p_value)')
