# By Jester

# Imports
import sys
import socket
import colorama
import errno

# Colors
red = colorama.Fore.LIGHTRED_EX
yellow = colorama.Fore.LIGHTYELLOW_EX
blue = colorama.Fore.LIGHTBLUE_EX
reset = colorama.Fore.RESET

# Dict with parameters for work software
main_software_work_parameters = {}


# Main soft banner "Vega"
soft_banner = fr'''                                            
       ,---.                                  
      /__./|   By {blue}Jester{reset}                               
 ,---.;  ; |            ,----._,.             
/___/ \  | |   ,---.   /   /  ' /   ,--.--.   
\   ;  \ ' |  /     \ |   :     |  /       \  
 \   \  \: | /    /  ||   | .\  . .--.  .-. | 
  ;   \  ' ..    ' / |.   ; ';  |  \__\/: . . 
   \   \   ''   ;   /|'   .   . |  ," .--.; | 
    \   `  ;'   |  / | `---`-'| | /  /  ,.  | 
     :   \ ||   :    | .'__/\_: |;  :   .'   \
      '---"  \   \  /  |   :    :|  ,     .-./
              `----'    \   \  /  `--`---'    
                         `--`-'               
'''

# Help text
soft_help = rf'''Use {yellow}-p{reset} to specify one port, which you wanna scan
Use {yellow}-P{reset} to specify ports range
Use {yellow}-i{reset} to specify ip address
Use {yellow}-t{reset} to specify timeout for connect to host
Use {yellow}-f{reset} to specify path to file.txt with ports, that you wanna scan,
(the ports in the file should be written as each new port from a new line)

Use {yellow}one{reset} argument {yellow}-h{reset} for get help
Use {yellow}one{reset} argument {yellow}-s{reset} to see developer

{blue}Exemple -h and -s{reset}:
python main.py {yellow}-h{reset}
{yellow}Description{reset}: if you wanna get help

python main.py {yellow}-s{reset}
{yellow}Description{reset}: if you wanna see developer


{blue}Exemple usage{reset}:
python main.py {yellow}-i{reset} 125.255.1.34 {yellow}-p{reset} 135
{yellow}Description{reset}: if you wanna check: is open port {yellow}135{reset} at address {yellow}125.255.1.34{reset}

python main.py {yellow}-i{reset} 125.255.1.34 {yellow}-P{reset} 0 1025
{yellow}Description{reset}: if you wanna check ports from {yellow}0{reset} to {yellow}1025{reset} at the address {yellow}125.255.1.34{reset}

python main.py {yellow}-i{reset} 125.255.1.34 {yellow}-f{reset} c:\\User\\Jester\ports.txt
{yellow}Description{reset}: if you wanna check: is open every port from {yellow}c:\\User\\Jester\ports.txt{reset}  at the address {yellow}125.255.1.34{reset}
'''


# Print error in screen
def print_error(error_text: str):
    print(soft_banner)
    print(f'{red}Error -> {error_text}')


# Print data in screen
def print_data(text: str):
    print(soft_banner)
    print(text)


# Scan one port
def scan_one_port():
    soc = socket.socket()

    try:
        ip = str(main_software_work_parameters['ip_address'])
        port = int(main_software_work_parameters['port'])
    except ValueError:
        print(soft_banner)
        print(f'{red}You entered incorrectly port! {yellow}Exemple{reset}: {yellow}-p{reset} 135')
        quit()

    try:
        soc.connect((ip, port))
        if 'timeout' in main_software_work_parameters:
            try:
                soc.settimeout(int(main_software_work_parameters['timeout']))
            except ValueError:
                print(f'{red} You entered incorrect timeout!')
                quit()
        soc.close()
        print_data(f'[*] Port {yellow}{port}{reset} is open')
    except ConnectionRefusedError:
        print_data(f'[*] Port {red}{port}{reset} is close')
    except TimeoutError:
        print_error(f'Time out error, connection waiting exceeded!{reset}')
    except PermissionError:
        print_error(f'Permission error, The host did not give you the right to access it{reset}')
    except OSError as e:
        if e.errno == errno.EHOSTUNREACH:
            print_error(f'OS error, the host is unavailable, port may be close{reset}')
        elif e.errno == errno.ETIMEDOUT:
            print_error(f'OS error, connection waiting exceeded!{reset}')
        elif e.errno == errno.ECONNREFUSED:
            print_error(f'OS error, connection refused, port may be close{reset}')
        elif e.errno == errno.EADDRINUSE:
            print_error(f'OS error, the host is already in use!{reset}')
        elif e.errno == errno.WSAEINVAL:
            print_error(f'OS error, this address is incorrect for its context!{reset}')
        elif e.errno == 10049:
            print_error(f'OS error 10049, this address is incorrect for its context!{reset}')
        elif e.errno == 11001:
            print_error(f'Value error, ip address or port may be incorrect!{reset}')
        else:
            print_error(f'WinError: {e.errno}{reset}')
    except ValueError:
        print_error(f'Value error, ip or port may be incorrect!{reset}')
    except NameError:
        print_error(f'Value error, ip or port may be incorrect!{reset}')
    except OverflowError:
        print_error(f'Port error, port must be 0-65535!{reset}')


