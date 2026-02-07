# MurDB

> Secure Database Export & Encrypted Backup Tool\
> AES-256 + RSA Hybrid Encryption for Database Dumps

------------------------------------------------------------------------

## Overview

MurDB is a security-focused database export tool designed to protect
backup files from data leaks.

Instead of storing raw database dumps (JSON / SQL / BSON), MurDB
encrypts backups using:

-   **AES-256 (symmetric encryption)** for the database dump
-   **RSA-2048 (asymmetric encryption)** to protect the AES key
-   A custom `.sq` secure container format

Even if a backup server is compromised, attackers cannot read the data
without the private key.

------------------------------------------------------------------------

## Why MurDB?

Real-world breaches often happen like this:

Company makes backups\
↓\
Backups stored in cloud / backup server\
↓\
Backup server compromised\
↓\
Backup files stolen\
↓\
If unencrypted → DATA BREACH

MurDB solves this by encrypting backups **before storage**.

------------------------------------------------------------------------

## Architecture

    DB Dump
       ↓
    AES-256 (random session key)
       ↓
    RSA (encrypt AES key using public.pem)
       ↓
    .sq Secure Container

-   The **server only needs the public key**
-   The **admin keeps the private key locally**
-   The container is useless without the private key

------------------------------------------------------------------------

## Roles in Security Scenario

### Administrator

-   Generates RSA keypair locally
-   Keeps `private.pem` secret
-   Uploads `public.pem` to server
-   Performs encrypted exports
-   Can decrypt `.sq` files

### Attacker

-   Gains access to backup storage
-   Steals `.sq` files
-   Cannot decrypt without `private.pem`

------------------------------------------------------------------------

## Features

-   MongoDB export
-   PostgreSQL export
-   SQLite export
-   Hybrid AES + RSA encryption
-   Secure container format
-   CLI interface
-   Docker-based server deployment
-   Windows installer support

------------------------------------------------------------------------
## Installation
``` bash
1. Download the file in the releases tab.
2. Run the installer.
3. After installing, make sure you've reopened all of your console tabs.
```



## Installation (Developer Mode)

``` bash
pip install -e .
```

------------------------------------------------------------------------

## Docker Setup

Start services:

``` bash
murdb up
```

Stop services:

``` bash
murdb down
```

------------------------------------------------------------------------

## Generate Keys (Admin Side)

``` bash
murdb keygen
```

Keys are stored in:

    C:\Users\<USER>\.MurDB\
        private.pem
        public.pem

Keep `private.pem` secret.

------------------------------------------------------------------------

## Export Database Example

``` bash
murdb export --type mongodb --db testmongo
```

Output:

    testmongo.sq

This file is encrypted and safe to store in cloud or backup storage.

------------------------------------------------------------------------

## Decrypt Backup

``` bash
murdb decrypt testmongo.sq
```

Requires `private.pem`.

------------------------------------------------------------------------

## Example Use Case (Demo Scenario)

1.  Attacker steals `.sq` file from server
2.  Attacker tries to open it → unreadable binary
3.  Admin runs `murdb decrypt`
4.  Data restored successfully

------------------------------------------------------------------------

## Project Structure

    app/              # Core server logic
    cli/              # CLI interface
    Dockerfile        # Container setup
    docker-compose.yml
    pyproject.toml
    requirements.txt

------------------------------------------------------------------------

## Security Model

-   No private keys stored on server
-   Encrypted backup format
-   Separation of roles (admin vs server)
-   Hybrid encryption model used in real-world systems

------------------------------------------------------------------------

## Roadmap

-   Cloud storage integration
-   Automated scheduled backups
-   Web dashboard
-   Multi-key support
-   Hardware key support (YubiKey)

------------------------------------------------------------------------

## License

MIT License

------------------------------------------------------------------------

## Author

femominal

Build date: 2026-02-07
