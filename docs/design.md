# Manifold Design Docs

The design docs will be available for essentially every developer that wants to pick up the work of working on the `manifold` library.

The purpose of `manifold` is to provide multi-objective rewards to reinforcement learning. To understand what this library actually is in detail we need to ensure you have a solid understanding prior information.

## What is Machine Learning?

Machine learning the action of closing the distance of a belief to a core truth. That's a fancy word for optimization, where optimization is the movement of our beliefs of how X contributes to X. The most classic version of this is what we call linear regression. It's formed by getting a data set, then finding a line that best fits the dataset. It does that using `Y=Mx+B`, where `B` is the compared intercept, `x` is the current location you are in a coordinate plane, and `M` is the slope between a dataset; `Y` is the result of implanting `X` into that line.


Machine learning is largely that. Everything beyond that point is figuring out how to make it so that `x` will give a better prediction result `Y`. 

1. System identification
2. Deep Learning
3. Trees
4. Etc

They all are focused on ensuring `x` accurately corresponds to `Y`, and we use accuracy as a measure to it.


There's ML for many applications:

* Image Classification
* Predicting Housing Prices
* Credit Risk
* NLP
* Knowledge Graphs


The list is largely endless. What we're focusing on is something called Reinforcement Learning(RL for short). We're going to overview what Reinforcement Learning is in the next segment.



## What is Reinforcement Learning?

GeeksForGeeks describes it best:

    Reinforcement learning is an area of Machine Learning. Reinforcement. It is about taking suitable action to maximize reward in a particular situation. It is employed by various software and machines to find the best possible behavior or path it should take in a specific situation. Reinforcement learning differs from the supervised learning in a way that in supervised learning the training data has the answer key with it so the model is trained with the correct answer itself whereas in reinforcement learning, there is no answer but the reinforcement agent decides what to do to perform the given task. In the absence of training dataset, it is bound to learn from its experience.

Reinforcement learning (RL) finds a sequence of interactions to avoid pain and recieve pleasure. So for a given action `X` reinforcment learning aims to find the highest possible reward `Y`. The great thing about it is that you don't need to tell the machine what all of the features mean to the RL learning agent, all you need to define is a set of actions and reward the agent based on what it does periodically. The agent figures everything else out itself.


### Biggest Issues With Reinforcement Learning

RL sounds great in theory, yet there's a fundamental issue with it. RL is extremely dumb. Bare with me, but I'm going to explain. To begin, watch the video below of the guy that made his own car racing agent using RL. The bottle necks should give you an idea of the problems. Once you finish watching return to this document to get a summarization. I'm also going to add another article [here](https://www.alexirpan.com/2018/02/14/rl-hard.html) that explains its issues. The next segment will be focused on the problem statement more than anything else.

https://youtu.be/r428O_CMcpI


### The Problem(s) That Need to Be Solved:

If you didn't see the issues of reinforcement learning in the article before, here they are again in a bullet point list:

1. Deep Reinforcement Learning Can Be Horribly Sample Inefficient
2. If You Just Care About Final Performance, Many Problems are Better Solved by Other Methods
3. Reinforcement Learning Usually Requires a Reward Function
4. Reward Function Design is Difficult
5. Even Given a Good Reward, Local Optima Can Be Hard To Escape
6. Even When Deep RL Works, It May Just Be Overfitting to Weird Patterns In the Environment


Basically, if we were to summarize everything, RL has a lot of issues. The key issue is that it, by default, doesn't know how to handle reward functions appropiately. It:

1. Clings to local optima
2. Can overfit too much
3. Designing rewards can be extremely difficult.


The `manifold-rl` library is a solution to those 3 problems:

1. Simplify Reward Design
2. Embed mechanisms to prevent overfit
3. Embed machanisms to prevent local optimas
4. Taking into account multiple objectives at once



### Problem Statement: Make reward design accessible and easy


Reward design is hard. It's the very act of telling the AI agent what's good, bad, and what's approaching good and bad as it's progressing through to a task. A mishaping of rewards and punishments are enough to cause an AI to crash and burn rather easily.

What a reward designer might face:

1. No knowing how to explain to the RL that it's heading in the right direction.
2. Overfitting to one objective to the detriment of many other objectives that shows functionality.
3. Not knowing how to fit the rewards in a way where credit can clearly be assigned
4. Not giving enough inference that there are better rewards available by slightly changing its strategy from a given point, therefore becoming massively stuck in a local optima.
5. Providing too much punishment at the wrong point, which would destroy the learning process.
6. Ordering of priorities based on present state.



The list goes on, however those are the key issues with reward design.

`Manifold` will solve all of these problems using the same library in a modular manner. The last part of this primer will look how we'll solve that issue through a combination of techniques.



### The Cobra Effect
To get a better understanding of what we mean for creating rewards with multiple objectives  look no further than the cobra effect. It's an interesting idea.


According to Wikipedia:

    The cobra effect occurs when an attempted solution to a problem makes the problem worse,[1][2] as a type of unintended consequence. The term is used to illustrate the causes of incorrect stimulation in economy and politics.[2] 

    The term cobra effect originated in an anecdote, set at the time of British rule of colonial India. The British government was concerned about the number of venomous cobra snakes in Delhi.[3] The government therefore offered a bounty for every dead cobra. Initially this was a successful strategy as large numbers of snakes were killed for the reward. Eventually, however, enterprising people began to breed cobras for the income. When the government became aware of this, the reward program was scrapped, causing the cobra breeders to set the now-worthless snakes free. As a result, the wild cobra population further increased.[2][4]



