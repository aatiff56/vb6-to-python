from dateutil.parser import parse

LeaderSVR = None

def IsDate(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except BaseException as error:
        return False