from flask import flash

# Globals
global_message_queue = []

# Utility Functions

def check_messages():
    global global_message_queue
    messages = {
        "review_saved" : "Your review has been saved. Thank you.",
        "sorry_old_model" : "Sorry, but your review could not be submitted. "
                            "There is currently a problem with our database that we are working to resolve.",
        "thank_volunteer" : "Thank you for sending an encouraging e-mail to your volunteer."
    }
    for message in global_message_queue:
        if message is not 0:
            flash(messages[message])
    del global_message_queue[:]
    return
