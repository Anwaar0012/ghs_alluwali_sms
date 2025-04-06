from django import template

register = template.Library()

@register.filter
def calculate_grade(obtained, max_marks):
    try:
        percentage = (float(obtained) / float(max_marks)) * 100
        if percentage >= 90: return 'A+'
        elif percentage >= 80: return 'A'
        elif percentage >= 70: return 'B'
        elif percentage >= 60: return 'C'
        elif percentage >= 50: return 'D'
        else: return 'F'
    except:
        return 'N/A'