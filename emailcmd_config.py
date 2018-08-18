"""emaailcmd_config.py
File with configuration information for emailcmd.py
"""
############
# ACCOUNTS #
############
radr = 'bob@example.com' # address to check and send from
imapserver = 'imap.example.com'# imap server for account
smtpserver = 'smtp.example.com'# smtp server for account
smtpserverport = 587 # smtp server port for starttls
pwd = b'bXlwYXNz' # password for account encoded with base64.b64encode
sadr = 'alice@example.com' # address to receive commands from

##########
# PARAMS #
##########
check_freq = 5 # Frequency to check for emails in sec
timeout = 20 # Default timeout for commands in sec

############
# COMMANDS #
############

# To add a command, define the function here and add it to the
#    dictionary commands at the bottom.  Key is command name and
#    value is the fuction object.  
# Function must have an argument for an array that is the message
#    split by lines and return text to be emailed back, including
#    any error messages.  
# The first line is always the command so it cannot be a paramater.
# The message:
#times two
#
#32
# Would become []

# Example:
# def times_two(lines):
#     return lines[2] * 2
# commands = {"times two" : times_two}

import subprocess as sub
def exec_cmd(cmds):
    param = cmds[2]
    """exec_cmd: executes a command with subprocess
    """
    print("name is exec cmd")
    try:
        p = sub.run(param, shell=True, timeout=20, stdout=sub.PIPE, stderr=sub.PIPE)
    except sub.TimeoutExpired:
        return "Command timed out.  "
    return '''Command exited with code %s
Stdout:
%s
Stderr:
%s
''' % (p.returncode, p.stdout.decode(), p.stderr.decode())

def runscript(lines):
    """
    Writes input to disk and executes it.  Returns any errors.
    IMPORTANT:
    Before running, make sure file 'script' exists and is executable.
    """
    try:
        f = open("script", "w")
        count = 0
        for i in lines:
            if count is 0 or i is 1:
                count = count + 1
                continue
            f.write(i + "\n")
            count = count + 1
        f.close()
        p = sub.run("./script", shell=True, timeout=timeout, stdout=sub.PIPE, stderr=sub.PIPE)
        r = """Script finished!
Return code: %s
Stdout:
%s
Stderr:
%s
""" % (p.returncode, p.stdout.decode(), p.stderr.decode())
    except Exception as e:
        return "Error: \n" + str(e)
    return r


#################
# COMMANDS DICT #
#################
commands = {"exec cmd" : exec_cmd, "runscript" : runscript}
