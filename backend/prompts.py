"""Prompt templates for LLM interactions in Twenty Questions game."""


def get_set_object_prompt():
    """Generate prompt for Player 1 to choose an object."""
    return """You are playing Twenty Questions as Player 1. Think of a common, concrete object that someone could guess in 20 yes/no questions.

IMPORTANT: Choose a RANDOM and VARIED object. Try to pick something different from what you might have chosen before.

The object can be anything - an everyday item, animal, food, vehicle, tool, piece of clothing, plant, structure, toy, or any other common, tangible thing.

Examples of good objects: pencil, dog, apple, car, hammer, shirt, tree, house, ball, book, elephant, pizza, bicycle, scissors, hat, flower, bridge, doll, cup, penguin, sandwich, airplane, wrench, shoes, cactus, tower, puzzle, phone, butterfly, cookie, boat, screwdriver, gloves, grass, fence, blocks, keys, shark, banana, train, lamp, jacket, mushroom, wall, kite

Make sure your object is:
- Common enough that people would know it
- Concrete and tangible (not abstract)
- Not too specific (avoid "red sports car" - just "car" is better)
- Not too obscure (avoid "cell wall" or "mitochondria")

Pick ONE specific object. Respond with ONLY the object name, nothing else."""


def get_ask_question_prompt(conversation_history):
    """Generate prompt for Player 2 to ask a strategic question."""
    prompt = """You are playing Twenty Questions as Player 2. Your goal is to guess the object Player 1 is thinking of by asking strategic yes/no questions.

STRATEGY:
- Start broad (e.g., "Is it an animal?") and narrow down
- Use each question to eliminate large categories
- Build on previous answers to narrow the possibilities
- Ask questions that split the remaining possibilities in half when possible

EXAMPLES OF GOOD QUESTIONS:
- "Is it an animal?"
- "Is it something you can eat?"
- "Is it found indoors?"
- "Does it have wheels?"
- "Is it made of metal?"

Ask ONE strategic yes/no question that will help you narrow down what the object might be. Only ask the question, nothing else."""

    if conversation_history:
        prompt += "\n\nPrevious questions and answers:\n"
        for qa in conversation_history:
            prompt += f"Q: {qa['question']}\nA: {qa['answer']}\n"
        prompt += "\nBased on the information above, ask your next strategic question:"
    
    return prompt


def get_make_guess_prompt(conversation_history):
    """Generate prompt for Player 2 to make a guess."""
    prompt = """You are playing Twenty Questions as Player 2. Based on all the questions and answers, make your best guess for what object Player 1 is thinking of.

Think about what you've learned:
- What category does it belong to?
- What are its key characteristics?
- What objects fit all the answers you've received?

Respond with ONLY the object name, nothing else. Do not add prefixes like "I think it's" or "My guess is" - just state the object."""

    if conversation_history:
        prompt += "\n\nPrevious questions and answers:\n"
        for qa in conversation_history:
            prompt += f"Q: {qa['question']}\nA: {qa['answer']}\n"
        prompt += "\nBased on all the above information, what is your guess?"
    
    return prompt


def get_decide_action_prompt(remaining_questions, conversation_history):
    """Generate prompt for Player 2 to decide whether to ask or guess."""
    prompt = f"""You are playing Twenty Questions as Player 2. You have {remaining_questions} questions remaining.

DECISION CRITERIA:
- If you are CONFIDENT about the answer based on the information gathered, respond with: guess
- If you need MORE INFORMATION to narrow down the possibilities, respond with: question

Consider:
- Do you have enough information to make an educated guess?
- Are there still multiple possibilities that fit the answers?
- Would one more question significantly narrow it down?

IMPORTANT: Respond with ONLY the single word "guess" or "question", nothing else."""

    if conversation_history:
        prompt += "\n\nPrevious questions and answers:\n"
        for qa in conversation_history:
            prompt += f"Q: {qa['question']}\nA: {qa['answer']}\n"
        prompt += "\nBased on the above, should you ask another question or make a guess?"
    
    return prompt


def get_answer_question_prompt(chosen_object, question):
    """Generate prompt for Player 1 to answer a question truthfully."""
    return f"""You are playing Twenty Questions as Player 1. You are thinking of: {chosen_object}

Player 2 has asked you this question: {question}

RULES:
- You must answer TRUTHFULLY based on the object you're thinking of
- Answer "yes" if the question is true for your object
- Answer "no" if the question is false for your object
- Be precise - consider the exact wording of the question

Answer with ONLY "yes" or "no", nothing else."""

