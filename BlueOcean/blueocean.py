import numpy as np
import matplotlib.pyplot as plt



class BlueOcean:
    figure_size = 8, 4

    def __init__(self, title=None):
        self.title = title if title else self.collect_title()

    def run(self):
        self.collect_metrics()
        self.collect_legend_keys()
        self.score_metrics()
        self.plot()
        self.add_plot_styling()
        plt.show()

    def collect_title(self):
        self.title = input('What will be the topic of your Blue Ocean?\n\n')

    def collect_metrics(self):
        print(f'What factors about {self.title} would you consider important?')
        metrics = []
        while metric := input(f'{len(metrics) + 1}. '):
            metrics.append(metric)
        self.metrics = metrics

    def collect_legend_keys(self):
        '''Defines the legend_keys that will be to each other once data is collected about the metrics & scores.'''
        print(f'What are you measuring your important factors of {self.title} against?')
        legend_keys = []
        while legend_key := input(f'{len(legend_keys) + 1}. '):
            legend_keys.append(legend_key)
        self.legend_keys = legend_keys 

    def score_metrics(self):
        '''For each legend_key, a score is assinged to each metric given in order to create it's own custom array.'''
        score_map = {}
        for legend_key in self.legend_keys:
            print(f'\n Score where you are in "{legend_key}" for...\n')
            score_dict = {}
            for metric in self.metrics:
                score = int(input(f'• {metric.capitalize()}: '))
                score_dict[metric] = score
            score_map[legend_key] = score_dict
        self.score_map = score_map

    def plot(self):
        '''Here the data given above is put into a visual graph based on the users data.'''
        for score_dict in self.score_map.values():
            metrics, scores = zip(*score_dict.items())
            print(metrics, scores)
            plt.plot(metrics, scores, marker=0)
            

    def add_plot_styling(self):
        plt.rcParams['figure.figsize'] = self.figure_size
        plt.title(f"Blue Ocean: {self.title}", loc="left")
        plt.legend(self.legend_keys, loc='upper left', bbox_to_anchor=(1,1))
        plt.xlabel("Important Factors")
        plt.ylabel("Score")
        plt.tight_layout(pad=5)
        plt.yticks(range(1,6),range(1,6))
        plt.xticks(rotation=30)

def main():
    o = BlueOcean('Health')
    o.legend_keys = ['Where I am now', 'Where I want to be']
    o.score_map = {
        'Where I am now': {'Healthy Diet': 1, 'Exercise': 3, 'Exercise Fulfillment': 1},
        'Where I want to be': {'Healthy Diet': 5, 'Exercise': 5, 'Exercise Fulfillment': 5}
    }
    o.plot()
    o.add_plot_styling()
    plt.show()

if __name__ == '__main__':
	main()
