from datetime import datetime
from datetime import timezone
import numpy
import re
from collections import Counter
from scipy.stats import mannwhitneyu
import helpers.statics as statics
import json
import matplotlib.pyplot as plt

class Date:
    DMY = '%Y-%m-%d'
    YMV = '%Y-%m-%V'
    YV = '%Y-%V'
    V = '%V'
    Y = '%Y'
    M = '%m'
    D = "%A"
    DMYHMS = '%Y-%m-%d %H:%M:%S'
    DMYHMSZ = '%Y-%m-%d %H:%M:%S %z'

    @staticmethod
    def get_timestamp_year_week(date_field):
        datetime_object = datetime.strptime(date_field + '-1', '%Y-%W-%w')
        timestamp = datetime.timestamp(datetime_object)
        return int(timestamp)

    @staticmethod
    def to_timestamp(date_field, local_time=False) -> int:
        """
        Converts Given Time in the format of '2017-11-14 19:09:20 +1300' to timestamp.
        :param local_time: boolean indicates whether we want the local time or UTC time. It removes +0000 from the end
        :param date_field: string of date
        :return: timestamp of the give date in arguments
        :rtype: int
        """
        if not date_field:
            return False
        # 2020-12-28T22:46:14Z
        # If the input is in gitlog format (Wed Oct 18 13:05:28 2017 +1300), we change it to normal date (2017-10-30
        # 15:31:32 +1300)
        if len(date_field.split()) == 6:
            date_field = date_field.split()[4] + "-" + str(Date.fetch_month_number(date_field.split()[1])) + "-" + \
                         date_field.split()[2] + " " + \
                         date_field.split()[3] + " " + date_field.split()[5]

        # if the input is 2015-03-24 we change it to 2015-03-24 00:00:00 +0000
        if len(date_field) == 10:
            date_field = date_field + " 00:00:00 +0000"

        # if the input is in github format 2020-12-28T22:46:14Z
        if len(date_field.split('T')) == 2:
            date_field = date_field.replace("Z", "")
            date_field = date_field.split('T')[0] + " " + date_field.split('T')[1] + " +0000"

        # COnvert the date into timestamp
        if local_time:
            date_field = date_field[:-6] + " +0000"

        datetime_object = datetime.strptime(date_field, "%Y-%m-%d %H:%M:%S %z")
        timestamp = datetime.timestamp(datetime_object)
        return int(timestamp)

    def fetch_month_number(self):
        """
        From the given month name it returns the month number (e.g. 'Jan')
        :param self: string of month char
        :return: number of month
        :rtype: int
        """
        if self == 'Jan':
            return 1
        elif self == 'Feb':
            return 2
        elif self == 'Mar':
            return 3
        elif self == 'Apr':
            return 4
        elif self == 'May':
            return 5
        elif self == 'Jun':
            return 6
        elif self == 'Jul':
            return 7
        elif self == 'Aug':
            return 8
        elif self == 'Sep':
            return 9
        elif self == 'Oct':
            return 10
        elif self == 'Nov':
            return 11
        elif self == 'Dec':
            return 12
        else:
            raise Exception("not supported month string")

    def get_seperate(self, what='d'):
        if what == 'd':
            return self / (60 * 60 * 24)

    def to_date(self, return_format):
        timestamp = self
        dt_obj = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime(return_format)
        return dt_obj


def generate_weeks(start, end):
    """
    gives weeks btw two weeks
    :param start: start point
    :param end: end point
    """
    first_year = int(str(start)[:4])
    last_year = int(str(end)[:4])
    first_week = int(str(start)[4:])
    last_week = int(str(end)[4:])

    all_weeks = []

    for i in range(first_week, 54):
        all_weeks.append(int(str(first_year) + str(i).zfill(2)))

    for i in range(first_year + 1, last_year):
        for j in range(1, 54):
            all_weeks.append(int(str(i) + str(j).zfill(2)))

    for i in range(1, last_week + 1):
        all_weeks.append(int(str(last_year) + str(i).zfill(2)))

    return all_weeks


class Math:
    @staticmethod
    def remove_outliers(arr):
        elements = numpy.array(arr)

        mean = numpy.mean(elements, axis=0)
        sd = numpy.std(elements, axis=0)

        final_list = [x for x in arr if (x > mean - 2 * sd)]
        final_list = [x for x in final_list if (x < mean + 2 * sd)]
        return final_list

    @staticmethod
    def median(lst):
        return numpy.quantile(lst, .5)

    @staticmethod
    def third_quantile(lst):
        return numpy.quantile(lst, .75)

    @staticmethod
    def mean(lst):
        return sum(lst) / len(lst)


class Validate:
    @staticmethod
    def check(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, email)):
            return True
        else:
            return False


class Cleaner:
    @staticmethod
    def email(author_email):
        # 49656678+hkeebler@users.noreply.github.com>
        if not Validate.check(author_email):
            # clean emails like shayan@apache.org@hash(e.g. david@mygrid.org.uk@bf327186-88b3-11dd-a302-d386e5130c1c)
            if Counter(author_email)['@'] == 2:
                tmp = author_email.split('@')
                result = (tmp[0] + tmp[1], 'known')
            else:
                result = (author_email, 'unknown')
        else:
            result = (author_email, 'known')
        return result


class Operations:
    @staticmethod
    def sum_2d_lists(a, b):
        c = []
        for i in range(0, len(a)):
            c.append([])
        for loc in range(0, len(a)):
            c[loc] = a[loc] + b[loc]
        return c

    @staticmethod
    def subtract_dicts(first, second):
        difference = {}
        for k, v in second.items():
            difference[k] = v - first.get(k, 0)
        return difference

    @staticmethod
    def dictionary_percentile(input):
        result = {}
        sum_of_values = sum(input.values())
        for key, value in input.items():
            result[key] = value/sum_of_values
        return result




