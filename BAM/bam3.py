'''
Working example of Bidirectional associative memory
Encoding objects without the images:

NN-Team-2
'''

import numpy as np


class BAM(object):
    def __init__(self, data):
        self.AB = []
        # store associations in bipolar form to the array
        for item in data:
            self.AB.append(
                [self.__l_make_bipolar(item[0]),
                 self.__l_make_bipolar(item[1])]
            )
        self.len_x = len(self.AB[0][1])
        self.len_y = len(self.AB[0][0])
        # create empty BAM matrix
        self.M = [[0 for x in range(self.len_x)] for x in range(self.len_y)]
        # compute BAM matrix from associations
        self.__create_bam()

    def __create_bam(self):
        '''Bidirectional associative memory'''
        for assoc_pair in self.AB:
            X = assoc_pair[0]
            Y = assoc_pair[1]
            # calculate M
            for idx, xi in enumerate(X):
                for idy, yi in enumerate(Y):
                    self.M[idx][idy] += xi * yi

    def get_assoc(self, A):
        '''Return association for input vector A'''
        A = self.__mult_mat_vec(A)
        return self.__threshold(A)

    def get_bam_matrix(self):
        '''Return BAM matrix'''
        return self.M

    def __mult_mat_vec(self, vec):
        '''Multiply input vector with BAM matrix'''
        v_res = [0] * self.len_x
        for x in range(self.len_x):
            for y in range(self.len_y):
                v_res[x] += vec[y] * self.M[y][x]
        return v_res

    def __threshold(self, vec):
        '''Transform vector to [0, 1]'''
        ret_vec = []
        for i in vec:
            if i < 0:
                ret_vec.append(0)
            else:
                ret_vec.append(1)
        return ret_vec

    def __l_make_bipolar(self, vec):
        '''Transform vector to bipolar form [-1, 1]'''
        ret_vec = []
        for item in vec:
            if item == 0:
                ret_vec.append(-1)
            else:
                ret_vec.append(1)
        return ret_vec


if __name__ == "__main__":

    #Generate some fake data:
    # descriptors = [
    #     ['category', [0, 0]]
    #     ['fur', [0]],
    #     ['body color', [0, 0]],
    #     ['legs', [0, 0, 0]],
    #     ['size', [0, 0, 0]],
    #     ['fin direction', [0, 0]]
    # ]

    # generate all possible dog descriptions
    dogs = []
    for i in range(4):
        for j in range(4):
            dogs.append([
                0, 1,                                               # category
                1,                                                  # fur
                1 if i >= 2 else 0, 1 if i % 2 != 0 else 0,         # body color
                1, 0, 0,                                            # legs
                0, 1 if j >= 2 else 0, 1 if j % 2 != 0 else 0,      # size
                0, 0                                                # fin direction
            ])

    # generate all possible elephants
    elephants = []
    for i in range(2):
        for j in range(4):
            elephants.append([
                0, 1,
                0,
                1 if i >= 2 else 0, 1 if i % 2 != 0 else 0,
                1, 0, 0,
                1 if j >= 2 else 0, 1 if j % 2 != 0 else 0, 0,
                0, 0
            ])

    data_pairs = []
    for i in range(dogs.__len__()):
        data_pairs.append([dogs[i], [1, 0, 0, 0, 0, 0, 0, 0, 0]])
    for i in range(elephants.__len__()):
        data_pairs.append([elephants[i], [0, 1, 0, 0, 0, 0, 0, 0, 0]])

    b = BAM(data_pairs)

    print('\n')
    for i in range(dogs.__len__()):
        print('test[{},:] ---> '.format(i), b.get_assoc(data_pairs[i][0]))
        print('       expecting: ', [1, 0, 0, 0, 0, 0, 0, 0, 0])
        print('')

    print ('---')
    for i in range(elephants.__len__()):
        print('test[{},:] ---> '.format(i+dogs.__len__()), b.get_assoc(data_pairs[i+dogs.__len__()][0]))
        print('       expecting: ', [0, 1, 0, 0, 0, 0, 0, 0, 0])
        print('')