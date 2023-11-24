def e_parser(value,sep):
    from re import search
    array = []
    while True:
        result = search(sep, value)
        if result:
            result = result.span(0)
            tmp_str = value[0:result[0]]
            if tmp_str != '':
                array.append(tmp_str)
                
            value = value[result[1]:(len(value))]
        else:
            if value != '':
                array.append(value)

            break

    return array

def input_error(func):
    def true_handler(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if type(result) == str:
                print(result)
        except KeyError:
            return "No user with this name"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Please, provide name (as a single word, can use '_'), and a phone number (also as a single word) or use 'help' for input syntax tips."
    return true_handler

@input_error
def add(*args, **kwargs):
    name,number = args
    if name in users:
        return "Contact with this name already exists! Use 'change' to change existing contact or 'help' for input syntax tips."

    users[name] = number
    return f"Contact with name '{name}', phone number '{number}' successfully added!"

def hello():
    print('How can I help you?')
    
@input_error
def change(*args, **kwargs):
    name,number = args
    if str(name) in users:
        users[name] = number
        return f"Successfully edited contact '{name}'! New phone number is '{number}'."
    else:
        return f"No contact with name '{name}' found. Use 'add' to add a new contact or 'help' for input syntax tips."

@input_error
def phone(*args, **kwargs):
    name = args[0]
    if str(name) in users:
        return f"Found contact '{name}' with number {users[name]}"
    else:
        return f"No contact with name '{name}' found. Check the spelling or use 'help' for input syntax tips."
    

@input_error
def show_all(*args, **kwargs):
    if len(users) > 0:
        for k,v in users.items():
            print(f"Contact '{k}', number '{v}'")
    else:
        return 'Phone book is empty!'


@input_error
def help_me(*args, **kwargs):
    command = None
    parsed = args[0]
    if len(parsed) > 2:
        command = parsed[1] + ' ' + parsed[2]
    elif len(parsed) == 2:
        command = parsed[1]
        
    if command == None:
        tmp_l = list()
        for n in help_d:
            tmp_l.append(n)
        return f'Welcome to the phone book manual! Enter "help + the command" to see what it does!\nAwailable commands:{tmp_l}'
    else:
        if command in help_d:
            return help_d[command]
        else:
            return 'Incorrect command.'

def IsEnd(parsed):
    if parsed[0] in stop_list:
        print('Good bye!')
        working[0] = False



working = [True]
users = dict()
tip_1 = 'Use spaces between each variable (i.e. between the command, the name, and the phone number).\nDo NOT use spaces between parts of a single variable (i.e. Jack Daniels),\nuse underscores instead (Jack_Daniels)'
tip_3 = 'Adds a new phone number.\nSyntax: command + name + phone number.\nIf a contact already exists, use "change".'
tip_2 = 'Politely greets you.'
tip_4 = 'Changes phone number for a given contact.\nSyntax: command + name + phone number.\nIf a contact is not found, use "add" to add a new one.'
tip_5 = 'Shows a phone number for any given contact.\nIf a contact is not found, use "add" to add a new one.'
tip_6 = 'Shows all contacts and their respective phone numbers.'
tip_7 = 'How did we even get here?\nWhat, you gonna ask the manual about the purpose of a manual? Really?'
help_d = {'general_tips':tip_1,'hello':tip_2, 'add':tip_3, 'change':tip_4, 'phone':tip_5, 'show all':tip_6, 'help':tip_7}
func_d = {'hello':hello, 'add':add, 'change':change, 'phone':phone, 'show all':show_all, 'help':help_me, 'good bye':IsEnd, 'close':IsEnd, 'exit':IsEnd}
arg_d = {'hello':0, 'add':2, 'change':2, 'phone':1, 'show all':0,'help':'all', 'good bye':'all', 'close':'all', 'exit':'all'}
stop_list = ['good bye', 'close', 'exit']

def main():
    while working[0]:
        received_command = input()
        parsed = e_parser(received_command, ' ')
        starter = False
        if len(parsed) > 0:
            parsed[0] = parsed[0].lower()
        else:
            print('Enter the command!')
        if parsed[0] in func_d:
            starter = True
        elif len(parsed) >= 2:
            composed = parsed[0] + ' ' + parsed[1]
            if composed in func_d:
                parsed.remove(parsed[1])
                parsed[0] = composed
                starter = True
        if starter:
            if arg_d[parsed[0]] == 2:
                if len(parsed) >= 3:
                    func_d[parsed[0]](parsed[1],parsed[2])
                else:
                    print("Selected function requires two arguments!")
            elif arg_d[parsed[0]] == 1:
                if len(parsed) > 1:
                    func_d[parsed[0]](parsed[1])
                else:
                    print('One argument required!')   
            elif arg_d[parsed[0]] == 'all':
                func_d[parsed[0]](parsed) 
            else:
                func_d[parsed[0]]() 

if __name__ == '__main__':
    main()