class Statistical:
    @staticmethod
    def mannwhitneyu(s1, s2):
        s1 = list(s1)
        s2 = list(s2)
        stat, p = mannwhitneyu(s1, s2)
        return stat, p

    @staticmethod
    def interpolate(inp, fi):
        i, f = int(fi // 1), fi % 1  # Split floating-point index into whole & fractional parts.
        j = i + 1 if f > 0 else i  # Avoid index error.
        print(inp)
        print(i, j)
        return (1 - f) * inp[i] + f * inp[j]


class Designite:
    @staticmethod
    def pretty(input_file):
        smell_counts = []
        for word in input_file.split():
            if word.isdigit():
                smell_counts.append(int(word))
        try:
            # skip this line -> The trial version allows you to analyze an application lesser than 50000 lines of code
            # in size. The selected application has crossed the threshold, therefore the detailed results are disabled.
            # Please consider buying a Professional edition of the tool for unrestricted access to the functionality.
            if smell_counts[0] == 50000:
                smell_counts.pop(0)

            results = {}
            for i in range(0, len(statics.designite_headers)):
                results[statics.designite_headers[i]] = smell_counts[i]
        except IndexError:
            # print('Error')
            return False

        return results

    @staticmethod
    def results(just_smells = False, smell_types = False):
        results = {}
        with open("data/borders.json") as json_file:
            borders = json.load(json_file)
        for repo, points in borders.items():
            results[repo] = {}
            for i in range(0, len(points.keys())):
                time_window = str(i-1)+"-"+str(i)
                file_name = '/designite_'+str(i)+'.txt'
                designite_directory = 'data/metrics/'
                directory = designite_directory+repo+file_name
                try:
                    a_file = open(directory, "r")
                    designite_file = a_file.read()
                except FileNotFoundError:
                    print("skipped "+directory+time_window)
                    continue
                designite_json = Designite.pretty(designite_file)
                # File has some issues with collection of dataset
                if designite_json:
                    if just_smells:
                        designite_json.pop('Total LOC analyzed', None)
                        designite_json.pop('Number of packages', None)
                        designite_json.pop('Number of classes', None)
                        designite_json.pop('Number of methods', None)
                    results[repo][time_window] = designite_json

        # Filter results into desired smell_types
        if smell_types:
            refined_smells = {}
            for repo, time_windows in results.items():
                refined_smells[repo] = {}
                for time_window, code_smells in time_windows.items():
                    refined_smells[repo][time_window] = {}
                    for code_smell, counts in code_smells.items():
                        if code_smell in smell_types:
                            refined_smells[repo][time_window][code_smell] = counts
            results = refined_smells


        return results

class Plot:
    """
    This class is responsible to generate plots easy
    """

    @staticmethod
    def violin_plot(data, x_lable, y_lable):
        """
        Generate violin plot
        :param data: should be a dict {'a': [1,2,3], 'b': [1,2,3] ....}
        :param x_lable:
        :param y_lable:
        """
        labels, data = [*zip(*data.items())]
        plt.violinplot(data, showmeans=True)
        plt.xticks(range(1, len(labels) + 1), labels, rotation=90)
        plt.xlabel(x_lable)
        plt.ylabel(y_lable)
        plt.show()

    @staticmethod
    def box_plot(data, x_lable, y_lable, title):
        """
        Generate box plot
        :param data: should be a dict {'a': [1,2,3], 'b': [1,2,3] ....}
        :param x_lable:
        :param y_lable:
        """
        labels, data = [*zip(*data.items())]
        plt.boxplot(data, showmeans=True, showfliers=False)
        plt.xticks(range(1, len(labels) + 1), labels, rotation=30)
        plt.xlabel(x_lable)
        plt.ylabel(y_lable)
        plt.title(title)
        plt.show()

    @staticmethod
    def bar_plot(data, x_lable, y_lable):
        """
        Generate box plot
        :param data: should be a dict {'a': 20, 'b': 10 ....}
        :param x_lable:
        :param y_lable:
        """
        plt.bar(range(len(data)), list(data.values()), align='center')
        plt.xticks(range(len(data)), list(data.keys()), rotation=90)
        plt.xlabel(x_lable)
        plt.ylabel(y_lable)
        plt.show()

    @staticmethod
    def hue_violing(refactoring, development):
        import seaborn as sns
        import matplotlib.pyplot as plt
        import pandas as pd
        from matplotlib.lines import Line2D

        to_convert = []
        for day, lines in refactoring.items():
            for line in lines:
                to_convert.append(['refactoring', day, line])
        for day, lines in development.items():
            for line in lines:
                to_convert.append(['development', day, line])

        to_convert = pd.DataFrame(to_convert, columns=["rhythm", "day", "loc"])

        mean = to_convert['day'].mean()
        sd = to_convert['day'].std()

        to_convert = to_convert[(to_convert['day'] <= mean + (3 * sd))]


        print(to_convert)
        # Load the dataset
        tips = sns.load_dataset("tips")

        print(tips)
        # exit()

        sns.violinplot(data=to_convert, x="day", y="loc", hue="rhythm", split=True)
        plt.show()

class FileManager:
    @staticmethod
    def read_json(directory):
        with open(directory) as json_file:
            return json.load(json_file)

    @staticmethod
    def dump_json(data, directory):
        out_file = open(directory, "w")
        json.dump(data, out_file, indent=4)
        out_file.close()

    @staticmethod
    def read_data(directory):
        with open(directory, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def dump_data(data, directory):
        with open(directory, 'wb') as f:
            pickle.dump(data, f)




