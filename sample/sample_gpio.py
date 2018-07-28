import RPi.GPIO as GPIO
import time


def main():
    GPIO.setmode(GPIO.BOARD)
    #Use PIN 7 (GPIO 4)
    GPIO.setup(7, GPIO.OUT)

    GPIO.output(7, True)
    time.sleep(1)
    GPIO.output(7, False)
    time.sleep(1)

    GPIO.cleanup()


if __name__ == "__main__":
    main()

