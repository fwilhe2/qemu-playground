#!/usr/bin/python

import subprocess

subprocess.run(['/usr/bin/qemu-system-x86_64', '-m', '4096', '-cpu', 'host', '-machine', 'q35,accel=kvm', '-smp', '4,sockets=1,cores=4,threads=1', '-drive', 'if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE.fd', '-boot', 'order=c,splash-time=0,menu=on', '-drive', 'file=Fedora-Cloud-Base-36-1.5.x86_64.raw,format=raw,if=virtio', '-device', 'virtio-rng-pci', '-net', 'nic', '-net', 'user', '-device', 'virtio-vga', '-device', 'virtio-keyboard-pci', '-device', 'virtio-mouse-pci', '-display', 'sdl', '-cdrom', 'config/seed.iso'])