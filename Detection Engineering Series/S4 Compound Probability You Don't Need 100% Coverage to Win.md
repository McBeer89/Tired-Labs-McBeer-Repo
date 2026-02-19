# Compound Probability: You Don't Need 100% Coverage to Win

**Author:** VanVleet  
**Published:** September 5, 2024  
**Reading Time:** 6 min read  
**Part of:** [Threat Detection Engineering: The Series](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62)

![VanVleet Profile](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

---

<!-- Image: Article header image - not accessible -->

This article is part of a [series on Threat Detection](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62). In this post, I'm going to use compound probability to show why you don't need to have 100% attack surface coverage to have a strong chance of detecting attackers in your environment.

In this article I'm building on previous topics, so you'll find it easier to follow along if you've already read the [other articles in the series](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62), but here are some key points you'll need to know:

1. Defending a network can be described as a [game of probability](https://medium.com/@vanvleet/threat-detection-strategy-a-visual-model-b8f4fa518441): how probable is it that an attacker will select a path from initial access to their objective that doesn't alert you to their presence?
2. Not all detections provide the same amount of attack surface coverage. The best detection is the one that provides the most incremental coverage.

## Compound Probability

First let's take a trip back to our years of high school math. Compound probability is the likelihood of two or more separate events happening. For example, the probability of rolling a one three times in a row. The formula for this is:

P(A and B) = P(A) * P(B)

So, the probability of **both** events happening is the probability of the first event times the probability of the second event. Using our example of rolling a one three times in a row:

P(rolling a 1) = 1/6

P(rolling a 1 three times) = 1/6 * 1/6 * 1/6 = 1/216

It's intuitive that as we add more events to the calculation, the likelihood of them all happening as desired decreases rapidly. If we want to get four ones in a row, the chances drop to 1 in 1296.

## Compound Probability in Threat Detection

Every time an attacker takes an action in your enterprise's environment, they are rolling the dice. They have an objective for each action: something they want to accomplish (persistence, lateral movement, privilege escalation, etc). They also have a finite number of techniques to choose from to accomplish that objective. When they pick a specific technique, they're taking a gamble that you don't have any detections in place to alert you to the action they're taking. If they are successful, they get to stay on the network undetected and continue towards their final objective. If they fail, you get an alert and start a response to kick them out. Putting this back into the [visual model](https://medium.com/@vanvleet/threat-detection-strategy-a-visual-model-b8f4fa518441), **each attack technique they execute is a roll of the dice. The probability of their success is determined by the percentage of techniques that you have covered (for a given tactic).**

<!-- Image: Visual representation of attacker's path through techniques as dice rolls -->

They have to continue to roll the dice action by action as they forge a path through your network to their objective. While the odds might be in their favor for each individual roll, compound probability strongly favors the defender. The likelihood of guessing correctly over and over again gets smaller and smaller with every new roll, even if our attack surface coverage isn't impressive. For an example, let's assume an attack surface coverage of only 33% of the full attack surface, meaning we have detections or preventative policies in place for 33% of all the attack techniques in each tactic. That means an attacker has a 33% chance of failure and a 66% chance of success each roll. Further, let's imagine that an attacker can get from initial access to their final objective in just 5 actions (that would be an impressive feat in real life, but it serves well to demonstrate the point). The probability of an attacker choosing a technique we don't have covered 5 times in a row is:

P(choosing right 5 times w/ a 66% chance) = ⅔ * ⅔ * ⅔ * ⅔ * ⅔ = **13%**

Those odds are definitely in the defender's favor! And they just improve as our attack surface coverage increases. Let's explore how improving the attack surface coverage changes the odds. We'll use the above example of a 5 step attack.

* At 15% coverage, an attacker's odds are 44%.
* At 25% coverage, their odds drop to 24%.
* At 33% coverage, the odds go to 13%.
* At 40% coverage, the odds are just 7%.
* If we can reach 50% coverage, they have only a 3% chance of success.

The math also works in the defender's favor as we increase the number of steps an attacker needs to take in our environment, which is effectively the goal of many security practices like least privilege, network segmentation, zero trust, etc. Using a static 33% attack surface coverage:

* An attacker's odds of guessing right 5 times in a row is 13%.
* The odds of guessing right 6 times in a row is 9%.
* The odds of guessing right 7 times in a row is only 6%.
* The odds of guessing right 8 times is 3%.

Now, if we could get 50% coverage AND require the attacker to take 8 steps, their chance of success is a paltry .4%! Compound probability is a big ally to blue teams!

## Focusing on Attack Surface Coverage

This further illustrates the point that **detection engineers should focus their efforts on the detections that will increase their attack surface coverage the most.** In my [original article](https://medium.com/@vanvleet/threat-detection-strategy-a-visual-model-b8f4fa518441), I do some calculations on different types of detections and show how some provide considerably more detection coverage than others. Time and effort spent on producing as-comprehensive-as-possible detections will pay off as attack surface coverage increases. On the other hand, time and effort spent on low-coverage detections doesn't yield much when an attacker is rolling the dice.

It's probably a good time to note that estimates of attack surface coverage are always estimates. It would be a rare situation to be able to say you have 100% coverage of an attack technique (you'd need [100% identification and 100% classification](https://medium.com/@vanvleet/identifying-and-classifying-attack-techniques-002c0c4cd595), a high bar to reach!). However, as Luke Paine illustrated in a [recent article](https://posts.specterops.io/to-infinity-and-beyond-feab2d8ff93c), if we test enough of the known procedures, we can gain a good approximation of what our coverage likely is. Determining our real attack surface coverage requires understanding the possible procedures of an attack technique (for which a [detection data model](https://medium.com/@vanvleet/improving-threat-identification-with-detection-data-models-1cad2f8ce051) excels) and a robust testing program.

## Independent Events and Truly Random Choices?

For the sake of simplicity, we've treated the attacker's choices of techniques as independent events and a fully random choice (i.e. any of the available options are equally likely to be chosen). In reality, there are ways in which that isn't totally accurate. The most significant of these is the case of EDR detections.

A good EDR solution will provide significant attack surface coverage out of the box, which would appear to really tip the probability in your favor. However, due to the commercial nature of EDR solutions and their wide user base, attackers often have the opportunity to determine what techniques an EDR will detect before they use them on your network. So they can eliminate those techniques from their list of options before they make their selection. Thus, the decision isn't fully random: an attacker is way less likely to select a technique they expect your EDR to detect. In the case of attackers with VERY good OpSec (the [red team kind](https://www.blackhillsinfosec.com/wp-content/uploads/2021/03/SLIDES_OPSECFundamentalsRemoteRedTeams-1.pdf) of OpSec), this counter-balances the coverage provided by your EDR. The net effect is to narrow the range of options that they will choose from, and our probability game is played on a smaller field.

That doesn't mean your EDR's coverage is worthless, though. Not all attackers have good OpSec (some criminal actors don't seem to care much about OpSec at all). Also, a good EDR is always putting out new detections, so an attacker can't assume that it'll miss something today that it missed yesterday. Finally, a smaller field is still to the defender's advantage: it's easier to reach 50% coverage when there are less techniques to cover. This just means that, **in addition to having an EDR, blue teams need to create their own custom detections to fill gaps left by their EDR solutions. For attackers of a certain skill level, the real game of probability is played only in the space left by the EDR.**

## Thoughts?

If you have any thoughts to add, post a comment below!

---

**Tags:** Threat Detection, Detection Engineering, Infosec, Cybersecurity