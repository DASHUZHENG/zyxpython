# -*- coding: utf-8 -*-
# version=0.1 author=Zheng YX
from __future__ import division
import pandas
import random
import pdb
import time
import os
import numpy


def ztest():

    vacab = pandas.read_excel("zenglish.xlsx")

    size = vacab.index.size

    answer = {"1": None, "2": None, "3": None, "4": None}

    while True:

        num = random.randint(0, size)

        word = vacab["Word"][num]

        vacab["Appear"][num] += 1

        # pdb.set_trace()

        answer_list = random.sample(range(0, size), 3)

        answer_list.append(num)

        random.shuffle(answer_list)

        for seq in answer:

            answer[seq] = answer_list.pop()

        print("%s\n" % word)

        print("1.%s\n" % vacab["Chinese"][answer["1"]])
        print("2.%s\n" % vacab["Chinese"][answer["2"]])
        print("3.%s\n" % vacab["Chinese"][answer["3"]])
        print("4.%s\n" % vacab["Chinese"][answer["4"]])

        user_input = raw_input()

        print "\n"

        while user_input not in ["1", "2", "3", "4", "q"]:

            user_input = raw_input("Input Illegal!")

            print "\n"

        if user_input != "q":

            if answer[user_input] == num:

                print "right!\n"

                vacab["Correct"][num] += 1

                vacab["ratio"][num] = vacab["Correct"][num] / \
                    vacab["Appear"][num]

            else:

                print "wrong!\n"

        else:

            vacab.to_excel("zenglish.xlsx")

            break


