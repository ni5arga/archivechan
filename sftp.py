import paramiko

def archive_sftp_dir(host, username, password, remote_dir, local_dir):
    transport = paramiko.Transport((host, 22))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    os.makedirs(local_dir, exist_ok=True)
    for item in sftp.listdir(remote_dir):
        remote_path = f"{remote_dir}/{item}"
        local_path = f"{local_dir}/{item}"
        sftp.get(remote_path, local_path)
    sftp.close()
