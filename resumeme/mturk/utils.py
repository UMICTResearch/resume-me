# Utility Functions

def get_message_text(message):
    messages = {
        "review_saved" : "Your review has been saved. Thank you.",
        "sorry_old_model" : "Sorry, but your review could not be submitted. "
                            "There is currently a problem with our database that we are working to resolve.",
        "thank_volunteer" : "Thank you for sending an encouraging e-mail to your volunteer."
    }
    return(messages[message])

