# ui.py
# Chloe Fabro
# xfabro@uci.edu
# 85968044


from pathlib import Path
from Profile import Post, Profile, DsuFileError, DsuProfileError
import time

# Global variable to store the path to the DSU file
global_path = None


def output_path(path, file, search, extension):
    if file and path.is_dir():
        return False
    if search and search not in path.name:
        return False
    if extension and not path.name.endswith('.' + extension):
        return False
    return True


def list_content(currentPath, recursive, file, search, extension):
    for entry in sorted(currentPath.iterdir(), key=lambda e: (e.is_file(), e.name)):
        if recursive and entry.is_dir():
            list_content(entry, recursive, file, search, extension)
        elif output_path(entry, file, search, extension):
            print(entry)


def list_directory(path, recursive=False, file=False, search=None, extension=None):
    list_content(Path(path), recursive, file, search, extension)


def delete_file(file_path):
    if file_path.suffix != '.dsu':
        print("ERROR")
        return
    file_path.unlink()
    print(f"{file_path} DELETED")


def read_file(file_path):
    if file_path.suffix != '.dsu':
        print("ERROR")
        return
    if file_path.stat().st_size == 0:
        print("EMPTY")
        return
    with file_path.open('r') as file:
        print(file.read())


def create_file(directory, name):
    global global_path
        # Create new file with .dsu extension
    try:
        file_path = Path(directory) / f"{name}.dsu"
        if file_path.exists():
            # raise FileExistsError(f"The file {name}.dsu already exists.Please enter a unique file name!")
            print(f"The file {name}.dsu already exists, loading file instead.")
            return open_dsu_file(str(file_path))
        else:    
            username = input("Enter username: ").strip()
            if not username:
                raise Exception("Username cannot be empty.")
            password = input("Enter password: ").strip()
            if not password:
                 raise Exception("Passwor cannot be empty.")
            bio = input("Enter bio: ")
            if not bio:
                 raise Exception("Bio cannot be empty.")
            file_path.touch()
            profile = Profile(username=username, password=password, bio=bio)
            profile.save_profile(str(file_path))
            global_path = str(file_path)  # Update the global path
            print(f"Profile saved to {file_path}")
        return profile
    except Exception as e:
        print(f"Error: {e}")
        # profile = None ###
        return None
        

def open_dsu_file(file_path):
    global global_path
    profile = Profile()
    global_path = file_path ###
    try:
        profile.load_profile(file_path)
        global_path = file_path  # Update the global path
        print(f"Profile loaded successfully from {file_path}.")
        print(f"Username: {profile.username}, Password: {profile.password}, Bio: {profile.bio}")
    except DsuFileError as e:
        print(f"Error loading DSU file: {e}")
        profile = None 
    except DsuProfileError as e:
        print(f"Error processing DSU file content: {e}")
        profile = None 
    except Exception as e:
        print(f"Unexpected error: {e}")
        profile = None 
    return profile
        

def edit_file(profile, operate, value):
    if operate == '-usr' and  value:
        profile.username = value  # Directly set the new username
        print(f"Username updated to {profile.username}")
    elif operate == '-pwd' and value:
        profile.password = value  # Directly set the new password
        print(f"Password updated to {profile.password}")
    elif operate == '-bio' and value:
        
        profile.bio = value
        print(f"Bio has updated to {profile.bio}")  
                      
    elif operate == "-addpost":
        new_post = Post(entry=value)
        profile.add_post(new_post)     
        print(f'Post has been updated to {global_path}')      
    elif operate == "-delpost":
        print("tesing delete feature....")
        post_id = int(value) - 1 # index start at  0
        if profile.del_post(post_id):
            print(f'Post ID {post_id + 1} has been deleted.')
        else:
            print("Invalid post ID.")
    else:
        print("Invalid operation.")
    profile.save_profile(global_path)
    

