import sys

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()

    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Not enough arguments"
        except IndexError:
            return "Not enough arguments"
        except KeyError:
            return "Contact not found"

    return inner

@input_error
def add_contact(args, contacts):
    name, phone = args

    contacts[name] = phone
    
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, phone = args

    if not name in contacts:
        raise KeyError
    
    contacts[name] = phone
    
    return "Contact updated."

@input_error
def get_phone(args, contacts):
    name = args[0]

    if not name in contacts:
        raise KeyError
    
    return contacts[name]

@input_error
def list(args, contacts):
    if len(contacts) == 0:
        return 'Contacts are empty.'
    
    result = ''
    
    for name, phone in contacts.items():
        result += f'{name}: {phone}\n'

    return result

def main():
    contacts = {}

    print('Welcome to the assistant bot!')

    while True:
        user_input = input('Enter a command: ')
        command, *args = parse_input(user_input)

        if command in ['close', 'exit']:
            
            print('Good bye!')

            break
        
        elif command == 'hello':
            
            print('How can I help you?')
        
        elif command == 'add':
            
            print(add_contact(args, contacts))
        
        elif command == 'change':
            
            print(change_contact(args, contacts))

        elif command == 'phone':
            
            print(get_phone(args, contacts))

        elif command == 'all':
            
            print(list(None, contacts))
        
        else:
            print('Invalid command.')
    

if __name__ == '__main__':
    main()