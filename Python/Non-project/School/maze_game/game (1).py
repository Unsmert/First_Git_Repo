test = ['test1, test2']
test_input = input()
match test_input:
    case "1":
        print(f"Testing1: {", ".join(test)}")
    case "2":
        print(f"Testing2: {", ".join(test)}")
    case _:
        print(f"Testing3: {", ".join(test)}")