def chunks(l, n):
    """
    :description: Takes in a list of symbols, string items, or integers, and
    then creates multiple lists inside of the initial list. Each list containing
    the number of items specified with the n parameter.

    :param l: takes in a list of items that need to be chunked into groups.
    :param n: This is the size of the chunked items. Lets you know how many
    items to put into each chunk.
    """
    n = max(1, n)
    return (l[i: i + n] for i in range(0, len(l), n))


class Params:
    # CREATE THE DIFFERENT PARAMS AS ATTRIBUTES TO BE
    # PASSED TO THE TDA CLASS THEN USED IN THEIR
    # METHODS TO CREATE DIFFERENT METHOD CALLS

    #####################################################################
    # CREATE GET COMPANIES FUNCTION:
    #####################################################################

    one_minute_10day = {
        "symbol": "stocks",  # DON'T CHANGE, change stocks exchange param in cleaned_symbols func
        "period": "10",  # 1,2,3,4,5,10
        "periodType": "day",  # day, week, month, year, ytd
        "frequency": "1",  # minute=1,5,10,15,30; daily=1, weekly=1, monthly=1
        "frequencyType": "minute",  # minute, daily, weekly, monthly
        "needExtendedHoursData": "false",
    }

    one_minute_daily = {
        "symbol": "stocks",  # DON'T CHANGE, change stocks exchange param in cleaned_symbols func
        "period": "1",  # 1,2,3,4,5,10
        "periodType": "day",  # day, week, month, year, ytd
        "frequency": "1",  # minute=1,5,10,15,30; daily=1, weekly=1, monthly=1
        "frequencyType": "minute",  # minute, daily, weekly, monthly
        "needExtendedHoursData": "false",
    }

    one_year_daily = {
        "symbol": "stocks",  # DON'T CHANGE, change stocks exchange param in cleaned_symbols func
        "period": "1",  # 1,2,3,4,5,10
        "periodType": "year",  # day, week, month, year, ytd
        "frequency": "1",  # minute=1,5,10,15,30; daily=1, weekly=1, monthly=1
        "frequencyType": "daily",  # minute, daily, weekly, monthly
        "needExtendedHoursData": "false",
    }

    ten_year_daily = {
        "symbol": "stocks",  # DON'T CHANGE, change stocks exchange param in cleaned_symbols func
        "period": "10",  # 1,2,3,4,5,10
        "periodType": "year",  # day, week, month, year, ytd
        "frequency": "1",  # minute=1,5,10,15,30; daily=1, weekly=1, monthly=1
        "frequencyType": "daily",  # minute, daily, weekly, monthly
        "needExtendedHoursData": "false",
    }

    max_daily = {
        "symbol": "stocks",  # DON'T CHANGE, change stocks exchange param in cleaned_symbols func
        "period": "20",  # 1,2,3,4,5,10,15,20
        "periodType": "day",  # day, week, month, year, ytd
        "frequency": "1",  # minute=1,5,10,15,30; daily=1, weekly=1, monthly=1
        "frequencyType": "daily",  # minute, daily, weekly, monthly
        "needExtendedHoursData": "false",
    }
