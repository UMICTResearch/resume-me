import resumeme.feedback.config as CONFIG
import resumeme.feedback.constant as CONSTANT

# Utility Functions


# converts a dict to a list for storage and iteration
def dict_to_list(data):
    print "########################### dict_to_list ##########################"
    print list(sorted(data.items()))
    return list(sorted(data.items()))

# returns a direct link to the nested question data dict
def get_question_config(group, id):
    return CONFIG.all_questions[group][id]

# returns a question group as a sorted list (in the config file it is a dict)
def get_question_group_config_list(group):
    return dict_to_list(CONFIG.all_questions[group])

def get_message_text(message):
    messages = {
        "review_saved" : "Your review has been saved. Thank you.",
        "sorry_old_model" : "Sorry, but your review could not be submitted. "
                            "There is currently a problem with our database that we are working to resolve.",
        "thank_volunteer" : "Thank you for sending an encouraging e-mail to your volunteer."
    }
    return(messages[message])

