from functions.get_files_info import get_files_info

def test():

    print(f'Result for "." directory: {get_files_info("calculator", ".")}')
    print(f'Result for "pkg" directory: {get_files_info("calculator", "pkg")}')
    print(f'Result for "/bin" directory: {get_files_info("calculator", "/bin")}')
    print(f'Result for "../" directory: {get_files_info("calculator", "../")}')

if __name__ == "__main__":
    test()