import argparse
import sys


def authenticate():
    '''
    Call the "Authentcation" service
    '''
    pass


def scan():
    '''
    Call the "Scan" service
    '''
    pass


def scan_result():
    '''
    Call the "Old scan result" service
    '''
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Automate the recon phase for a penetration test.')
    parser.add_argument('--auth', required=False, action='store_true', help='Authenticate to the authentication service.')
    parser.add_argument('--scan', required=False, action='store_true', help='Start the scan on a given domain.')
    parser.add_argument('--results', required=False, action='store_true', help='View the results of previous scans.')
    args = parser.parse_args()

    if args.auth:
        authenticate()
    elif args.scan:
        scan()
    elif args.results:
        scan_result()
    else:
        parser.print_help(sys.stderr)

