from functions.get_file_content import get_file_content

def test():
    result = get_file_content("calculator", "calculator.py")
    print(f"Length: {len(result)}")
    print(f"Last 100 chars: {result[-100:]}")
    
