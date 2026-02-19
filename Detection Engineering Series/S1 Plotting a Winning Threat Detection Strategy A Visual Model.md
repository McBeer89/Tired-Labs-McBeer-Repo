# Plotting a Winning Threat Detection Strategy: A Visual Model

**Author:** VanVleet  
**Published:** January 23, 2024  
**Reading Time:** 9 min read  
**Part of:** [Threat Detection Engineering: The Series](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62)

![VanVleet Profile](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

---

<!-- Image: Article header image - not accessible -->

This article is part of a [series on Threat Detection](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62). In this article, I'm going to set up a model for thinking about threat detection and then use it to answer two fundamental questions:

1. Where is the best place to focus detection engineering efforts to maximize impact?
2. How do we evaluate the quality of a detection? What makes one detection better or worse than another?

## The Model

First we'll build a visual model. we'll start with Mitre's ATT&CK framework for Windows.

<!-- Image: Mitre's ATT&CK Framework for Windows - diagram showing the ATT&CK matrix -->

We're going to represent each technique as a single dot.

<!-- Image: Diagram showing each technique represented as a single dot in the model -->

Then, if we've done a good job defining our attack techniques, an attacker's path through the network from initial access to objective could be represented as a path between dots. Obviously, an attacker doesn't have to use a technique from EVERY tactic, but they do have to use SOME.

<!-- Image: Diagram showing an attacker's path through dots from initial access to objective -->

Using this model, the goal of threat detection is to build mechanisms to prevent and/or detect as many techniques as possible, so an attacker can't get from initial access to objective without triggering alarms. At this point, it becomes a game of probability: how probable is it that an attacker will take a path through that doesn't alert you to their presence?

<!-- Image: Diagram showing coverage of techniques to prevent attacker paths -->

Let's make this simple model just a little more realistic. Many techniques have numerous sub-techniques. There are 193 techniques and 401 sub-techniques in ATT&CK v12. We're going to approximate that by turning some dots into clusters of dots, so that each dot now represents a sub-technique.

<!-- Image: Diagram showing dots clustered together representing sub-techniques -->

Then, let's consider that each sub-technique may have multiple distinct procedures for how it can be executed. Jared Atkinson provides a very compelling demonstration of this idea in an excellent [blog series](https://posts.specterops.io/on-detection-tactical-to-function-810c14798f63) where he refines the definition of a "procedure." He demonstrates with an example where he identifies 4 distinct procedures for the sub-technique "OS Credential Dumping: LSASS Memory" and graphs them into a single chart, which I'm going to call a "procedure map."

<!-- Image: T1003.001 OS Credential Dumping: LSASS Memory procedure map by Jared Atkinson -->

(Adding my own note to Jared's work here: a procedure map should only include the ESSENTIAL operations that MUST BE EXECUTED in order to implement the procedure. We'll talk more about this when we discuss detection data models.)

Adding in procedures, our model becomes a mass of dots and clusters of dots, with each dot representing a procedure and clusters representing procedures that implement the same sub-technique, or Jared's "sub-technical synonyms."

<!-- Image: Diagram showing mass of dots and clusters representing procedures and sub-techniques -->

## Answering the Questions

Using this model, let's discuss what makes the best detection. The natural answer is "the detection that comprehensively covers the most dots." The more dots a detection covers, the more likely an attacker's path through the network will traverse one of them. But from a logistical perspective, it's impractical to detect unrelated procedures in a single detection. (It's hard enough to maintain simple detections, who needs complex ones?) So, if we can find closely related procedures that can be covered in a single detection, or a set of related ones, that's where we get the most impact. Luckily, this grouping of related procedures is already done for us: sub-techniques are often a cluster of related procedures. So, the theoretically ideal detection would be the ***one that comprehensively covers all the procedures of a single sub-technique.***

<!-- Image: Diagram highlighting ideal detection coverage -->

The detection engineering task is to find the best detection possible given the sub-technique's procedure map, available telemetry, and environmental noise. We're going to borrow Jared's procedure map again to dive in a little deeper.

