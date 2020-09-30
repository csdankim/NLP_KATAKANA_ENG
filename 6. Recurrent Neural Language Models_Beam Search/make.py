import sys

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.replace("<s>", "")
        line = line.replace("</s>", "")
        line = line.replace(" ", "")
        line = line.replace("_", " ")
        s = line.index("*")
        print(line[:s])
