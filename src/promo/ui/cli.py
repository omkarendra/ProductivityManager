# src/promo/ui/cli.py

class CLI:

    def run(self):
        command = input("Promo > ").strip().lower()
        self.dispatch(command)

    def dispatch(self, command):
        match command:
            case "add":
                print("Add selected")

            case "list":
                print("List selected")

            case "delete":
                print("Delete selected")

            case _:
                print("Unknown command")
