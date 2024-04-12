def create_output_file(content, num_lines):
    with open("output.txt", "w") as file:

        for i in range(num_lines):
            file.write(content + "\n")


def main():
    content = input("Введите строку: ")
    num_lines = int(input("Введите число строк: "))

    create_output_file(content, num_lines)
    print("Файл output.txt успешно создан!")


if __name__ == "__main__":
    main()