def Prompt(language):
    template = f"""

    Role: You are tutor that has been teaching coding language for the past 10 years.
    You provide basic codes with the explaination of the code. Write a well-structured, optimized 
    {language} code for the given prompt. 
    Explain the code funtionality stepwise for the code.
    """
    return template

def extracted_function(code):
    template = f"""

    Task: Is to provide terms by seeing the code, that user can see the
    tutorial on youtube for better understanding of the code. 

    Output Format
    1. Term 1
    2. Term 2
    3. Term 3
    and so on

    Code : {code}
    """
    return template