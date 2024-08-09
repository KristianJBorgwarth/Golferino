class ErrorMessage:
    @staticmethod
    def value_cant_be_empty(field_name):
        return f"{field_name} must not be empty"

    @staticmethod
    def must_contain_only_letters(field_name):
        return f"{field_name} must contain only letters"

    @staticmethod
    def must_be_at_least(field_name, length):
        return f"{field_name} must be at least {length} characters long"

    @staticmethod
    def must_be_less_than(field_name, length):
        return f"{field_name} must be less than or equal to {length} characters long"

    @staticmethod
    def must_contain_at_symbol(field_name, symbol):
        return f"{field_name} must contain {symbol}"
    
    @staticmethod
    def must_be_of_type(field_name, type):
        return f"{field_name} must be of type {type}"

    # TODO: Should add a type name, to dynamically describe what type already exists for reusability
    @staticmethod
    def already_exists(field_name):
        return f"({field_name}) already exists."

    @staticmethod
    def unspecified_error(message):
        return message

    @staticmethod
    def not_found(message):
        return message
