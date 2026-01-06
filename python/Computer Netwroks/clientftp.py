import ftplib
import os

def connect_to_ftp_server(host, port, username, password):
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, port)
        ftp.login(username, password)
        return ftp
    except Exception as e:
        print(f"Error connecting to FTP server: {e}")
        return None

def list_files(ftp):
    try:
        files = ftp.nlst()
        print("Files in ftp_files directory:")
        for file in files:
            print(file)
    except Exception as e:
        print(f"Error listing files: {e}")

def download_file(ftp, filename):
    try:
        with open(filename, 'wb') as f:
            ftp.retrbinary(f"RETR {filename}", f.write)
        print(f"File {filename} downloaded successfully")
    except Exception as e:
        print(f"Error downloading file: {e}")

def upload_file(ftp, filename):
    try:
        with open(filename, 'rb') as f:
            ftp.storbinary(f"STOR {filename}", f)
        print(f"File {filename} uploaded successfully")
    except Exception as e:
        print(f"Error uploading file: {e}")

def delete_file(ftp, filename):
    try:
        ftp.delete(filename)
        print(f"File {filename} deleted successfully")
    except Exception as e:
        print(f"Error deleting file: {e}")

def update_file(ftp, filename):
    try:
        # Download the file to a temporary location
        temp_filename = f"{filename}.tmp"
        with open(temp_filename, 'wb') as f:
            ftp.retrbinary(f"RETR {filename}", f.write)

        # Append the user's input to the file
        user_input = input("Enter the text to append to the file: ")
        with open(temp_filename, 'a') as f:
            f.write(user_input + "\n")

        # Upload the updated file back to the FTP server
        with open(temp_filename, 'rb') as f:
            ftp.storbinary(f"STOR {filename}", f)

        # Remove the temporary file
        os.remove(temp_filename)

        print(f"File {filename} updated successfully")
    except Exception as e:
        print(f"Error updating file: {e}")

def display_file_content(ftp, filename):
    try:
        # Download the file to a temporary location
        temp_filename = f"{filename}.tmp"
        with open(temp_filename, 'wb') as f:
            ftp.retrbinary(f"RETR {filename}", f.write)

        # Read the file content
        with open(temp_filename, 'r') as f:
            content = f.read()
            print(content)

        # Remove the temporary file
        os.remove(temp_filename)
    except Exception as e:
        print(f"Error displaying file content: {e}")

def main():
    host = 'localhost'
    port = 8080
    username = 'user'
    password = 'password'

    ftp = connect_to_ftp_server(host, port, username, password)
    if ftp:
        while True:
            print("\nFTP Client Menu:")
            print("1. List files")
            print("2. Download file")
            print("3. Upload file")
            print("4. Delete file")
            print("5. Update file")
            print("6. Display file content")
            print("7. Quit")
            choice = input("Enter your choice: ")

            if choice == '1':
                list_files(ftp)
            elif choice == '2':
                filename = input("Enter the filename to download: ")
                download_file(ftp, filename)
            elif choice == '3':
                filename = input("Enter the filename to upload: ")
                upload_file(ftp, filename)
            elif choice == '4':
                filename = input("Enter the filename to delete: ")
                delete_file(ftp, filename)
            elif choice == '5':
                filename = input("Enter the filename to update: ")
                update_file(ftp, filename)
            elif choice == '6':
                filename = input("Enter the filename to display content: ")
                display_file_content(ftp, filename)
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please try again.")

        ftp.quit()

if __name__ == '__main__':
    main()