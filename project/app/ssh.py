import paramiko
import os

class RemoteConnect():
    def __init__(self,hostname,username,password,message):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.message = message
        self.client = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(self.hostname, 
                        username=self.username, 
                        password=self.password, 
                        timeout=30)
            print(f"Connect to {self.hostname} with user {self.username}")
            session_dict = {
                "username":self.username,
                "message": None,
                "client": self.client
            }
            # return self.username, self.password, self.message, self.client

        except Exception as e:
            self.message = str(e)
            session_dict = {
                "username":self.username,
                "message": self.message,
                "client": self.client
            }
        return session_dict
        
    def get_session(self):
        if self.client and self.client.get_transport() and self.client.get_transport().is_active():
            print("Session is active.")
            return self.client
        else:
            # Attempt reconnection if the session has become inactive
            print("Session inactive. Attempting to reconnect...")
            self.connect()  # Re-establish the SSH connection
            return self.client if self.client.get_transport().is_active() else None
        
    def upload(self, fullcimpath):
        if self.client:
            print("Trying to upload...")
            if self.client.get_transport() and self.client.get_transport().is_active():
                try:
                    sftp = self.client.open_sftp()
                    sftp.put(fullcimpath, f"/home/{self.username}/" + os.path.basename(fullcimpath))
                    print(f"File uploaded to SFTP server successfully")
                    return True
                except Exception as e:
                    print(f"Failed to upload cim file: {e}")
                    return False
        else:
            print("No active connection for file upload.")
            return False
    
    def close(self):
        if self.client and self.client.get_transport() and self.client.get_transport().is_active():
            try:
                self.client.close()
                print("Connection closed")
            except Exception as e:
                print(f"Error while closing connection: {e}")
            finally:
                self.client = None
        else:
            print("No connection to close.")