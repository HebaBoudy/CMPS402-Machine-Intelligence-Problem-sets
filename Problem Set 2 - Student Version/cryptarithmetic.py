import re
from CSP import Assignment, Problem, Constraint, BinaryConstraint
from typing import Callable, Dict, List, Any, Tuple
# TODO (Optional): Import any builtin library or define any helper function you want to use


# this function is called three times for each LHS0 , LHS1 and RHS because their logic is very similar
# it takes the word (either LHS0,LHS1,RHS and add their domains and add them to the variables list , it generates carries as well )
# the flag parameter to distinguish LHS words from RHS words in order to handle carry counts
# in case its RHS , the carries generation is not made

def Initialize_variables_and_domains(word: str, domains: Dict,  variables: List, explored: set, all_carries: set, flag: bool) -> set or List or Dict:
    numbers = [i for i in range(10)]

    carrycount = 0
    for letter in word:
        if letter not in explored:

            explored.add(letter)
            variables.append(letter)  # add the variable to the variables list
            # if it the mmost significant , discard zero from its domain
            if (letter == word[0]):
                domains.update({letter: numbers[1::]})
            else:
                domains.update({letter: numbers})
        else:  # explored before but it maybe occured in the most significant place for the first time
            if (letter == word[0]):
                domains.update({letter: numbers[1::]})
        if (flag == 0):  # the function is called on LHS0 or LHS1 word NOT RHS
            carry = chr(ord('a')+carrycount)
            if (carry not in explored):
                explored.add(carry)
                variables.append(carry)
                domains.update({carry: [0, 1]})
                all_carries.add(carry)
                carrycount += 1
                # else do nothing , the carry  already exists when initializing LHS0

    return domains, explored, variables, all_carries

# ----------------------------------COMBINING DOMAINS ------------------------------------------------------


def Combine_Two_domains(letter1: str, letter2: str, domains: Dict) -> list:
    new_domain = []
    for i in range(len(domains[letter1])):
        for j in range(len(domains[letter2])):
            # Tuple of the two values
            new_domain.append((domains[letter1][i], domains[letter2][j]))
    return new_domain


def Combine_Three_domains(letter1: str, letter2: str, letter3: str, domains: Dict):
    new_domain = []
    for i in range(len(domains[letter1])):
        for j in range(len(domains[letter2])):
            for k in range(len(domains[letter3])):
                # Tuple of the two values
                new_domain.append(
                    (domains[letter1][i], domains[letter2][j], domains[letter3][k]))
    return new_domain
# --------------------------------------------------------------------------------------------------------
# ------------------------------RHS LHS EQUATIONS ---------------------------------------------------------


def Check_Equation(number1: List, number2: List):
    # print("Inside Check_Equation")
    # print("number1 is: ", number1)
    # print("number2 is: ", number2)
    # first check if there is a triple tuple
    is_triple = False
    if (len(number1) == 3):
        LHS_combined = number1
        RHS_Combined = number2
        is_triple = True

    if (len(number2) == 3):
        LHS_combined = number2
        RHS_Combined = number1
        is_triple = True
    if (is_triple):
        return ((LHS_combined[0]+LHS_combined[1]+LHS_combined[2] == RHS_Combined[0]+10*RHS_Combined[1]))
    else:
        if number1[0] + number1[1] == number2[0] + 10*number2[1]:
            return True
        elif number2[0] + number2[1] == number1[0] + 10*number1[1]:
            return True
        return False

        # ----------------------------------------------------------------------------------------------------------


def Equal(number1: int, number2: int) -> bool:

    if (number1 == number2):
        return True
    else:
        return False


def Add_Distinct_Variables_Constraints(variables: List, constraints: List):
    carries = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'C0', 'C1', 'C2'}

    def Not_Equal(number1: int, number2: int): return number1 != number2
    for variable in variables:
        if len(variable) == 1 and variable not in carries and variable != '#':
            for next_variable in variables[1::]:
                if (len(next_variable) == 1 and next_variable not in carries and next_variable != '#'):
                    if (next_variable != variable):
                        constraint = BinaryConstraint(
                            (variable, next_variable), Not_Equal)
                        constraints.append(constraint)
# -----------------------------------CHEKING FOR COMBINED VARIABLES CONSTRAINTS---------------------------


def Index_0(number1: int, number2: List) -> bool:
    if (isinstance(number1, int)):
        return (number2[0] == number1)
    else:
        return (number1[0] == number2)


def Index_1(number1: int, number2: List) -> bool:
    if (isinstance(number1, int)):
        return (number1 == number2[1])
    else:
        return (number2 == number1[1])


def Index_2(number1: int, number2: List) -> bool:
    if (isinstance(number1, int)):
        return (number1 == number2[2])
    else:
        return (number2 == number1[2])
# --------------------------------------------------------------------------------------------------------


