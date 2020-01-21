def calculateCentered(message):
    if len(message) >= 16:
        return message
    empty_spaces = 16 - len(message)
    left_spaces = (empty_spaces / 2)
    final_message = " " * int(left_spaces) + message
    return final_message