import paramiko
from concurrent.futures import ThreadPoolExecutor, as_completed

class SSHManager:
    def __init__(self, username, password=None, key_file=None):
        self.username = username
        self.password = password
        self.key_file = key_file

    def _connect(self, host):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if self.key_file:
                client.connect(host, username=self.username, key_filename=self.key_file)
            else:
                client.connect(host, username=self.username, password=self.password)
            return client
        except Exception as e:
            print(f"Connection failed to {host}: {e}")
            return None

    def execute_command(self, host, command):
        client = self._connect(host)
        if client:
            try:
                stdin, stdout, stderr = client.exec_command(command)
                output = stdout.read().decode()
                error = stderr.read().decode()
                return output if output else error
            finally:
                client.close()
        else:
            return None

    def upload_file(self, host, local_path, remote_path):
        client = self._connect(host)
        if client:
            try:
                sftp = client.open_sftp()
                sftp.put(local_path, remote_path)
                sftp.close()
                print(f"File uploaded to {host}:{remote_path}")
            except Exception as e:
                print(f"File upload failed to {host}: {e}")
            finally:
                client.close()

    def execute_parallel(self, hosts, command):
        results = {}
        with ThreadPoolExecutor() as executor:
            future_to_host = {executor.submit(self.execute_command, host, command): host for host in hosts}
            for future in as_completed(future_to_host):
                host = future_to_host[future]
                try:
                    results[host] = future.result()
                except Exception as e:
                    results[host] = f"Error: {e}"
        return results

