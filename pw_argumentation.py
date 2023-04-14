""" This file contains the code for the argumentation model. """
import random

import pandas as pd
from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative

from communication.preferences.Preferences import Preferences
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Item import Item
from communication.preferences.CriterionName import criterion_find

from arguments.argument import Argument

DATASET_PATH = "weapons_dataset.csv"


class ArgumentAgent(CommunicatingAgent):
    """ArgumentAgent which inherit from CommunicatingAgent ."""

    def __init__(self, unique_id, model, name, preferences):
        super().__init__(unique_id, model, name)
        self.preferences = preferences


class ArgumentModel(Model):
    """ArgumentModel which inherit from Model ."""

    def __init__(self):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)

        self.preferences = Preferences()
        self.commits = 0

        # Read the dataset
        dataset = pd.read_csv(DATASET_PATH, sep=";")

        self.preferences.set_criterion_name_list(
            [criterion_find(column) for column in dataset.columns if column != "WEAPON"]
        )

        # Add values
        self.items = []
        for _, row in dataset.iterrows():
            new_item = Item(row["WEAPON"], "")
            self.items.append(new_item)
            for column in dataset.columns:
                if column != "WEAPON":
                    self.preferences.add_criterion_value(
                        CriterionValue(
                            new_item,
                            criterion_find(column),
                            row[column],
                        )
                    )

        agent1 = ArgumentAgent(1, self, "A", self.preferences)
        self.schedule.add(agent1)

        agent2 = ArgumentAgent(2, self, "B", self.preferences)
        self.schedule.add(agent2)

        self.running = True
        self.__messages_service.send_message(
            Message("A", "B", MessagePerformative.PROPOSE, random.choice(self.items))
        )

    def support_proposal(self, item):
        """
        Used when the agent receives " ASK_WHY " after having proposed an item
        : param item : str - name of the item which was proposed
        : return : string - the strongest supportive argument
        """
        premisses = Argument.list_supporting_proposal(item, self.preferences)
        return random.choice(premisses)

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()
        for agent in self.schedule.agents:
            unread_messages = agent.get_new_messages()
            print(agent.get_name() + " has " + str(len(unread_messages)) + " messages.")
            for message in unread_messages:
                print(message.get_content())
                sender = message.get_exp()
                receiver = message.get_dest()
                performative = message.get_performative()
                content = message.get_content()
                if performative == MessagePerformative.PROPOSE:
                    if self.preferences.is_item_among_top_20_percent(
                        content, self.items
                    ):
                        self.__messages_service.send_message(
                            Message(
                                receiver, sender, MessagePerformative.ACCEPT, content
                            )
                        )
                    else:
                        self.__messages_service.send_message(
                            Message(
                                receiver, sender, MessagePerformative.ASK_WHY, content
                            )
                        )
                elif performative == MessagePerformative.ACCEPT:
                    # Send COMMIT message
                    self.__messages_service.send_message(
                        Message(receiver, sender, MessagePerformative.COMMIT, content)
                    )
                    self.commits += 1
                elif performative == MessagePerformative.COMMIT:
                    if self.commits == 1:
                        self.__messages_service.send_message(
                            Message(
                                receiver, sender, MessagePerformative.COMMIT, content
                            )
                        )
                        self.commits += 1
                    elif self.commits == 2:
                        self.running = False
                        print(f"Proposition accepted: {content.get_name()}")

                elif performative == MessagePerformative.ASK_WHY:
                    self.running = False
                    print("Proposition rejected")


argument_model = ArgumentModel()
for i in range(10):
    if not argument_model.running:
        break
    print(f"\nStep {i}")
    argument_model.step()
