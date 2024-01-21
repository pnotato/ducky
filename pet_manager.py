import pet
import asyncio
import numpy as np
import Calendar.reminder as rem
import WebScraper.webscraper as ws
import time

class PetManager:
    def __init__(self):
        self.pet = pet.Pet()
        self.i = 0
        self.reminder = rem.Reminders()
        self.reminders = self.reminder.read_events(10)

    async def update(self):
        if self.i % 100 == 0:
            self.roam()
        elif self.i % 10110 == 0:
            self.pet.idle()
            self.compliment()
        elif self.i % 203 == 0:
            self.pet.idle()
            self.volunteer()
        elif self.i % 1000036 == 0:
            self.pet.say("Remember to take a break! You've been working for a while now!")
        self.pet.update()
        self.remind()
        await asyncio.sleep(0.001)
        self.i = self.i + 1

    def roam(self):
        # makes the pet randomly roam/idle across the screen

        # randomly choose whether to roam or idle
        if not self.pet.isDragged and not self.pet.isTalking:
            roam = np.random.choice([True, False])

            if roam:
                # randomly choose a direction
                direction = np.random.choice([-1, 1])

                # randomly choose a speed
                speed = np.random.randint(1, 5)

                # set the pet's velocity
                self.pet.set_velocity([direction * speed, self.pet.velocity[1]])

                # set the pet's acceleration
                self.pet.set_acceleration([0, self.pet.acceleration[1]])
            else:
                self.pet.idle()

    def compliment(self):
        # makes the pet compliment the user
        if not self.pet.isDragged:
            self.pet.say(np.random.choice(["You're awesome!", "You're the best!", "You're looking great today!", "a a a a a a a"]))

    def remind(self):
        # for each reminder, check if it's time to remind the user
        for reminder in self.reminders:
            if reminder[0] == {"year": time.localtime().tm_year, "month": time.localtime().tm_mon, "day": time.localtime().tm_mday, "hour": time.localtime().tm_hour, "minute": time.localtime().tm_min} and not reminder[2]:
                reminder[2] = True
                self.pet.say(f"Hey! You have a reminder set for this time! {reminder[1]}")
                self.pet.idle()

    def volunteer(self):
        if not self.pet.isDragged:
            random_opportunity = ws.get_random_volunteer_opportunity()
            self.pet.say(f"Hey! {random_opportunity[4]} has a volunteer opportunity you may be interested in! \n\n {random_opportunity[0]} \n {random_opportunity[3]}")


async def main():
    pet_manager = PetManager()
    while True:
        await pet_manager.update()

asyncio.run(main())


