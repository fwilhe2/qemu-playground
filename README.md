# qemu-playground
Scripts and notes on qemu virtual machines


## Build config iso image

```
make
```

## Start VM

```
./run.py [fedora/alma]
```

## Login

The default user name depends on the used os image.

```
ssh -p 2222 fedora@localhost
```

## References

[Lima: Linux virtual machines (on macOS, in most cases)](https://github.com/lima-vm/lima)

[How to SSH from host to guest using QEMU?](https://unix.stackexchange.com/a/196074)

