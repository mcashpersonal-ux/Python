# paramiko — SSH and SFTP automation

> paramiko implements the SSH2 protocol in pure Python — run remote
> commands, transfer files over SFTP, and script server automation without
> shelling out to the `ssh` binary.

## Install and connect

```bash
python -m pip install paramiko
```

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.RejectPolicy())
client.load_system_host_keys()
client.connect("host.example.com", username="deploy", key_filename="/home/user/.ssh/id_ed25519")
```

`RejectPolicy` (the default-safe choice) refuses to connect to a host whose
key is not already known — it is what prevents a silent
man-in-the-middle. Never use `AutoAddPolicy` outside a throwaway lab
environment; it accepts any host key without verification.

## run a remote command

```python
stdin, stdout, stderr = client.exec_command("uptime")
print(stdout.read().decode())
print(stderr.read().decode())
exit_status = stdout.channel.recv_exit_status()
client.close()
```

Always read `exit_status` before trusting the command succeeded —
`exec_command` does not raise on a non-zero exit code by itself.

## transfer files with SFTP

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.RejectPolicy())
client.load_system_host_keys()
client.connect("host.example.com", username="deploy", key_filename="/home/user/.ssh/id_ed25519")

with client.open_sftp() as sftp:
    sftp.put("local_report.csv", "/var/data/report.csv")
    sftp.get("/var/log/app.log", "app.log")

client.close()
```

SFTP runs over the same authenticated SSH connection — no separate port
or credentials needed.

## use a context manager and connection pooling for many hosts

```python
import paramiko

def run(host, command):
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        client.load_system_host_keys()
        client.connect(host, username="deploy", key_filename="/home/user/.ssh/id_ed25519", timeout=10)
        _, stdout, _ = client.exec_command(command)
        return stdout.read().decode()

for host in ("web1.example.com", "web2.example.com"):
    print(host, run(host, "systemctl is-active nginx"))
```

Always pass `timeout=` — an unreachable host otherwise hangs the call
indefinitely. For fleets larger than a handful of hosts, consider a proper
orchestration tool (Ansible, Fabric) built on top of this same primitive.

## Credential safety

Prefer key-based auth over passwords, keep private keys out of version
control and readable only by their owner (`chmod 600`), and use an
SSH agent or `key_filename` rather than embedding a passphrase in code.

Next door: [python-can](041-python-can.md) and [pyserial](042-pyserial.md)
for talking to hardware over other transports, and [boto3](106-boto3.md)
for the cloud instances you might be SSHing into.
