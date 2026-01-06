
import getpass
import poplib
from email import message_from_bytes

def fetch_and_parse_emails():
    server = 'pop.gmail.com'
    port = 995
    
    try:
        M = poplib.POP3_SSL(server, port)
        
        M.user("mytreyan197@gmail.com")

        M.pass_("tinku@197")
        
        numMessages = len(M.list()[1])
        print(f"Total messages: {numMessages}")
        
        for i in range(10):
            response, lines, octets = M.retr(i + 1)
            msg_data = b'\n'.join(lines)
            msg = message_from_bytes(msg_data)
            
            print(f"\nFrom: {msg['From']}")
            print(f"Subject: {msg['Subject']}")
            print(f"Date: {msg['Date']}")
        M.quit()
    
    except poplib.error_proto as e:
        print(f"POP3 error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_and_parse_emails()

