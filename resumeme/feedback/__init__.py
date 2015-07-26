# Add jinja filters
from resumeme import app


# Date-Time formatting to make them look nicer
@app.template_filter('feedback_datetime')
def feedback_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="EE dd.MM.y HH:mm"
    return value.strftime("%c")
