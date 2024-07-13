#!/usr/bin/python

import subprocess
import argparse
from urllib.parse import urlparse
import lzma
import os.path
import yaml
import platform

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def image_format(image):
    return image.split('.')[-1]


def image_name(url):
    return urlparse(url).path.split('/')[-1]


def download_image_if_required(vm):
    image_location = vm['location']
    print(image_location)

    disk_image = image_name(image_location)
    if image_location.endswith('xz'):
        disk_image = image_name(image_location)[:-3]

    if not os.path.exists(disk_image):

        # use wget because alma download fails with urllib (status forbidden, reason unclear)
        subprocess.run(['wget', image_location])

        if image_location.endswith('xz'):
            with lzma.open(disk_image) as f:
                image_bytes_uncompressed = f.read()

            disk_image = image_name(image_location)[:-3]
            with open(disk_image, 'wb') as file:
                file.write(image_bytes_uncompressed)
    return disk_image


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage qemu VMs.')
    parser.add_argument('image')
    args = parser.parse_args()

    os_image = args.image
    with open(f'{os_image}.yaml', 'r') as f:
        manifest = yaml.load(f, Loader=Loader)
        machine = platform.machine()
        vm = [image for image in manifest['images'] if image['arch'] == machine]
        print(vm)
        assert len(vm) == 1, f"expected one image for arch {machine}, got {len(vm)} images"
        disk_image = download_image_if_required(vm[0])
        print(disk_image)

        subprocess.run([
            '/usr/bin/qemu-system-x86_64', '-m', '4096', '-cpu', 'host',
            '-machine', 'q35,accel=kvm', '-smp', '4,sockets=1,cores=4,threads=1',
            '-drive',
            'if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE.fd',
            '-boot', 'order=c,splash-time=0,menu=on', '-drive',
            f'file={disk_image},format={image_format(disk_image)},if=virtio',
            '-device', 'virtio-rng-pci', '-net', 'nic', '-net',
            'user,hostfwd=tcp::2222-:22', '-device', 'virtio-vga', '-device',
            'virtio-keyboard-pci', '-device', 'virtio-mouse-pci', '-display',
            'sdl', '-cdrom', 'config/seed.iso'
        ])
