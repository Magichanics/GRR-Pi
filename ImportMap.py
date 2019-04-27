'''
Jan Garong
April 27th, 2019
'''
import os

# this should be the network drive
def get_smb_map(ip_address, user, password, volume_name='volume(sda1)'):

    try:

        # mount volume (MacOS)
        os.system("osascript -e 'mount volume \"smb://" + ip_address + "/"+ volume_name +"/\" \
        as user name \"" + user + "\" with password \"" + password + "\"'")

        # read map and return 2d grid
        grid = []
        with open('/Volumes/volume(sda1)/GRR/data/map2d.txt', 'r') as f:
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

        # dismount volume
        os.system("osascript -e 'unmount volume \"smb://" + ip_address + "/" + volume_name + "/\"")
        return grid

    except:

        print('failed to connect to network')
        return [['R']]

if __name__ == '__main__':

    # get input
    ip_address = input('Write the IP Address.')
    user = input('Write the username.')
    password = input('Write the password.')

    # produce 2dmap from mounted volume
    grid = get_smb_map(ip_address, user, password)

    # display grid
    for i in range(len(grid)):
        print(grid[i])