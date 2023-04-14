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
from arguments.couplevalue import CoupleValue

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

        self.preferences.set_criterion_name_list([0, 1, 2, 3, 4, 5])

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

        # Create agents
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
        argument = Argument(True, item)
        premisses = argument.list_supporting_proposal(item, self.preferences)
        return ["Because", item, random.choice(premisses)]

    def counter_proposal(self, proposed_item: Item, couple_value: CoupleValue):
        """
        Find a counter proposal to the given item
        - Try to find an item with a better value for the given criterion
        - If not, consider a better criterion
        - If not, propose a random item
        """
        criterion = couple_value.criterion_name
        value = couple_value.value

        # Find an item with a better value for the given criterion
        for item in self.items:
            item_value = self.preferences.get_value(item, criterion)
            if item_value > value:
                return [
                    "Found better item for this criterion",
                    item,
                    CoupleValue(criterion, item_value),
                ]

        # Consider a better criterion
        best_criterion = None
        for criterion in self.preferences.get_criterion_name_list():
            if criterion != couple_value.criterion_name:
                best_criterion = criterion
            else:
                break
        # Find an item with a better value for the best criterion
        if best_criterion is not None:
            best_criterion_value = self.preferences.get_value(
                proposed_item, best_criterion
            )
            for item in self.items:
                item_value = self.preferences.get_value(item, best_criterion)
                if item_value > best_criterion_value:
                    return [
                        "The criterion is not the most important one",
                        item,
                        CoupleValue(best_criterion, item_value),
                    ]

        # Else random item
        item = random.choice(self.items)
        return [
            "The item is not satisfying, how about...",
            item,
            self.support_proposal(item)[2],
        ]

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()
        for agent in self.schedule.agents:
            unread_messages = agent.get_new_messages()
            for message in unread_messages:
                # Parse the message
                sender = message.get_exp()
                receiver = message.get_dest()
                performative = message.get_performative()
                content = message.get_content()

                # Print the message
                print(f"Message from {sender}: {performative}")
                if isinstance(content, list):
                    for element in content:
                        print(element)
                else:
                    print(content)
                print("")

                # If PROPOSE, send ACCEPT or ASK_WHY
                if performative == MessagePerformative.PROPOSE:
                    if self.preferences.is_item_among_top_10_percent(
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

                # If ACCEPT, send COMMIT
                elif performative == MessagePerformative.ACCEPT:
                    # Send COMMIT message
                    self.__messages_service.send_message(
                        Message(receiver, sender, MessagePerformative.COMMIT, content)
                    )
                    self.commits += 1

                # If COMMIT, send COMMIT and stop the simulation
                elif performative == MessagePerformative.COMMIT:
                    if self.commits == 1:
                        self.__messages_service.send_message(
                            Message(
                                receiver, sender, MessagePerformative.COMMIT, content
                            )
                        )
                        self.commits += 1
                    elif self.commits == 2:
                        print(f"Commitment reached for {content} !\n")
                        self.running = False

                # If ASK_WHY, send ARGUE
                elif performative == MessagePerformative.ASK_WHY:
                    self.__messages_service.send_message(
                        Message(
                            receiver,
                            sender,
                            MessagePerformative.ARGUE,
                            self.support_proposal(content),
                        )
                    )

                # If ARGUE, send ACCEPT or ARGUE
                elif performative == MessagePerformative.ARGUE:
                    [comment, item, couple_value] = content
                    if self.preferences.is_item_among_top_10_percent(item, self.items):
                        self.__messages_service.send_message(
                            Message(receiver, sender, MessagePerformative.ACCEPT, item)
                        )
                    else:
                        self.__messages_service.send_message(
                            Message(
                                receiver,
                                sender,
                                MessagePerformative.ARGUE,
                                self.counter_proposal(item, couple_value),
                            )
                        )


# Run the simulation
argument_model = ArgumentModel()

for i in range(20):
    if not argument_model.running:
        break
    print(f"Step {i}:")
    argument_model.step()
