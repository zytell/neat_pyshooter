import random


class RandomSelector:
    def __init__(self):
        self.objects = list()  # list of objects
        self.scores = list()  # scores of object in list
        self.total_score = 0  # sum of scores

    def add(self, element, score):
        # add an object to the random selector
        self.objects.append(element)
        self.scores.append(score)
        self.total_score += score

    def random(self):
        # return a random object
        # the function is built the following way:
        # the higher the score the higher the probability
        # that this object will be chosen.
        if len(self.objects) == 1:
            return self.objects[0]
        v = random.random() * self.total_score
        c = 0
        for obj, score in zip(self.objects, self.scores):
            c += score
            if c > v:
                return obj

