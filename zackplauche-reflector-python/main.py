from reflector import Reflector
import activities

main_reflector = Reflector([
    activities.morning_reflection,
    activities.end_of_day_reflection,
    activities.weekly_reflection,
    activities.acclaim_system,
])

if __name__ == '__main__':
    main_reflector.run()