def print_file(profile, operate, value):
    if operate == '-usr':
        print(f'Username: {profile.username}')
    elif operate == "-pwd":
        print(f'Password: {profile.password}')
    elif operate == "-bio":
        print(f"Bio :{profile.bio}")
    elif operate == '-posts':
        content = profile.get_posts()
        print("Here are your post: ")
        if content:
            for i, post in enumerate(content):
                entry = post.entry
                timestamp = post.timestamp
                print(f'Post ID {i+1}: {entry} at {time.ctime(timestamp)}')
    elif operate == "-post":
        post_id = int(value) - 1 # index start at  0
        content = profile.get_posts()
        post = content[post_id]
        entry = post.get_entry()
        timestamp = post.get_time()
        for i, post in enumerate(content):
            if i == post_id:
                print(f'Post ID {i+1}: {entry} at {time.ctime(timestamp)}')
    elif operate == '-all':
        print(f'Username: {profile.username}')
        print(f'Password: {profile.password}')
        print(f'Bio: {profile.bio}')       
        content = profile.get_posts()
        if content:
            for i, post in enumerate(content):
                entry = post.entry
                timestamp = post.timestamp                                  
                print(f'Post ID {i+1}: {entry} at {time.ctime(timestamp)}')
        else: 
            print("No content avaliable")
  

def parse_command(user_input):
    parts = user_input.split()
    if not parts:
        return "", []
    command = parts[0]
    options = parts[1:]
    return command, [option.strip('\"\'') for option in options]


##################################################################
"""

Bleow code will handle User-friendly interface and admin mode

"""



def list_directory_flow():
    path = input("Enter the directory path to list: ")
    recursive = input("Do you want to list contents recursively? (yes/no): ").lower() == 'yes'
    file_only = input("Should we list files only? (yes/no): ").lower() == 'yes'
    search = input("Enter search term for filenames (leave blank for no search): ").strip() or None
    extension = input("List files with what extension? (leave blank for no filter): ").strip() or None
    list_directory(path, recursive, file_only, search, extension)


def delete_file_flow():
    file_path = input("Enter the full path of the file you wish to delete: ")
    confirm = input(f"Are you sure you want to delete {file_path}? This cannot be undone. (yes/no): ").lower()
    if confirm == 'yes':
        delete_file(Path(file_path))
    else:
        print("File deletion cancelled.")


def read_file_flow():
    file_path = input("Enter the full path of the file you wish to read: ")
    read_file(Path(file_path))


def open_dsu_file_flow():
    file_path = input("Enter the path to the DSU file: ")
    profile = open_dsu_file(file_path)  # Assuming this returns a profile object or None
    if profile:
        print("Profile loaded successfully.")
    else:
        print("Failed to load profile.")
    return profile


def create_file_flow():
    directory = input("\nEnter the directory path for the new DSU file: ")
    name = input("Enter the name for the DSU file: ")
    create_file(directory, name)


def load_file_flow():
    file_path = input("Enter the path to the DSU file: ")
    open_dsu_file(file_path)


def edit_profile_flow(profile):
    while True:
        print("\nEdit Profile Options:")
        print("1. Change Username")
        print("2. Change Password")
        print("3. Update Bio")
        print("4. Add Post")
        print("5. Delete Post")
        print("B. Back")
        choice = input("Choose an option: ").lower()

        if choice == '1':
            new_username = input("Enter the new username: ")
            edit_file(profile, '-usr', new_username)
        elif choice == '2':
            new_password = input("Enter the new password: ")
            edit_file(profile, '-pwd', new_password)
        elif choice == '3':
            new_bio = input("Enter the new bio: ")
            edit_file(profile, '-bio', new_bio)
        elif choice == '4':
            new_post_content = input("Enter the content of the new post: ")
            edit_file(profile, '-addpost', new_post_content)
        elif choice == '5':
            post_id_to_delete = input("Enter the post ID to delete: ")
            edit_file(profile, '-delpost', post_id_to_delete)
        elif choice == 'b':
            break
        else:
            print("Invalid choice. Please try again.")


