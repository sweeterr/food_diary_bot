from datetime import datetime


class Record:
    def __init__(self, input_string: str, record_type: str):
        self.date = datetime.now().date().strftime("%d.%m.%Y")
        self.time = datetime.now().time().strftime("%H:%M")
        self.contents = ""
        self.comments = ""
        self.message = ""
        self.row = ""
        self.type = record_type
        self.__parse_input(input_string)

    def __parse_input(self, input_string: str):
        inputs = [i.strip() for i in input_string.split(";")]
        if len(inputs) < 1:
            self.message = "No input detected"
        elif len(inputs) > 4:
            self.message = "Too many delimiters"
        else:
            if len(inputs) == 1:
                self.contents = inputs[0]
            elif len(inputs) == 2:
                self.time, self.contents = inputs[0], inputs[1]
            elif len(inputs) == 3:
                self.date, self.time, self.contents = inputs[0], inputs[1], inputs[2]
            elif len(inputs) == 4:
                self.date, self.time, self.contents, self.comments = inputs[0], inputs[1], inputs[2], inputs[3]
            self.message = f"Date: {self.date}\n" \
                           f"Time: {self.time}\n" \
                           f"Contents: {self.contents}\n" \
                           f"Comments: {self.comments}\n"
            self.row = list(self.__dict__.values())[:4]


def main():
    record = Record("asca", "acasdfcwe")
    print(record.row)


if __name__ == "__main__":
    main()