* A detection that can catch all four procedures (at one of the graph's bottlenecks, for example) is the theoretical **ideal** (yellow on the graph). (Whether or not that ideal is viable depends on telemetry and noise in the given environment.)
* A set of detections that catch all four, perhaps at different points, is the **second best** (green on the graph). You have the same coverage, and just a little more work to maintain.

<!-- Image: LSASS procedure map with yellow highlighting showing ideal detection points -->

These are the best case scenarios. In real life, we are often only able to detect some of the procedures, or even some portion of some procedures. The rest are a known gap.

Now let's discuss the worst case scenarios.

The first is one where all we can do is detect the **tangential** elements (brown on the graph) of a procedure, like the command line parameters used by a specific tool that implements one of the procedures. When we focus on tangential elements, there are almost infinite paths through the procedure map. (An attacker can create a new path by writing a new tool, scripting the procedure, using command-line obfuscation, or load and execute the tool in memory, just to name a few.)

<!-- Image: LSASS procedure map with brown highlighting showing tangential detection points -->

Detecting **tangentials** shifts the probability game to strongly favor the attacker. This shouldn't be done until all better options have been exhausted. (And yet, much of the publicly available threat detection content is of this nature!)

The next common detection pattern that falls in the worst case category is the one that looks for **tuples** of procedures. For example, the detection might look for an EXE, ISO, or ZIP file written by Outlook (T1566.001 Spearphishing Attachment) that executes a Powershell script (T1059.001 Powershell). The problem is that this detection covers a specific 2-tuple of dots.\* Any other combination, even using some of the same procedures, won't be caught. This turns our hundreds of dots into a hundred thousand 2-tuples! (If we had 500 procedures, there would be [124,750 possible 2-tuple combinations](https://www.calculatorsoup.com/calculators/discretemathematics/combinations.php?n=500&r=2&action=solve).) Covering that many combinations requires a lot of detections, so this clearly shifts the probability game in the attacker's favor.

<!-- Image: Diagram showing tuple detection pattern -->

*\* We give this hypothetical detection more credit than it deserves. This example is worse than just a procedure chain, because it doesn't comprehensively cover all the individual procedures in the chain. An attacker could traverse the exact path and still evade detection by using a different implementation of the procedure, like phishing with a different file type.*

There's one more observation to extract here. Let's explore our LSASS Memory example a little further. Let's suppose we have telemetry from the Process Access operation showing the target process and requested access rights (maybe from an EDR hook on NtOpenProcess, for example). We'll add the rights requested by each tool to our graphic. (Note that reading credentials from LSASS memory only actually needs the "PROCESS\_VM\_READ" permission, but at least two tools overshoot and request all possible permissions.)

* A detection (or set of detections) for LSASS with any flag combination that includes "PROCESS\_VM\_READ" or "PROCESS\_CREATE\_PROCESS" or "PROCESS\_DUP\_HANDLE" would be the theoretical **ideal** (yellow) because it covers all 4 procedures at an essential operation.
* A detection looking for LSASS and "PROCESS\_ALL\_ACCESS" is a worst case scenario, because it's looking for the specific implementation of a specific tool (or tools, in this case). Even though it looks very similar to the ideal, we're really back to detecting **tangentials** (brown).

<!-- Image: LSASS procedure map with process access rights annotations -->

## Doing the Math

Using this model, we can make a rough mathematical representation of the incremental coverage value of a given detection. Let's pretend that there are 500 total procedures in our cluster of dots (that's probably way too low, but it suffices for our purposes).

* A detection that comprehensively covers one procedure covers 1/500th of the total attack surface.
* A detection that covers 4 procedures (like our ideal detection in the LSASS Memory example) covers 4/500th of the attack surface.
* A detection that can only reliably cover half of a procedure is still covering 1/1000th of the attack surface.
* A detection that covers 1 2-tuple is covering 1/124,750th of the attack surface (remember that 500 items allows for 124,750 possible 2-tuples).
* A detection that covers one tangential element is effectively covering 1 of nearly infinite options, but for the sake of our math let's generously assume there are only 1,000 different tangential elements an attacker could introduce. Thus, it covers 1/1,000th of 1 of 500 procedures, so that's 1/500,000th of our attack surface.

Obviously, our math is rough, but it serves to illustrate a few important points:

1. Not all detections provide the same coverage value.
2. Our coverage impact is orders of magnitude greater when we focus detection efforts on covering a procedure as comprehensively as possible.
3. Detection strategies that use tangential elements or tuples shift the probability game in favor of the attacker. They shouldn't be pursued until more effective options have been exhausted. ([Some cover so little attack surface that they may not be worth the development and maintenance effort!](https://medium.com/@vanvleet/the-threat-detection-balancing-act-coverage-vs-cost-cdb71d21412f))
4. The best level to focus our detection engineering efforts is the sub-technique level, where we have clusters of similar procedures that we might be able to detect together.

## One Last Pattern

There is one last type of detection pattern that can be effective, which I'm going to call a "grouple" detection. This is similar to the tuple pattern, but differs in a critical way. Instead of looking at just tuples of single procedures, it's looking for tuples of entire groups or categories of procedures. For example, we might look for ANY alert under the "Initial Access" tactic, followed within a certain timeframe by ANY alert in the "Persistence" tactic.

<!-- Image: Diagram showing "grouple" detection pattern across tactic groups -->

This detection pattern has the potential to be effective, so long as our coverage of the individual procedures in each group is good. But where it particularly excels is in situations where telemetry for a given procedure is too noisy to alert on directly. We can't cover the procedure itself, but we can alert when it co-occurs with other (possibly also noisy) procedures, allowing us to build in some coverage where none is otherwise possible. That makes "grouple" detections an excellent option to cope with those inevitable cases where the environment noise is just too loud to permit a high-fidelity detection (scheduled tasks, I'm looking at you!).

## The Winning Strategy

Using this visual model, I hope I've offered some compelling answers to my two fundamental questions:

**Q**: Where is the best place to focus detection engineering efforts to maximize impact?

**A**: *At the sub-technique level, covering each procedure as comprehensively as possible.*

**Q**: How do we evaluate the quality of a detection? What makes one detection better or worse than another?

**A**: *The best detection is the one that covers the procedures of a sub-technique as comprehensively as possible. Be careful to focus on essential elements, not tangential ones! Detections that focus on tangential elements are not helping us win.*

## Summary

With these answers, we can see that a great strategy for winning this game of probability is to review each sub-technique one by one and implement rules to detect (or to prevent) each procedure. Where telemetry shortcomings or environmental noise prevent a detection, we can generate an event that can be bundled into "grouple" detections.

<!-- Image: Summary diagram showing the complete strategy -->

If you can cover enough of the threat space, and maybe with a little help from Lady Luck, you can keep attackers out of your network!

## Thoughts?

Hopefully this exploration of my visual model has helped clarify the challenges we detection engineers are constantly trying to tackle! If you have any thoughts to add, post a comment or let me know on [Twitter](https://twitter.com/_vanvleet)!

*Originally published at [https://www.linkedin.com](https://www.linkedin.com/pulse/threat-detection-visual-model-andrew-vanvleet).*

---

**Tags:** Threat Detection, Threat Hunting, Detection Engineering, Information Security