class ZVacab(object):

    def __init__(self, excel="zenglish.xlsx", time_interim=0.5):

        self.vacab = pandas.read_excel(excel)

        self.size = self.vacab.index.size

        self.interim = time_interim

        # Weighted Score 2
        self.vacab["Score"] = self.vacab[[
            "Assess_score", "Recite_score"]].min(axis=1)
        self.vacab["Weight"] = self.vacab["Score"] * self.vacab["Score"] - 1

        #__call__ behavior control

        self.mode=0

        self._start = 0

        self._end = self.size

        self._counter = 0

        self._check=True

    # def __enter__():

    # def __exit__():

    def __call__(self):

        print "Test Start"

        self.mode_set()

        try:

            while self._check:

                num, answer = self.question()

                self.screen_show(num, answer)

                user_ansewer, react_time = self.answer()

                self.check(user_ansewer, react_time, num, answer)

                self.update(num, answer)

                time.sleep(self.interim)

            self.vacab.to_excel("zenglish.xlsx")

            self.log()

            print "Done"

        finally:

            print "All Process Done"

    def mode_set(self):

        self.mode = raw_input("1.选择题;2.顺序背诵;3.测评;4.背诵测试;5.其他")

        start = input("Start Point (0-%s):" % (self.vacab.index.size - 1))

        end = input("End Point(%s-%s):" % (start, self.vacab.index.size - 1))

        if not (start < self.vacab.index.size or start +
                test_length < self.vacab.index.size):

            start = 0

            end = self.vacab.index.size - 1

        self.vacab_test = self.vacab[start:end]

        self._start = start

        self._end = end

        self._counter = start

    def question(self):

        if self.mode == "1":

            answer = {"1": None, "2": None, "3": None, "4": None}

            #rand_answer=lambda x:random.randint(self._start,self._end)
            # 产生随机问题
            # num=rand_answer(1)

            num = random.randint(self._start, self._end)

            self.vacab["Appear"][num] += 1

            answer_list = random.sample(range(0, self.size), 3)

            answer_list.append(num)

            random.shuffle(answer_list)

            for seq in answer:

                answer[seq] = answer_list.pop()

        if self.mode == "2":
            # Sequential Reciting
            num = self._counter

            answer = self._counter

            self.vacab["Recite"][num] += 1

            self._counter += 1

        if self.mode == "3":
            # Sequential Reciting
            num = self._counter

            answer = self._counter

            self._counter += 1

            return num, answer

        if self.mode == "4":

            divisor = self.vacab_test["Weight"].sum()

            # pdb.set_trace()

            if divisor != 0:

                probability = self.vacab_test["Weight"] / divisor

                num = numpy.random.choice(
                    range(
                        self._start,
                        self._end),
                    1,
                    p=probability)[0]

                self.vacab["Recite"][num] += 1

                answer = num

                self._counter += 1

            else:

                print("Your Reciting Queue is empty")

                num = 0

                answer = 0

                self._check = False

            return num, answer

    def screen_show(self, num, answer):

        if self.mode == "1":

            os.system("cls")

            print("%s\n\n" % self.vacab["Word"][num])

            print("1.%s\n" % self.vacab["Chinese"][answer["1"]])
            print("2.%s\n" % self.vacab["Chinese"][answer["2"]])
            print("3.%s\n" % self.vacab["Chinese"][answer["3"]])
            print("4.%s\n" % self.vacab["Chinese"][answer["4"]])

        if self.mode == "2":

            os.system("cls")

            print("Question No.%s\n\n" % (self._counter - self._start))

            print("%s\n\n" % self.vacab["Word"][num])

            print("%s\n\n" % self.vacab["Chinese"][answer])

            print("1.Easy 2.Hard 3. Hell q.Quit\n")

            if self._counter >= self._end:

                print("You can finish the study now!\n")

        if self.mode == "3":

            os.system("cls")

            print("Question No.%s\n\n" % (self._counter - self._start))

            print("%s\n\n" % self.vacab["Word"][num])

            #print("%s\n\n" % self.vacab["Chinese"][answer])

            print("1.Easy 2.Hard 3. Hell q.Quit\n")

            if self._counter >= self._end:

                print("You can finish the study now!\n")

        if self.mode == "4":

            os.system("cls")

            print("Question No.%s\n\n" % (self._counter - self._start))

            print("%s\n\n" % self.vacab["Word"][num])

            #print("%s\n\n" % self.vacab["Chinese"][answer])

            print("1.Easy 2.Hard 3. Hell q.Quit\n")

    def answer(self):

        start = time.time()

        user_input = raw_input()

        print "\n"

        while user_input not in ["1", "2", "3", "4", "q"]:

            user_input = raw_input("Input Illegal!")

            print "\n"

        end = time.time()

        return user_input, end - start

    def check(self, user_input, period, num, answer):

        if self.mode == "1":

            if user_input != "q":

                if answer[user_input] == num:

                    print "right!\n"

                    self.vacab["Correct"][num] += 1

                    self.vacab["Ratio"][num] = self.vacab["Correct"][num] / \
                        self.vacab["Appear"][num]

                else:

                    print "wrong!\n"

            else:

                self._check = False

        if self.mode == "2":

            if user_input != "q":

                self.vacab["Assess"][num] = user_input

            else:

                self._check = False

        if self.mode == "3":

            # assess_score={"1":1,"2":0.5,"3":0,"4":0}

            if user_input != "q":

                self.vacab["Assess"][num] = user_input

                self.vacab["Assess_score"][num] = user_input

            else:

                self._check = False

        if self.mode == "4":

            # assess_score={"1":1,"2":0.5,"3":0,"4":0}

            if user_input != "q":

                self.vacab["Recite"][num] += 1

                self.vacab["Recite_score"][num] = user_input

            else:

                self._check = False

    def update(self, num, answer):

        # Score Update

        # self.vacab["Score"][num]=0.5*self.vacab["Correct"][num]/(self.vacab["Appear"][num]+1)+0.5*self.vacab["Assess_score"][num]

        # self.vacab["Weight"][num]=self.weight(self.vacab["Score"][num])

        self.vacab["Score"][num] = min(
            self.vacab["Recite_score"][num],
            self.vacab["Assess_score"][num])

        self.vacab["Weight"][num] = self.vacab["Score"][num] * \
            self.vacab["Score"][num] - 1

        if self.mode == "3" or self.mode == "4":

            print("%s\n\n" % self.vacab["Chinese"][answer])

    def weight(self, number):

        if number <= 0.3:

            result = 5

        elif number <= 0.6:

            result = 3

        elif number <= 0.8:

            result = 1

        else:

            result = 0

        return result

    def log(self):

        if not os.path.isfile("zenglish_log.txt"):

            with open("zenglish_log.txt", "wb") as f:

                print "New Log generated"

        with open("zenglish_log.txt", "a") as f:

            f.write("\n\n%s" % time.asctime())

            f.write("\nStudy Length:%s" % (self._counter - self._start))

            overall = len(self.vacab["Assess"])

            studied = len(self.vacab["Assess"][self.vacab["Assess"] != 0])

            learned = len(self.vacab["Assess"][self.vacab["Assess"] == 1])

            level1 = len(self.vacab["Assess"]
                         [self.vacab["Assess"] == 1]) / studied

            level2 = len(self.vacab["Assess"]
                         [self.vacab["Assess"] == 2]) / studied

            level3 = len(self.vacab["Assess"]
                         [self.vacab["Assess"] == 3]) / studied

            f.write(
                "\noverall:%s; stuided: %s; learned: %s; ratio:%.2f" %
                (overall, studied, learned, studied / overall))

            f.write(
                "\nlearned:%.2f; umfamiliar:%.2f; unlearned %.2f;" %
                (level1, level2, level3))


if __name__ == "__main__":

    a = ZVacab()

    a()
