import base64
import paramiko
import argparse
import os.path


def conn_ssh(ip, username, ssh_pass, remote_cmd, passwd=None):
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ip, 22, username, ssh_pass)

    if passwd is not None:
        stdin, stdout, stderr = s.exec_command(remote_cmd)
        stdin.write(passwd + '\n')
        stdin.flush()

    else:
        stdin, stdout, stderr = s.exec_command(remote_cmd)

    print stdout.read()
    print stderr.read()
    s.close()


def chk_argv():
    pass


def main():

    parser = argparse.ArgumentParser(description='SSH Connect')
    parser = argparse.ArgumentParser()
    parser.add_argument('--gen', help='Generate password')
    args = parser.parse_args()

    if args.gen is not None:
        pwd64 =  base64.b64encode(args.gen)
        print("[+] You password encode: " + pwd64 + ")")
        exit(1)



    is_sudo_cmd = True
    serv_lst = "/tmp/serv.lst"  # File with IPs

    if is_sudo_cmd:
        sudo_remote_cmd = "sudo -S id"
        sudo_b64_password = base64.b64decode("Y2Rma2RxMWFsZmE=)")

    else:
        remote_cmd = "uptime"

    remote_user_ssh = "emelys3"
    ssh_b64_pass = base64.b64decode("Y2Rma2RxMWFsZmE=)")

    # Open IP file
    with open(serv_lst, "r") as f:
        text = f.readlines()

    # for-loop for IP list
    for lineHost in text:

        # Remove CRLF
        lineHost = lineHost.replace("\n", "")

        # Connect SSH
        print "[+] Connecting Addr::" + lineHost

        if is_sudo_cmd:
            conn_ssh(lineHost, remote_user_ssh, ssh_b64_pass, sudo_remote_cmd, sudo_b64_password)
        else:
            conn_ssh(lineHost, remote_user_ssh, ssh_b64_pass, remote_cmd)

        print "NOC Output Results"


main()
