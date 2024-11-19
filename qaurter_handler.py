def get_fy_qtr_suffix(year, qtr):
    year_suffix = str(year)[-2:]
    # Map quarters to their desired format
    quarter_map = {
        "qtr1": "Q1",
        "qtr2": "Q2",
        "qtr3": "Q3",
        "qtr4": "Q4"
    }

    qtr_suffix = quarter_map[qtr]

    # Format the sheet name
    return year_suffix + "_" + qtr_suffix


def get_six_months_ago(year, quarter):
    # Define the mapping for quarters
    quarters = ['qtr1', 'qtr2', 'qtr3', 'qtr4']

    # Calculate the current quarter index
    current_quarter_index = quarters.index(quarter)

    # Calculate the six months ago quarter index
    six_months_ago_quarter_index = (current_quarter_index - 2) % 4
    six_months_ago_quarter = quarters[six_months_ago_quarter_index]

    # Adjust the year based on the quarter change
    if current_quarter_index < 2:
        six_months_ago_year = year - 1
    else:
        six_months_ago_year = year

    return six_months_ago_year, six_months_ago_quarter

