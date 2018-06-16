# Add jinja filters
from resumeme import app


# Date-Time formatting to make them look nicer
@app.template_filter('feedback_datetime')
def feedback_datetime(value, format='medium'):
    if format == 'full':
        format="%c"
    elif format == 'medium':
        format="%A %B %d, %Y - %I:%M%p %Z"
    return value.strftime(format)
