import re


def is_mobile(request):
    mobile_agent = re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)

    if mobile_agent.match(request.META['HTTP_USER_AGENT']):
        return True
    return False