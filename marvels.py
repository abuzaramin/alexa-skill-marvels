import json

Player_LIST = ["Captain America", "Iron man", "Wolvarine", "Spiderman", "thor", "hulk"]

Player_BIOGRAPHY = {"captain america":"Captain America is a superhero appearing in American comic books published by Marvel Comics. Captain America is the alter ego of Steve Rogers, a frail young artist enhanced to the peak of human perfection by an experimental super-soldier serum after joining the military to aid the United States government's efforts in World War II.",

"iron man":"Iron Man is a fictional superhero appearing in American comic books published by Marvel Comics. Iron Man possesses a wealth of powers through his powered armor suit. These powers include super strength, the ability to fly, durability, and a number of weapons. The primary weapons used by Iron Man are rays that are shot from the palms of his gauntlets",

"wolvarine":"Wolverine, is a fictional character from 20th Century Fox's superhero film series X-Men, portrayed by Hugh Jackman and based on the Marvel Comics character Wolverine. Wolvarine strengths are Enhanced strength, speed, stamina, durability, agility, dexterity, and reaction time. Superhuman senses and animal-like attributes. Regeneration and slowed aging. Indestructible bones via adamantium-infused skeleton",

"spiderman":"Spider-Man is a fictional superhero. Spider-Man's strength and agility stand far above those of the average human, allowing him to lift nearly ten tons and to leap and move at incredible speeds with high accuracy.",

"thor":"Thor Odinson is a fictional superhero appearing in American comic books published by Marvel Comics. He also possesses superhuman strength, speed, agility, durability and immunity to most diseases.",

"hulk":"The Hulk is a fictional superhero appearing in publications by the American publisher Marvel Comics. Hulk powers are , Incredible superhuman strength, durability, and healing factor. Becomes more powerful as anger increases. As Banner, possesses a genius-level intellect & is an expert in multiple scientific fields, particularly the studies of physics & radiation"}


def lambda_handler(event, context):
    # TODO implement
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()
        
def on_start():
    print("Session Started.")

def on_launch(event):
    onlunch_MSG = "Hi, welcome to the My Favourite Marvels Character Alexa Skill. My favourite marvel characters are: " + ', '.join(map(str, Player_LIST)) + ". "\
    "If you would like to hear more about a particular character, you could say for example: tell me about spriderman?"
    reprompt_MSG = "Do you want to hear more about a particular character?"
    card_TEXT = "Pick a marvel character."
    card_TITLE = "Choose a marvel character."
    return output_json_builder_with_reprompt_and_card(onlunch_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def on_end():
    print("Session Ended.")
    
def intent_scheme(event):
    
    intent_name = event['request']['intent']['name']

    if intent_name == "characterBio":
        return character_bio(event)        
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)

def character_bio(event):
    name=event['request']['intent']['slots']['character']['value']
    player_list_lower=[w.lower() for w in Player_LIST]
    if name.lower() in player_list_lower:
        reprompt_MSG = "Do you want to hear more about a particular character?"
        card_TEXT = "You've picked " + name.lower()
        card_TITLE = "You've picked " + name.lower()
        return output_json_builder_with_reprompt_and_card(Player_BIOGRAPHY[name.lower()], card_TEXT, card_TITLE, reprompt_MSG, False)
    else:
        wrongname_MSG = "You haven't used the full name of a character. If you have forgotten which characters you can pick say Help."
        reprompt_MSG = "Do you want to hear more about a particular character?"
        card_TEXT = "Use the full name."
        card_TITLE = "Wrong name."
        return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
    
def stop_the_skill(event):
    stop_MSG = "Thank you. Bye!"
    reprompt_MSG = ""
    card_TEXT = "Bye."
    card_TITLE = "Bye Bye."
    return output_json_builder_with_reprompt_and_card(stop_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)
    
def assistance(event):
    assistance_MSG = "You can choose among these characters: " + ', '.join(map(str, Player_LIST)) + ". Be sure to use the full name when asking about the character."
    reprompt_MSG = "Do you want to hear more about a particular character?"
    card_TEXT = "You've asked for help."
    card_TITLE = "Help"
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def fallback_call(event):
    fallback_MSG = "I can't help you with that, try rephrasing the question or ask for help by saying HELP."
    reprompt_MSG = "Do you want to hear more about a particular character?"
    card_TEXT = "You've asked a wrong question."
    card_TITLE = "Wrong question."
    return output_json_builder_with_reprompt_and_card(fallback_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
    
def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict

def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict
    
def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict    

def response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeach_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict

def output_json_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value)
    return response_dict