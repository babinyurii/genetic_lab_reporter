import string


low_chars = [char for char in string.ascii_lowercase]
upper_chars = [char for char in string.ascii_uppercase]
nums = [str(x) for x in range(0, 10)]

allowed_chars = low_chars + upper_chars + nums + ['_', '-']
