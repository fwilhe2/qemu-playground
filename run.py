#!/usr/bin/python

import subprocess
import argparse
import urllib.request
from urllib.parse import urlparse
import lzma
import os.path

virtual_machines = {
    'fedora': {
        'name':
        'Fedora 36',
        'location':
        'https://download.fedoraproject.org/pub/fedora/linux/releases/36/Cloud/x86_64/images/Fedora-Cloud-Base-36-1.5.x86_64.raw.xz',
        'arch':
        'x86_64',
        'digest':
        'abeb7eaafe6fcef788170d58cf4051bc833a130ab3886b78ec87915c41eae67e'
    },
    'alma': {
        'name':
        'Alma 9',
        'location':
        'http://repo.almalinux.org/almalinux/9.0/cloud/x86_64/images/AlmaLinux-9-GenericCloud-9.0-20220527.x86_64.qcow2',
        'arch':
        'x86_64',
        'digest':
        'e453dde3dac780c149932f39814e3371cb0b7fe3f758012b86ab6c7a51ec7a42'
    }
}


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

        with urllib.request.urlopen(image_location) as f:
            image_bytes = f.read()

            with open(disk_image, 'wb') as file:
                file.write(image_bytes)

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
    vm = virtual_machines[os_image]
    disk_image = download_image_if_required(vm)
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
