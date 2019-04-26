import os

def get_smb_map(ip_address, user, password, volume_name='volume(sda1)'):

    # mount volume (MacOS)
    os.system("osascript -e 'mount volume \"smb://" + ip_address + "/"+ volume_name +"/\" \
    as user name \"" + user + "\" with password \"" + password + "\"'")

    # read map and return 2d grid
    grid = []
    with open('/Volumes/volume(sda1)/GRR/data/logs.txt', 'r') as f:
        line = f.readline()
        while line != '':

            # clean string from \ns
            line = line.strip()

            # append each character
            row = []
            for i in range(len(line)):
                row.append(line[i])

            grid.append(row)

            # get next line
            line = f.readline()

    f.close()
    return grid
