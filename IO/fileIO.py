import os
import csv

# used for opening and reading files
class FileIO:
    def openToRead(self, name):
        try:
            return open(name, "r")
        except:
            print("can't open ", name)

    def readFile(self, file):
        return file.readlines()

    def contentToString(self, file):
        string = ""
        for line in file:
            string += str(line)
        return string

    def writeToFile(self, text, fileName):
        try:
            file = open(fileName, "x")
            file.write(text)
            file.close()
            print("generated > ", fileName)
        except:
            os.remove(fileName)
            self.writeToFile(text, fileName)
    
    def readCSV(self, csvfile, delim):
        return csv.reader(csvfile, delimiter=delim)

    def writeRowToCSV(self,file, delim, list):
        with open(file, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=delim,
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(list)

    
if __name__ == "__main__":
   pass
