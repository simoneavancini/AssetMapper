#!/usr/bin/env python3

import argparse
import sys
import requests
from getpass import getpass
import json


AUTH_SERVICE = 'http://127.0.0.1:8080/authentication/'
SCAN_SERVICE = 'http://127.0.0.1:8080/scan/'
SCAN_STORAGE_SERVICE = 'http://127.0.0.1:8080/scan_storage/'


def auth_header():
    try:
        with open('.token.txt', 'r') as f:
            token = f.read()
    except FileNotFoundError:
        print('You need to authenticate first', file=sys.stderr)
        exit(1)

    return { 'Authorization': 'Bearer ' + token }


def register():
    '''
    Call the "Authentcation" service to register a new account
    '''
    data = {
        'email': input('Email: '),
        'username': input('Username: '),
        'password': getpass()
    }
    response = requests.post(f'{AUTH_SERVICE}/register', json=data)

    if response.status_code == 200:
        print('Registration successful')
    else:
        print(data.text)


def authenticate():
    '''
    Call the "Authentcation" service
    '''
    data = {
        'username': input('Username: '),
        'password': getpass()
    }

    response = requests.post(f'{AUTH_SERVICE}/login', json=data)

    if response.status_code == 200 and 'application/json' in response.headers['Content-type']:
        data = response.json()
        print(data['message'])
        token = data['token']
        with open('.token.txt', 'wb') as f:
            f.write(token.encode())
    else:
        print(response.text)


def scan():
    '''
    Call the "Scan" service
    '''
    # Scan service
    response = requests.get(f'{SCAN_SERVICE}/host', params={'domain': input('Domain: ')}, headers=auth_header())

    if response.status_code != 200:
        print(response.text)
        return

    data = response.json()
    print('Scan completed')

    # Store the results with the scan_storage service
    response = requests.post(f'{SCAN_STORAGE_SERVICE}/scans', json=data, headers=auth_header())

    if response.status_code != 200:
        print(response.text)
        return

    data = response.json()
    print('Scan data stored successfully. ID: ' + data['id'])


def scan_ls():
    '''
    Call the "Old scan result" service
    '''
    response = requests.get(f'{SCAN_STORAGE_SERVICE}/scans', headers=auth_header())

    if response.status_code != 200:
        print(response.text)
        return

    for i, scan in enumerate(response.json()):
        print(f'{i+1}. {scan["domain"]}\n    ID: {scan["_id"]}\n    Date: {scan["createdAt"]}')


def scan_info():
    '''
    Call the "Old scan result" service
    '''
    response = requests.get(f'{SCAN_STORAGE_SERVICE}/scans/{input("ID: ")}', headers=auth_header())

    if response.status_code != 200:
        print(response.text)
        return

    # print(json.dumps(response.json(), indent=4))
    print_object_summary(response.json())


def print_object_summary(obj: dict):
    doc = obj.get("doc", {})

    print(f"\n📄 Domain: {doc.get('domain')}")
    print(f"🆔 ID: {doc.get('_id')}")
    print(f"🕒 Created: {doc.get('createdAt')}")
    print(f"🕒 Updated: {doc.get('updatedAt')}")

    print("\n🌐 Attack Surface:")
    for d in doc.get("attack_surface", {}).get("domains", []):
        print(f"  - Domain: {d['domain']}")
        print(f"    IPs: {', '.join(d['ips'])}")

    print("\n🖥️ IP Details:")
    for ip_entry in doc.get("attack_surface", {}).get("ips", []):
        print(f"  - {ip_entry['ip']} ({ip_entry['org']}) @ {ip_entry['loc']}")

    print("\n🔧 Technologies:")
    techs = doc.get("technologies", {}).get("technologies", {})
    for tech, val in techs.items():
        print(f"  - {tech}: {val}")

    print("\n👥 Employees:")
    for email in doc.get("employees", {}).get("emails", []):
        print(f"  - {email['value']} ({email['position']})")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Automate the recon phase for a penetration test.')
    parser.add_argument('--register', required=False, action='store_true', help='Register to the authentication service.')
    parser.add_argument('--auth', required=False, action='store_true', help='Authenticate to the authentication service.')
    parser.add_argument('--scan', required=False, action='store_true', help='Start the scan on a given domain.')
    parser.add_argument('--scan-ls', required=False, action='store_true', help='List previous scans.')
    parser.add_argument('--scan-info', required=False, action='store_true', help='List previous scans.')
    args = parser.parse_args()

    if args.register:
        register()
    elif args.auth:
        authenticate()
    elif args.scan:
        scan()
    elif args.scan_ls:
        scan_ls()
    elif args.scan_info:
        scan_info()
    else:
        parser.print_help(sys.stderr)

