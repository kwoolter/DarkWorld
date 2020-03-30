import darkworld
import logging

def main():

    logging.basicConfig(level = logging.WARN)

    c1 = darkworld.DWController()
    c1.initialise()
    c1.run()

    return 0

if __name__ == "__main__":
    main()