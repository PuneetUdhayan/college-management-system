class IncorrectTimeFormat(Exception):

    def __init__(self,message):
        super().__init__(message)


class IncorrectMinutesValue(Exception):

    def __init__(self,message = "Minutes value must be between 0 and 1,440"):
        super().__init__(message)


class TimeConversions():
    """TimeConverstion class is used to convert time from HH:MM format
    to an integer reprsenting minutes from midnight and vice versa
    """

    @staticmethod
    def time_to_minutes(time:str) -> str:

        timedata = time.split(':')

        try:
            hour = int(timedata[0])
            if hour > 24:
                raise Exception()
            minutes = int(timedata[1])
            if minutes > 60:
                raise Exception()
            return (hour*60)+minutes
        except Exception as e:
            raise IncorrectTimeFormat(str(e))


    @staticmethod
    def minutes_to_time(minutes:int) -> int:

        if minutes < 0 or minutes > 1440:
            raise IncorrectMinutesValue()
        
        hour = minutes//60
        minutes = minutes%60

        return f"{hour}:{minutes}"