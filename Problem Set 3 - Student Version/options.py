# This file contains the options that you should modify to solve Question 2


def question2_1():
    # TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.0,
        "discount_factor": 0.1,  # QUESTION WHY AT DISCOUNT FACTOR=0 WRONG - MORE GREEDY ?
        "living_reward": -1
    }


def question2_2():  # wrong
    # TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.1,  # Question why not working when noise =0
        "discount_factor": 0.4,
        "living_reward": -0.5  # less greedy
    }


def question2_3():
    # TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 0.1,  # greedy QUESTION WHY 0 DOES NOT WORK
        "living_reward": 1
    }


def question2_4():  # wrong
    # TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.1,
        "discount_factor": 1,
        "living_reward": -0.2
    }


def question2_5():
    # TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": 10
    }


def question2_6():
    # TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -20
    }