# Scan port range
def scan_port_range():
    print(soft_banner)

    try:
        a = int(main_software_work_parameters['range_ports'][0])
        b = int(main_software_work_parameters['range_ports'][1])
        ip = str(main_software_work_parameters['ip_address'])

        for port in range(a, b):
            try:
                soc = socket.socket()
                soc.connect((ip, port))
                if 'timeout' in main_software_work_parameters:
                    try:
                        soc.settimeout(int(main_software_work_parameters['timeout']))
                    except ValueError:
                        print(f'{red} You entered incorrect timeout!')
                        break
                soc.close()
                print(f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {yellow}is open{reset}')
            except ConnectionRefusedError:
                print(f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}is close{reset}')
            except TimeoutError:
                print(
                    f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}Time out error, connection waiting exceeded!{reset}')
            except PermissionError:
                print(
                    f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}Permission error, The host did not give you the right to access it{reset}')
            except OSError as e:
                if e.errno == errno.EHOSTUNREACH:
                    print(
                        f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}OS error, the host is unavailable, port may be close{reset}')
                elif e.errno == errno.ETIMEDOUT:
                    print(
                        f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}OS error, connection waiting exceeded!{reset}')
                elif e.errno == errno.ECONNREFUSED:
                    print(
                        f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}OS error, connection refused, port may be close{reset}')
                elif e.errno == errno.EADDRINUSE:
                    print(
                        f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}OS error, the host is already in use!{reset}')
                elif e.errno == errno.WSAEINVAL:
                    print(
                        f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}OS error, this address is incorrect for its context!{reset}')
                elif e.errno == 10049:
                    print(
                        f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}OS error 10049, this address is incorrect for its context!{reset}')
                elif e.errno == 11001:
                    print(
                        f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}Value error, ip address or port may be incorrect!{reset}')
                elif e.errno == 10038:
                    print(
                        f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}OS error, connection waiting exceeded!{reset}')
                else:
                    print(f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}WinError: {e.errno}{reset}')
            except ValueError:
                print(
                    f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}Value error, ip or port may be incorrect!{reset}')
            except NameError:
                print(
                    f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}Value error, ip or port may be incorrect!{reset}')
            except OverflowError:
                print(
                    f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}Port error, port must be 0-65535!{reset}')
    except ValueError:
        print(f'{red}You entered incorrect port range! {yellow}Exemple{reset}: {yellow}-P{reset} 0 1025')


# Scan ports in file
def scan_ports_in_file():
    print(soft_banner)

    # Delete ' and "
    path = ''
    ip = main_software_work_parameters['ip_address']

    for o in str(main_software_work_parameters['path_to_file']):
        if o not in('"', "'"):
            path += str(o)

    if not path.endswith('.txt'):
        print_error('This software can read only .txt files!')
        quit()

    try:
        with open(path, 'r', encoding='utf-8') as file:
            for port in file:
                port = int(port)
                try:
                    soc = socket.socket()
                    soc.connect((str(ip), port))
                    if 'timeout' in main_software_work_parameters:
                        try:
                            soc.settimeout(int(main_software_work_parameters['timeout']))
                        except ValueError:
                            print(f'{red} You entered incorrect timeout!')
                            break
                    soc.close()
                    print(f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {yellow}is open{reset}')
                except ConnectionRefusedError:
                    print(f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}is close{reset}')
                except TimeoutError:
                    print(
                        f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}Time out error, connection waiting exceeded!{reset}')
                except PermissionError:
                    print(
                        f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}Permission error, The host did not give you the right to access it{reset}')
                except OSError as e:
                    if e.errno == errno.EHOSTUNREACH:
                        print(
                            f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}OS error, the host is unavailable, port may be close{reset}')
                    elif e.errno == errno.ETIMEDOUT:
                        print(
                            f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}OS error, connection waiting exceeded!{reset}')
                    elif e.errno == errno.ECONNREFUSED:
                        print(
                            f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}OS error, connection refused, port may be close{reset}')
                    elif e.errno == errno.EADDRINUSE:
                        print(
                            f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}OS error, the host is already in use!{reset}')
                    elif e.errno == errno.WSAEINVAL:
                        print(
                            f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}OS error, this address is incorrect for its context!{reset}')
                    elif e.errno == 10049:
                        print(
                            f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}OS error 10049, this address is incorrect for its context!{reset}')
                    elif e.errno == 11001:
                        print(
                            f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}Value error, ip address or port may be incorrect!{reset}')
                    elif e.errno == 10038:
                        print(
                            f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}OS error, connection waiting exceeded!{reset}')
                    else:
                        print(f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}WinError: {e.errno}{reset}')
                except ValueError:
                    print(
                        f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}Value error, ip or port may be incorrect!{reset}')
                except NameError:
                    print(
                        f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}Value error, ip or port may be incorrect!{reset}')
                except OverflowError:
                    print(
                        f'[*] Trying connect to {ip}:{yellow}{port}{reset} -> {red}Port error, port must be 0-65535!{reset}')
    except FileNotFoundError:
        print(f'{red}File {path} not found!{reset}')
    except OSError:
        print(f'{red}File {path} is not txt!{reset}')


# Main function
def main():
    if 'port' in main_software_work_parameters:
        scan_one_port()
    elif 'range_ports' in main_software_work_parameters:
        scan_port_range()
    elif 'path_to_file' in main_software_work_parameters:
        scan_ports_in_file()


# Start software
if __name__ == '__main__':
    # Get all arguments
    sys_args = sys.argv
    sys_args.pop(0)

    # Check error
    if len(sys_args) == 0:
        print_error(f'You did not enter any arguments!{reset}\n'
                    f'Use {yellow}"-h"{reset} to help')
        quit()

    # Print help
    if sys_args[0] == '-h':
        print(soft_banner)
        print(soft_help)
        quit()
    elif sys_args[0] == '-s':
        print(soft_banner)
        print(f'{blue}Telegram{reset}: {yellow}https://t.me/Alternativa_all{reset}')


    # Get and set parameters in dict main_software_work_parameters
    for i in sys_args:
        if i == '-p':   main_software_work_parameters['port'] = sys_args[sys_args.index(i)+1]
        elif i == '-P': main_software_work_parameters['range_ports'] = (sys_args[sys_args.index(i)+1], sys_args[sys_args.index(i)+2])
        elif i == '-i': main_software_work_parameters['ip_address'] = sys_args[sys_args.index(i)+1]
        elif i == '-f': main_software_work_parameters['path_to_file'] = sys_args[sys_args.index(i)+1]
        elif i == '-t': main_software_work_parameters['timeout'] = sys_args[sys_args.index(i)+1]

    # Check errors
    if ('-p' or '-P' or '-f') in sys_args and '-i' not in sys_args:
        print_error(f'You entered ports, but you did not enter ip address!{reset}\n'
                    f'Use {yellow}-h{reset} to help')
        quit()
    elif ('-p' or '-P' or '-f') not in sys_args and 'i' in sys_args:
        print_error(f'You entered ip address, but you did not enter port, ports range or file with ports!{reset}\n'
                    f'Use {yellow}-h{reset} to help')
        quit()
    main()
