

class System:
    os = "Unknown"
    arch = "Unknown"

    def __init__(self):
        from platform import system, machine
        self.os = system()
        self.arch = machine()
        if self.os == "Windows":
            if self.arch == "AMD64":
                self.arch = "x86_64"
            else:
                self.arch = "Unknown"

    def __repr__(self):
        return F"{self.os} {self.arch}"

