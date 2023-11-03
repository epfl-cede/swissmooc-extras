# -*- coding: utf-8 -*-
from apps.split_logs.sms_command import SMSCommand
from apps.split_logs.utils import run_command
from django.conf import settings


class Command(SMSCommand):
    help = "Sync tracking logs files from swarm VMs to backup server"

    def handle(self, *args, **options):
        self.setOptions(**options)

        for swarm in settings.SWARMS:
            swarm_host = f"{settings.SMS_APP_ENV}-swarm-{swarm}"
            self._info(f"process {swarm_host=}")
            return_code, stdout, stderr = run_command([
                "ssh", "-o", "StrictHostKeyChecking=no",
                f"ubuntu@zh-{swarm_host}",
                "hostname",
            ])
            if return_code != 0:
                self._error(f"remote command {stderr=}")
                continue

            swarm_hostname = stdout
            for instance in settings.INSTANCES:
                self._info(f"process {instance=}")
                remote_dir = f"/backup/{settings.SMS_APP_ENV}/tracking-docker/{instance}/{swarm_hostname}/"
                return_code, stdout, stderr = run_command([
                    "ssh", "-o", "StrictHostKeyChecking=no",
                    f"ubuntu@{settings.BACKUP_SERVER}",
                    "mkdir", "-p",
                    remote_dir,
                ])
                if return_code != 0:
                    self._error(f"remote command {stderr=}")
                    continue

                return_code, stdout, stderr = run_command([
                    "ssh", f"ubuntu@zh-{swarm_host}",
                    "rsync", "--chmod=D755,F644", "-av",
                    "-e", "'ssh -o StrictHostKeyChecking=no'",
                    "--exclude=tracking.log",
                    "--ignore-missing-args",
                    f"/home/ubuntu/stacks/openedx-{instance}/logs/tracking/*.gz",
                    f"ubuntu@{settings.BACKUP_SERVER}" + ":" + remote_dir
                ])
                if return_code != 0:
                    self._error(f"remote command {stderr=}")
                    continue

            return_code, stdout, stderr = run_command([
                "ssh", f"ubuntu@zh-{swarm_host}",
                "find", "/home/ubuntu/stacks/openedx-*/logs/tracking/",
                "-mtime", "+30",
                "-type", "f",
                "-name", "\*.gz",
                "-delete"
            ])
            if return_code != 0:
                self._error(f"remote command {stderr=}")

        return_code, stdout, stderr = run_command([
            "ssh", f"ubuntu@{settings.BACKUP_SERVER}",
            "find", f"/backup/{settings.SMS_APP_ENV}/tracking-docker/",
            "-mtime", "1",
            "-type", "f"
        ])
        if return_code != 0:
            self._error(f"remote command {stderr=}")
        else:
            files = stdout.split("\n")
            result_message = []
            result_message.append(
                f"{len(files)} files were synced in last 24 hours:"
            )
            for _file in files:
                result_message.append(f" {_file}")
            result_message.append("")
            result_message.append("Detailed log:")

            self.message = result_message + self.message

        self.send_email("Sync tracking_logs")
