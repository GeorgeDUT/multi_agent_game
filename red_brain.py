import random
import numpy as np
import pandas as pd
import platform
import tensorflow as tf

os = platform.platform()
if os.find('Darwin')==-1:
    print('this version is not mac')
else:
    print('this version is mac')


def find_target(s):
    for i in range(len(s)):
        for j in range(len(s[0])):
            if s[i][j]==2:
                x,y=j,i
                return x,y
                # break
    return x,y


def goto_target(x,y,t_x,t_y,env_map):
    other_dis = []
    averge = 0.0
    for i in range(len(env_map)):
        for j in range(len(env_map[0])):
            if env_map[i][j] == 1:
                dis = abs(t_x - j) + abs(t_y - i)
                other_dis.append(dis)
    for i in range(len(other_dis)):
        averge = averge + other_dis[i] * 1.0 / len(other_dis)

    if (abs(t_x - x) + abs(t_y - y))< averge*0.6:
        action = 's'
    else:
        '''find short path start bfs'''
        dis_map = np.zeros(shape=(len(env_map), len(env_map[0])))
        for i in range(len(dis_map)):
            for j in range(len(dis_map[0])):
                dis_map[i][j] = 9999
        dir = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        dis_map[t_y][t_x] = 0
        que = []
        que.append([t_x, t_y])
        # flag=1,find a path, else no
        flag=0
        while len(que):
            front = que[0]
            del (que[0])
            if front[0] == x and front[1] == y:
                flag=1
                break
            for i in range(4):
                n_x = front[0] + dir[i][0]
                n_y = front[1] + dir[i][1]
                if 0 <= n_x < len(env_map[0]) and 0 <= n_y < len(env_map) and dis_map[n_y][n_x] == 9999 and \
                        env_map[n_y][n_x] == 0:
                    dis_map[n_y][n_x] = dis_map[front[1]][front[0]] + 1
                    que.append([n_x, n_y])
                if n_x==x and n_y==y:
                    dis_map[n_y][n_x] = dis_map[front[1]][front[0]] + 1
                    que.append([n_x, n_y])
        '''find short path end'''
        #if dis_map[y][x] == 9999:
        if flag==1:
            short_dir=[]
            for i in range(4):
                to_x = x + dir[i][0]
                to_y = y + dir[i][1]
                if 0 <= to_x < len(env_map[0]) and 0 <= to_y < len(env_map):
                    short_dir.append(dis_map[to_y][to_x])
                else:
                    short_dir.append(9999)
            if short_dir.index(min(short_dir))==0:
                action='r'
            elif short_dir.index(min(short_dir))==1:
                action='l'
            elif short_dir.index(min(short_dir))==2:
                action='d'
            elif short_dir.index(min(short_dir))==3:
                action='u'
        else:
            if x > t_x and y >= t_y:
                if random.random() > 0.8:
                    action = 'l'
                else:
                    action = 'u'
            elif x <= t_x and y > t_y:
                if random.random() > 0.2:
                    action = 'r'
                else:
                    action = 'u'
            elif x < t_x and y <= t_y:
                if random.random() > 0.8:
                    action = 'r'
                else:
                    action = 'd'
            elif x >= t_x and y < t_y:
                if random.random() > 0.2:
                    action = 'l'
                else:
                    action = 'd'
            else:
                action = 's'

    '''
    if x>t_x and y>=t_y:
        if random.random()>0.8:
            action='l'
        else:
            action='u'
    elif x<=t_x and y>t_y:
        if random.random()>0.2:
            action='r'
        else:
            action='u'
    elif x < t_x and y <= t_y:
        if random.random()> 0.8:
            action = 'r'
        else:
            action = 'd'
    elif x>=t_x and y<t_y:
        if random.random() > 0.2:
            action = 'l'
        else:
            action = 'd'
    else:
        action='s'
    '''
    return action


class RL(object):
    def __init__(self,action_space, learning_rate=0.01,reward_decay=0.9,e_greedy=0.9):
        self.actions = action_space
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = []
        self.q_table = pd.DataFrame(columns=self.actions,dtype=np.float64)

    def check_state_exist(self,state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0] * len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    def choose_action(self, observation):
        self.check_state_exist(observation)
        # choose action use e_greedy method
        if np.random.rand() < self.epsilon:
            state_action = self.q_table.loc[observation,:]
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            action = state_action.idxmax()
        else:
            action = np.random.choice(self.actions)
        # TODO: softmax method

        return action

    def learn(self, *arg):
        pass


class QLearningTable(RL):
        def __init__(self,actions, learning_rate=0.01,reward_decay=0.9,e_greedy=0.9):
            super(QLearningTable,self).__init__(actions, learning_rate, reward_decay, e_greedy)

        def learn(self, s,a,r,s_):
            self.check_state_exist(s_)
            q_predict = self.q_table.loc[s,a]
            if s_ != 'terminal':
                q_target = r+self.gamma*self.q_table.loc[s_,:].max()
            else:
                q_target = r
            self.q_table.loc[s,a]+=self.lr*(q_target-q_predict)


