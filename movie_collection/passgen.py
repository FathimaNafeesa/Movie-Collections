from substitute import *
import requests
import pyperclip
import argparse


def checkPasswords(passwords, actual_password):
    status = "Your password is OK!!"
    for password in passwords:
        if password == actual_password:
            status = "Password is Extremely vulnerable immediate attention required"
            break
        else:
            difference = findTheDifference(password, actual_password)
            if len(difference) < 2:
                status = "Password is  moderately vulnerable attention required"

    return status


def writePasswordsToClipboard(passwords):
    pwList = '\n'.join(passwords)
    print('%s passwords copied to the clipboard.' % (len(passwords)))
    pyperclip.copy(pwList)


def writePasswordsToFile(outputFile, passwords):
    with open(outputFile, 'w') as f:
        f.write('\n'.join(passwords))
    print('%s passwords written to %s' % (len(passwords), outputFile))
    f.close()


def makeRequests(target, data, passwords, findText):
    print("testing passwords... this may take a while.")
    for password in passwords:
        r = requests.post(target + "?" + data.format(password))
        if findText in r.text:
            print("Match found for password: ", password)
            return
    print("No matches found for passwords.")


parser = argparse.ArgumentParser()


def findTheDifference(s: str, t: str) -> str:
    # sort both the strings
    s_list = sorted(s)
    t_list = sorted(t)
    s_list.append(0)  # to make the length equal else we will get list index out of bounds (1 extra char in string2)
    for i in range(len(t_list)):
        if s_list[i] != t_list[i]:  # if character at i not same for both the strings, we get our answer
            return t_list[i]


"""
if __name__ == '__main__':
    parser.add_argument("-o", "--outputFile", help="The file that the password list will be written to.")
    parser.add_argument("-f", "--full", help="Full password list flag.  This can generate a very large password",
                        action="store_true")
    parser.add_argument("-c", "--copy", help="Copy password list result to the clipboard.", action="store_true")
    parser.add_argument("-n", "--numbers", help="Append numbers flag.", action="store_true")
    parser.add_argument("-t", "--target", help="The target of the HTTP POST request.")
    parser.add_argument("-d", "--data", help="The data for the post request.")
    parser.add_argument("-g", "--search",
                        help="The text to search for in POST respose that will indicate a successful login.")
    parser.add_argument("password", nargs="*")
    args = parser.parse_args()

    password = args.password[0]

    # load full or basic password list based on arguments passed in
    if args.full:
        passwords = fullSub(password)
    elif args.numbers:
        passwords = appendNumbers(password)
    else:
        passwords = basicSub(password)

    # save passwords to file
    if args.outputFile != None:
        writePasswordsToFile(args.outputFile, passwords)
    # copy passwords to clipboard
    else:
        checkPasswords(passwords)
"""