def print_profile_flow(profile):
    while True:
        print("\nPrint Profile Options:")
        print("1. Print Username")
        print("2. Print Password")
        print("3. Print Bio")
        print("4. Print All Posts")
        print("5. Print Specific Post by ID")
        print("6. Print All Profile Information")
        print("B. Back")
        choice = input("Choose an option: ").lower()


        if choice == '1':
            print_file(profile, '-usr', '')
        elif choice == '2':
            print_file(profile, '-pwd', '')
        elif choice == '3':
            print_file(profile, '-bio', '')
        elif choice == '4':
            print_file(profile, '-posts', '')
        elif choice == '5':
            post_id_to_print = input("Enter the post ID to print: ")
            print_file(profile, '-post', post_id_to_print)
        elif choice == '6':
            print_file(profile, '-all', '')
        elif choice == 'b':
            break
        else:
            print("Invalid choice. Please try again.")



def admin_mode(profile):
    global global_path

    print("Admin mode activated. Type 'exit' to leave admin mode.")
    while True:
        command_line = input()
        if command_line.lower() == 'exit':
            break
        parts = command_line.split()
        command = parts[0]
        options = parts[1:]      
        handle_admin_command(command, options)


def handle_admin_command(command, options):

    while True:
        user_input = input()
        command, options = parse_command(user_input)

        try:
            if command == 'Q':
                break
            
            elif command == 'D':
                path = options[0]
                delete_file(Path(path))
            elif command == 'R':
                path = options[0]
                read_file(Path(path))
            elif command == 'L':
                path = options[0] if options else None
                recursive = '-r' in options
                file = '-f' in options
                search = options[options.index('-s') + 1] if '-s' in options else None
                extension = options[options.index('-e') + 1] if '-e' in options else None
                if path is None:
                    print("Please enter the path for 'L' command")
                else:
                    list_directory(path, recursive, file, search, extension)
            elif command == 'C':
                if '-n' in options:
                    name_index = options.index('-n') + 1
                    directory = Path.cwd()  # Current directory, change if needed
                    name = options[name_index] if name_index < len(options) else None
                    create_file(directory, name)
                else:
                    print("Please specify a file name with -n flag.")
            elif command == "O":
                if options:
                    file_path = options[0]
                    open_dsu_file(file_path)
                else:
                    print("No file path provided to open.")   
            elif command == 'E':
                if  global_path:
                    profile = Profile()
                    profile.load_profile(global_path)
                    operate = options[0]
                    value = ' '.join(options[1:])  # Joining all remaining options as the value, assuming space-delimited input 
                    edit_file(profile, operate, value)
            elif command == "P":
                if global_path:
                    profile = Profile()
                    profile.load_profile(global_path)                 
                    operate = options[0]
                    value = ' '.join(options[1:]) 
                    print_file(profile, operate, value)              
        except Exception as e:
            print(f"ERROR: {e}")


def menu(current_profile):
    current_profile = None
    while True:
        print("\nWelcome to the DSU file manager.")
        print("1. Create a DSU file")
        print("2. Load a DSU file")
        print("3. List directory contents")
        print("4. Delete a file")
        print("5. Read a file")
        print("6. Edit a file")
        print("7. Print a file")
        print("Q. Quit")
        choice = input("Please choose an option or 'admin' to enter admin mode: ").lower()

        if choice == '1':
            current_profile= create_file_flow()
        elif choice == '2':           
            current_profile = open_dsu_file_flow()       
        elif choice == '3':
            list_directory_flow()
        elif choice == '4':
            delete_file_flow()
        elif choice == '5':
            read_file_flow()
        elif choice == '6':
            if current_profile:
                edit_profile_flow(current_profile)
            else:
                print("No profile is loaded.")           
        elif choice == '7':
            if current_profile:           
                print_profile_flow(current_profile)
            else:
                print('No profile is loaded for listing')
        elif choice == 'q':
            print("Exiting program.")
            break
        elif choice == 'admin':
            admin_mode(current_profile)       
        else:
            print("Invalid option, please try again.")