In other words, the cobra effect is the activity of making things worse as we create incentives to make things better. It's the result of using common sense and providing a single, easy to measure objective without considing all other components are involved. It can be argued that this issue exists inside of all forms governance & social systems. In fact, wikipedia was kind enough to [showcase two more examples](https://en.wikipedia.org/wiki/Cobra_effect):


**Carbon credits for HFC-23**

The UN Intergovernmental Panel on Climate Change kicked off an incentive scheme in 2005 to cut down on greenhouse gases. Companies disposing of polluting gases get rewarded with carbon credits, which could eventually get converted into cash. The program set prices according to how serious the damage the pollutant could do to the environment was, and attributed one of the highest bounties for destroying HFC-23, a byproduct of a common coolant. As a result, companies began to produce more of this coolant in order to destroy more of the byproduct waste gas, and collect millions of dollars in credits.[6] Credits for the destruction of HFC-23 were suspended in the European Union in 2013.[7]


**Pig eradication in Georgia, US**

Most management strategies of the wild pig (Sus scrofa) had proven ineffective at reducing or eliminating its populations, resulting in population expansion in recent decades. As other places, the Fort Benning Army Infantry Training Center in Georgia, US, had been inhabited by wild pigs since the mid‐1900s. In response to increasing negative impacts on flora, fauna, and military training activities and equipment, Fort Benning began offering a bounty on pigs in June 2007 to reduce the population and eventually eradicate wild pigs from the installation. However, the hog population grew, possibly because of food set out to lure pigs.[8] 



## The Solution to The Cobra Effect: Multi-Objective Optimization

While not popular in many headlines, multi-objective optimization may be 100% of what we need to have safe AI. We see here, that researchers were able to implant [social customs](https://techxplore.com/news/2019-12-multi-objective-optimization-approach-socially-aware.amp) into their bots by using it. In other words, the machine was able to consider soft rules while also optimizing its travel path (main objective).

Whether we know it or not, human beings do this naturally. Actually, all animals do. They prioritize living, while also prioritizing meaning, they prioritize feeding themselves while also prioritize feeding their loved ones, and community. Human beings are living with billions of objectives pressuring us.

We need to embed the same power into machines. However, this isn't necessary popular yet. Take a look at [Arxiv](https://arxiv.org/search/?query=multi-objective+reinforcement+learning&searchtype=all&abstracts=show&order=-announced_date_first&size=50) and you'll find that combining the term multi-objective and reinforcement learning yields nearly `0` results.


The very fact that it's not popular is the clear lack of need upfront. Our library will both utilize multi-objective optimization and we'll show the need for it as well.



## Design Of Manifold

For the manifold library to work, we need to:

1. Incorporate multiple variables into a single reward
2. Rank those variables and assign weights to each variable so we can combine the numbers
   1. Have mechanisms to determine the rank.
   2. The rank will be determined by the current state of the variable.
3. Have an easy way to declare the previous two things
4. Input each monitored variable in a reinforcement learning environment live
5. Get a single returned output based on all of the variables.


To do that in a relatively easy manner, I'm suggesting a component design. Each component will have a set of rules. The components are:

1. **Scalarizer** - This class orders all of the variables we have in our problem and assigns a weight to them. Usually prior to weighing each specific reward and creating the larger reward.
2. **Objective** - The variable we're observing and generating a core reward for. This holds rules for the movemnet of that variable.
3. **Ranking** - Determines the "priority" of the reward we're observing.

```py
from manifold_ml import Manifold
from manifold_ml import Objective # Maybe rename it as attractor
from manifold_ml.objectives import Ranking # Should be expert scheme. It determines
from manifold_ml.scales import Scalarizer # use to determine order and weight of each variable


class SampleScalar(Scalarizer):
    """ Orders and scales the reward according to the rules we set. """


# TODO: ExpertScheme

class ActionRanking(Ranking):
    def __init__(self, name, minimum=0, maximum=1):
        super().__init__(name, minimum=minimum, maximum=maximum)

    def processing_rule(self):
        # Takes the current history and transforms it
        return 0.5
    
    def transform(self):
        objective_priority = self.processing_rule()
        return objective_priority


class ActionLimiter(Objective):
    def __init__(self, name, ranking):
        super().__init__(name, ranking)
    
    @property
    def priority(self) -> float:
        """ Get the priority from the ranking function. """
        return 1.0

    def transform(self):
        """ We'll get the reward for this single variable here"""
        return 0.0

# We'd declare the main manifold class here
manifold = Manifold()

# We add the variables we want to add
manifold.add(
    ActionLimiter(
        name='action',
        ranking=ActionRanking()
    )
)

# arbitrary parameters goes here
manifold.scalar = SampleScalar(...)
manifold.reset() # resets all of the variables in the manifold


for i in range(1000):
    value = random.uniform(10, 1000)
    manifold.add_value(name='action', value, ambient={})
    # Other values would go here
    manifold.add_value(name='other_value', value, ambient={})
    manifold.add_value(name='other_value_2', value, ambient={})
    reward = manifold.reward # We get the reward here according to the rules we set.
```


## Components

TODO: Create smallest unit of components!!!!
How????

### 10 Observational Components For Manifold

1. Change over window
2. Difference from value (scalar, or anything else)
3. Speed Of Change
4. Desired Speed Of Change
5. Hot Streak
6. Fuzzy Hot Streak
7. Objective Decay
8. Objective Growth
9. Categorical 
   1.  Data Over Time
10. Growth-Decay


### Lowest Level Components For Determining Score

1. Change - Monitoring the change of a variable over time
2. Categorical - Determine the score by category
3. Response - Response rules for the change/category component
4. Combine - Methods of combining multiple variables into a single score