def Reverse(x) -> str:  # reversing string
    return x[::-1]


class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None:
                continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) + ")"
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match:
            raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        # TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).

        problem.variables = []
        problem.domains = {}
        problem.constraints = []
        explored = set()
        all_carries = set()

        problem.domains, explored,  problem.variables, all_carries = Initialize_variables_and_domains(
            LHS0, problem.domains, problem.variables, explored, all_carries, 0)
        problem.domains, explored,  problem.variables, all_carries = Initialize_variables_and_domains(
            LHS1, problem.domains, problem.variables, explored, all_carries, 0)
        problem.domains, explored,  problem.variables, all_carries = Initialize_variables_and_domains(
            RHS, problem.domains, problem.variables, explored, all_carries, 1)
# If the LHS size != RHS size , complete the smaller one with any dummy variable and assign only zero
#  to its domain in order not to change anything in the logic for testcases 5,6
        diffrence = len(LHS0)-len(LHS1)
        if (diffrence != 0):
            empty_str = ''
            for i in range(diffrence):
                empty_str += '#'
            empty_str += LHS1
            LHS1 = empty_str
            problem.domains.update({'#': [0]})
            problem.variables.append('#')

        LHS0 = Reverse(LHS0)
        LHS1 = Reverse(LHS1)
        RHS = Reverse(RHS)

        counter_carry = -1
        for i in range(0, len(LHS0)):
            # ------------------------------COMBINING RHS--------------------------------------------------
            carry = chr(ord('a')+i)
            Carry_RHS_Combined = RHS[i]+carry
            problem.variables.append(Carry_RHS_Combined)
            new_domain = Combine_Two_domains(
                RHS[i], carry, problem.domains)
            problem.domains.update({Carry_RHS_Combined: new_domain})
            First_constraint = BinaryConstraint(
                (Carry_RHS_Combined, RHS[i]), Index_0)
            problem.constraints.append(
                First_constraint)
            Second_constraint = BinaryConstraint(
                (Carry_RHS_Combined, carry), Index_1)
            problem.constraints.append(
                Second_constraint)
            # --------------------------------------------------------------------------------------------
            # ----------------------------COMBINING LHS---------------------------------------------------
            if (i == 0):
                LHS0_LHS1_Combined = LHS0[i]+LHS1[i]
                problem.variables.append(LHS0_LHS1_Combined)
                new_domain = Combine_Two_domains(
                    LHS0[i], LHS1[i], problem.domains)
                problem.domains.update({LHS0_LHS1_Combined: new_domain})
                First_constraint = BinaryConstraint((LHS0_LHS1_Combined, LHS0[i]),
                                                    Index_0)
                Second_constraint = BinaryConstraint((LHS0_LHS1_Combined, LHS1[i]),
                                                     Index_1)
                problem.constraints.append(First_constraint)
                problem.constraints.append(Second_constraint)
            else:
                carry = chr(ord(carry)-1)
                LHS0_LHS1_Combined = LHS0[i]+LHS1[i] + carry
                problem.variables.append(LHS0_LHS1_Combined)
                new_domain = Combine_Three_domains(
                    LHS0[i], LHS1[i], carry, problem.domains)
                problem.domains.update({LHS0_LHS1_Combined: new_domain})
                First_constraint = BinaryConstraint((LHS0_LHS1_Combined, LHS0[i]),
                                                    Index_0)
                Second_constraint = BinaryConstraint((LHS0_LHS1_Combined, LHS1[i]),
                                                     Index_1)
                Third_constraint = BinaryConstraint((LHS0_LHS1_Combined, carry),
                                                    Index_2)
                problem.constraints.append(First_constraint)
                problem.constraints.append(Second_constraint)
                problem.constraints.append(Third_constraint)
            # -----------------------------------------------------------------------------------------------------------
            Equation_Constraint = BinaryConstraint(
                (LHS0_LHS1_Combined, Carry_RHS_Combined), Check_Equation)
            problem.constraints.append(Equation_Constraint)
            counter_carry += 1

        # testcase 4 and 5
        if (len(LHS0) == len(LHS1) and len(LHS1) == len(RHS)):
            last_carry = chr(ord('a')+counter_carry)
            problem.domains[last_carry] = [0]
        # -----------------------------------------------------------------------------------------------------------
        else:
            last_carry = chr(ord('a')+counter_carry)
            Last_constraint = BinaryConstraint((RHS[counter_carry+1], last_carry),
                                               Equal)
            problem.constraints.append(Last_constraint)
        Add_Distinct_Variables_Constraints(
            problem.variables, problem.constraints)\
            # -----------------------------------------------------------------------------------------------------------
        return problem
    # Read a cryptarithmetic puzzle from a file

    @ staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())


# p = CryptArithmeticProblem.from_file('puzzles/puzzle_5.txt')
