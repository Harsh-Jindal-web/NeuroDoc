# prompts.py

prompts_list = [
    {"Entity": "Agreement Type", "Prompt": "Extract the type of this agreement."},
    {"Entity": "Parties Involved", "Prompt": "Extract the Parties or Companies involved in this intellectual property agreement. Answer in the most simplest form."},
    {"Entity": "Effective Date", "Prompt": "Extract the Effective date of this intellectual property agreement. Answer in the most simplest form."},
    {"Entity": "Governing Law", "Prompt": "Extract the governing law stated in this intellectual property agreement. Answer in the most simplest form."},
    {"Entity": "Dispute Resolution", "Prompt": "Extract the dispute resolution stated in this intellectual property agreement."},
    {"Entity": "Effect of Termination", "Prompt": "Extract the Effect of termination stated in this intellectual property agreement."},
    {"Entity": "Parties Address", "Prompt": "Extract the address of the parties involved in the intellectual property agreement."},
]

obligations_prompt = """
Input text: {text}
From the given input text extract all the possible obligations and return those obligations, section title, type of obligation like whether it is a task or non-task, and its frequency like one-time or recurring in the form of a list like:
[
    {{"section":"section title", "obligations":[{{"obligation":"extracted obligation", "type":"type of task", "frequency":"frequency of task"}}]}}
]
Return this format only. If no obligations, return "[]"
"""

responsibility_prompt = "Go through the agreement and identify the responsibilities of each party involved in the agreement."
rights_prompt = "Go through the agreement and identify the rights of each party involved in the agreement."
licence_type_prompt = "Go through the agreement and identify what type of license each party is having."
risk_prompt = "Go through the agreement and identify all financial, reputational and operational risks involved."
compliance_prompt = "Go through the agreement and identify all the compliance involved."