class DQN:
    def __init__(
            self,
            n_actions,
            n_features,
            learning_rate=0.01,
            reward_decay=0.9,
            e_greedy=0.5,
            replace_target_iter=300,
            memory_size=30000,
            batch_size=126,
            e_greedy_increment=None,
            output_graph=False,
    ):
        self.n_actions = n_actions
        self.n_features = n_features
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon_max = e_greedy
        self.replace_target_iter = replace_target_iter
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.epsilon_increment = e_greedy_increment
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max
        # total learning step
        self.learn_step_counter = 0
        # initialize zero memory [s, a, r, s_]
        self.memory = np.zeros((self.memory_size, n_features * 2 + 2))
        # consist of [target_net, evaluate_net]
        self._build_net()
        t_params = tf.get_collection('target_net_params')
        e_params = tf.get_collection('eval_net_params')
        self.replace_target_op = [tf.assign(t, e) for t, e in zip(t_params, e_params)]
        self.sess = tf.Session()
        if output_graph:
            # $ tensorboard --logdir=logs

            # tf.train.SummaryWriter soon be deprecated, use following

            tf.summary.FileWriter("logs/", self.sess.graph)
        self.sess.run(tf.global_variables_initializer())
        self.cost_his = []

    def _build_net(self):
        # ------------------ build evaluate_net ------------------
        self.s = tf.placeholder(tf.float32, [None, self.n_features], name='s')  # input
        self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='Q_target')  # for calculating loss
        with tf.variable_scope('eval_net'):
            # c_names(collections_names) are the collections to store variables
            c_names, n_l1, w_initializer, b_initializer = \
                ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES], 10, \
                tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)  # config of layers

            # first layer. collections is used later when assign to target net
            with tf.variable_scope('l1'):
                w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                l1 = tf.nn.relu(tf.matmul(self.s, w1) + b1)
            # second layer. collections is used later when assign to target net
            with tf.variable_scope('l2'):
                w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_eval = tf.matmul(l1, w2) + b2
        with tf.variable_scope('loss'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
        with tf.variable_scope('train'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)
        # ------------------ build target_net ------------------
        self.s_ = tf.placeholder(tf.float32, [None, self.n_features], name='s_')    # input
        with tf.variable_scope('target_net'):
            # c_names(collections_names) are the collections to store variables
            c_names = ['target_net_params', tf.GraphKeys.GLOBAL_VARIABLES]
            # first layer. collections is used later when assign to target net
            with tf.variable_scope('l1'):
                w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                l1 = tf.nn.relu(tf.matmul(self.s_, w1) + b1)
            # second layer. collections is used later when assign to target net
            with tf.variable_scope('l2'):
                w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_next = tf.matmul(l1, w2) + b2

    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter'):
            self.memory_counter = 0
        transition = np.hstack((s, [a, r], s_))
        # replace the old memory with new memory
        index = self.memory_counter % self.memory_size
        self.memory[index, :] = transition
        self.memory_counter += 1

    def choose_action(self, observation):
        # to have batch dimension when feed into tf placeholder
        observation = observation[np.newaxis, :]
        if np.random.uniform() < (1-self.epsilon):
            action = np.random.randint(0, self.n_actions)
        else:
            # forward feed the observation and get q value for every actions
            actions_value = self.sess.run(self.q_eval, feed_dict={self.s: observation})
            action = np.argmax(actions_value)
        return action

    def learn(self):
        # check to replace target parameters
        if self.learn_step_counter % self.replace_target_iter == 0:
            self.sess.run(self.replace_target_op)
            #print('\ntarget_params_replaced\n')
        # sample batch memory from all memory
        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_counter, size=self.batch_size)
        batch_memory = self.memory[sample_index, :]
        q_next, q_eval = self.sess.run(
            [self.q_next, self.q_eval],
            feed_dict={
                self.s_: batch_memory[:, -self.n_features:],  # fixed params
                self.s: batch_memory[:, :self.n_features],  # newest params
            })
        # change q_target w.r.t q_eval's action
        q_target = q_eval.copy()
        batch_index = np.arange(self.batch_size, dtype=np.int32)
        eval_act_index = batch_memory[:, self.n_features].astype(int)
        reward = batch_memory[:, self.n_features + 1]
        q_target[batch_index, eval_act_index] = reward + self.gamma * np.max(q_next, axis=1)
        # train eval network
        _, self.cost = self.sess.run([self._train_op, self.loss],
                                     feed_dict={self.s: batch_memory[:, :self.n_features],
                                                self.q_target: q_target})

        self.cost_his.append(self.cost)
        # increasing epsilon
        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
        self.learn_step_counter += 1

    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()
